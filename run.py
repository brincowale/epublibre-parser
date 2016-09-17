import json
import re
import time
from web_parser import WebParser
from database import Database


def create_next_page_url(url_index, first_number_book_current_page):
    return url_index['prefix_url'] + str(first_number_book_current_page) + url_index['suffix_url']

with open('config.json', encoding="utf8") as config_file:
    config = json.load(config_file)

first_number_book_current_page = config['url_index']['first_number_book_per_page']
url_index = create_next_page_url(config['url_index'], first_number_book_current_page)

parser = WebParser()
db = Database(config['server_sql'])

next_page = True
while next_page:
    books_url = parser.get_ebooks_url_from_index(url_index)
    next_page = parser.next_page()
    for book_url in books_url:
        book_id = re.findall("/(\d*)$", book_url)[0]
        if not db.book_exists(book_id):
            try:
                book = parser.extract_data_from_book(book_url)
                book[6] = '|'.join(book[6])
                db.insert_book(book)
                time.sleep(config['wait_seconds_between_books'])
            except:
                print('Unknow error')
    first_number_book_current_page += config['url_index']['increment_books_per_page']
    url_index = create_next_page_url(config['url_index'], first_number_book_current_page)

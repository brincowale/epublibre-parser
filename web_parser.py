import logging
import re
from grab import Grab


class WebParser:
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)
        self.grab = Grab()

    def get_ebooks_url_from_index(self, index_url):
        self.grab.go(index_url)
        books = self.grab.doc.select('//a[@id="stk"][@rel="popover"]')
        return [book.attr('href') for book in books]

    def extract_data_from_book(self, book_url):
        self.grab.go(book_url)
        book_id = re.findall("/(\d*)$", book_url)[0]
        title = self.grab.doc.select('//div[@id="titulo_libro"]').text()
        author = self.grab.doc.select('//a[contains(@href, "/autor/")]').text()
        cover_img_url = self.grab.doc.select('//img[@id="portada"]').attr('src')
        magnet_link = self.grab.doc.select('//a[@id="en_desc"]').attr('href')
        synopsis = self.grab.doc.select('//div[@class="detalle"]/div[@class="ali_justi"]/span').text()
        tags = [category.text() for category in self.grab.doc.select('//a[contains(@href, "/genero/")]')]
        pages = self.grab.doc.select('//table/tr/td/span[@class="well_blue btn-small negrita celda-info"]')[0].text()
        published_year = self.grab.doc.select('//table/tr/td/span[@class="well_blue btn-small negrita"]')[1].text()
        return [book_id, title, author, cover_img_url, magnet_link, synopsis, tags, pages, published_year, book_url]

    def next_page(self):
        """
        Must be used after method get_ebooks_url_from_index
        :return: True when this isn't the last page
        """
        next_page = self.grab.doc.select('//li[@id="pagina"][last()-1]/a')
        if 'siguiente' in next_page.text().lower():
            return True
        return False

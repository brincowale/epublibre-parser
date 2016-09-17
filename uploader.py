from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import json
from database import Database


class Wordpress:

    def __init__(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        config_wp = self.config['wp_login']
        print(config_wp['username'])
        print(config_wp['password'])
        print(config_wp['url'])
        self.wp = Client(config_wp['url'], config_wp['username'], config_wp['password'])
        self.db = Database(self.config['server_sql'])

    def publish_post(self, title, content, tags):
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'publish'
        post.terms_names = {
            'category': tags.split('|'),
        }
        post.id = self.wp.call(posts.NewPost(post))

    def get_post(self):
        book = self.db.get_book_not_published()
        url_referido = "https://www.amazon.es/s/?field-keywords={}&tag=REPLACE_TAG-21".format(book[1].replace(' ', '+'))
        content = '<a href="{}">Titulo: {}\nAutor: {}\nNúmero de páginas: {}\nAño de publicación: {}\n\n' \
                  '<img src="{}">\n\nHistoria: {}\n\n</a>'.format(url_referido, book[1], book[2], book[7], book[8],
                                                                  book[3], book[5])
        self.publish_post(book[1], content, book[6])

wp = Wordpress()
wp.get_post()

from sqlalchemy import MetaData, Table, Column, Integer, String, Text, Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from sqlalchemy.exc import IntegrityError
import sqlite3


class Database:

    def __init__(self, server_sql):
        self.metadata = MetaData()
        self.books = self.create_database()
        self.engine = create_engine(server_sql)
        self.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.session = session()
        self.conn = sqlite3.connect('books.db')

    def create_database(self):
        return Table('books', self.metadata,
            Column('id', Integer(), primary_key=True, nullable=False, unique=True),
            Column('title', String(255), index=True),
            Column('author', String(50)),
            Column('cover_img_url', String(50)),
            Column('magnet_link', Text()),
            Column('synopsis', Text()),
            Column('tags', Text()),
            Column('pages', Integer()),
            Column('published_year', Integer()),
            Column('book_url', String(255)),
            Column('published', Boolean()))

    def insert_book(self, book):
        book_id, title, author, cover_img_url, magnet_link, synopsis, tags, pages, published_year, book_url = book
        ins = self.books.insert().values(
            id=book_id,
            title=title,
            author=author,
            cover_img_url=cover_img_url,
            magnet_link=magnet_link,
            synopsis=synopsis,
            tags=tags,
            pages=pages,
            published_year=published_year,
            book_url=book_url,
            published=False
        )
        try:
            self.engine.execute(ins)
            return True
        except IntegrityError:
            return False

    def get_book_by_id(self, book_id):
        s = select([self.books]).where(self.books.c.id == book_id)
        rp = self.engine.execute(s)
        return rp.first()

    def book_exists(self, book_id):
        s = select([self.books.c.id]).where(self.books.c.id == book_id)
        rp = self.engine.execute(s)
        if rp.first() is None:
            return False
        return True

    def get_book_not_published(self):
        query = self.session.query(self.books)
        book = query.filter(self.books.c.published == False).limit(1).first()
        self.conn.execute("UPDATE books set published = 1 where id=" + str(book.id))
        self.conn.commit()
        return list(book)

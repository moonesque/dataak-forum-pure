from requests_html import HTMLSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Threads, Posts, Forums, Authors, DeclarativeBase
from config import config
import logging


class Account:
    def __init__(self):
        self.session = HTMLSession()

    def get_post_key(self):
        """
        retrieve unique post key required for login
        """
        response = self.session.get(config.forum_url)
        post_key = response.html.xpath("//input[@name='my_post_key']", first=True).attrs['value']

        return post_key

    def do_login(self, post_key):
        """
        perform login using post key
        """
        payload = {
            "action": "do_login",
            "url": config.forum_url,
            "quick_login": "1",
            "my_post_key": post_key,
            "quick_username": config.forum_username,
            "quick_password": config.forum_password,
            "quick_remember": "yes",
            "submit": "ورود"
        }

        headers = config.headers

        self.session.post(config.login_url, data=payload, headers=headers)

    def login(self):
        logging.info('Connecting to forum...')
        post_key = self.get_post_key()

        logging.info('Attempting login...')
        self.do_login(post_key)

        return self.session


class Crawler:

    def __init__(self, session):
        """
        Initializes database connection and sessionmaker.
        Creates the tables.
        """
        self.http_session = session
        logging.info('Creating database tables...')
        engine = self.db_connect()
        self.create_tables(engine)
        self.db_session = sessionmaker(bind=engine)()

    @staticmethod
    def db_connect():
        """
            Performs database connection using CONNECTION_STRING from config.py.
            Returns sqlalchemy engine instance
        """
        return create_engine(config.CONNECTION_STRING, echo=False)

    @staticmethod
    def create_tables(engine):
        DeclarativeBase.metadata.create_all(engine)

    def get_forums(self, page=None):
        if page is None:
            page = self.http_session.get(config.forum_url)
        forums = [[l.absolute_links.pop(), l.text] for l in page.html.xpath('//td/strong/a')]
        return forums

    def get_threads(self, forum):
        response = self.http_session.get(forum[0])
        threads = [[l.absolute_links.pop(), l.text] for l in response.html.xpath(
            '//span[@class="subject_old" or @class="subject_new" or @class="subject_editable subject_old"]/a')]

        forum_row = self.db_session.query(Forums).filter_by(url=forum[0]).first()
        for t in threads:
            thread = Threads(thread=t[1], url=t[0], forum_id=forum_row.id)
            self.db_session.add(thread)
            self.db_session.commit()

        return threads

    def crawl(self):

        thread_links = self.get_thread_links()

        next_page_xapth = '//a[@class="pagination_next"][1]'
        author_xpath = './/div[@class="author_information"]//a/text() | .//div[@class="author_information"]//em/text()'
        body_xpath = './/div[@class="post_body scaleimages"]/text() | .//div[@class="post_body scaleimages"]//*/text()'
        posts_xpath = '//div[@class="post"]'
        logging.info('Harvesting posts...')
        while thread_links:
            current = thread_links.pop(0)
            pagination = [current[0]]
            while pagination:
                page = pagination.pop(0)
                response = self.http_session.get(page)
                if response.html.xpath(next_page_xapth):
                    nx_page = response.html.xpath(next_page_xapth)[0].absolute_links.pop()
                    pagination.append(nx_page)

                posts = response.html.xpath(posts_xpath)
                for p in posts:
                    author = p.xpath(author_xpath)[0]
                    author_row = self.db_session.query(Authors).filter_by(name=author).first()
                    if not author_row:
                        author_row = Authors(name=author)
                        self.db_session.add(author_row)
                        self.db_session.commit()

                    body = ''.join(p.xpath(body_xpath))
                    author_row = self.db_session.query(Authors).filter_by(name=author).first()
                    thread = self.db_session.query(Threads).filter_by(url=current[0]).first()
                    post = Posts(body=''.join(body), author_id=author_row.id, thread_id=thread.id)
                    self.db_session.add(post)
                    self.db_session.commit()

        self.http_session.close()
        self.db_session.close()

    def get_forum_links(self):
        """
            BFS traverse of links
        """
        init_links = self.get_forums()
        visited = []
        to_visit = init_links
        logging.info('Harvesting forums...')
        while to_visit:
            current = to_visit.pop(0)
            visited.append(current)
            response = self.http_session.get(current[0])
            to_visit = to_visit + self.get_forums(response)

        for i in visited:
            forum = Forums(url=i[0], forum_name=i[1])
            self.db_session.add(forum)
            self.db_session.commit()

        return visited

    def get_thread_links(self):
        forums = self.get_forum_links()
        threads = []
        logging.info('Harvesting threads...')
        for link in forums:
            threads = threads + self.get_threads(link)

        return threads

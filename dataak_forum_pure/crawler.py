from requests_html import HTML, HTMLSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Threads, Posts, Forums, Authors, CONNECTION_STRING, DeclarativeBase

class PostKey:
    forum_url = 'http://forum.dataak.com/index.php'

    def get_post_key(self):
        session = HTMLSession()
        response = session.get(self.forum_url)
        with open ('forum_home.html', 'w+') as page:
            page.write(response.text)
            print(response.status_code, 'forum write success.')
        postkey = response.html.xpath("//input[@name='my_post_key']", first=True).attrs['value']
        print('post key:', postkey)
        return postkey, session


class Login:
    login_url = 'http://forum.dataak.com/member.php'
    index_url = 'http://forum.dataak.com/index.php'

    def do_login(self, postkey, session):

        payload = {
            "action": "do_login",
            "url": "http://forum.dataak.com/index.php",
            "quick_login": "1",
            "my_post_key": postkey,
            "quick_username": "mahan",
            "quick_password": "@123456",
            "quick_remember": "yes",
            "submit": "ورود"
            }

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
            #"Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Host": "forum.dataak.com",
            #"Content-Length": "218",
            #"DNT": "1",
            #"Host": "forum.dataak.com",
            #"Origin": "http://forum.dataak.com",
            #"Connection": "keep-alive",
            #"Referer": "http://forum.dataak.com/member.php",
            #"Upgrade-Insecure-Requests": "1"
        }

        forum = session.post(self.login_url, data=payload, headers=headers)
        forum = session.get(self.index_url)

        with open('logged_in.html', 'w+') as page:
            page.write(forum.text)
            print(forum.status_code, 'logged_in write success.')

        return forum, session


class Post:
    def __init__(self, body, thread, author):
        body = body
        thread = thread
        author = author



class Crawl:

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = self.db_connect()
        self.create_tables(engine)
        self.db_session = sessionmaker(bind=engine)()

    def db_connect(self):
        return create_engine(CONNECTION_STRING, echo=True)

    def create_tables(self, engine):
        DeclarativeBase.metadata.create_all(engine)


    def get_forums(self, response, session):
        forums = [[l.absolute_links.pop(), l.text] for l in response.html.xpath('//td/strong/a')]
        print(forums)
        return forums

    def get_threads(self, forum, session):
        response = session.get(forum[0])
        threads = [[l.absolute_links.pop(), l.text] for l in response.html.xpath(
            '//span[@class="subject_old" or @class="subject_new" or @class="subject_editable subject_old"]/a')]

        forum_row = self.db_session.query(Forums).filter_by(url=forum[0]).first()
        for t in threads:
            thread = Threads(thread=t[1], url=t[0], forum_id=forum_row.id)
            self.db_session.add(thread)
            self.db_session.commit()

        return threads

    def get_posts(self, threads, session):
        to_crawl = []

        next_page_xapth = '//a[@class="pagination_next"][1]'
        # thread = '//span[@class="active"]/text()'
        author_xpath = './/div[@class="author_information"]//a/text() | .//div[@class="author_information"]//em/text()'
        body_xpath = './/div[@class="post_body scaleimages"]/text() | .//div[@class="post_body scaleimages"]//*/text()'
        posts_xpath = '//div[@class="post"]'
        # input('#############MARK0#################')
        while threads:
            current = threads.pop(0)
            response = session.get(current[0])
            pagination = []
            pagination.append(current[0])
            # input('#############MARK1#################')
            while pagination:
                page = pagination.pop(0)
                response = session.get(page)
                if response.html.xpath(next_page_xapth):
                    nx_page = response.html.xpath(next_page_xapth)[0].absolute_links.pop()
                    pagination.append(nx_page)


                posts = response.html.xpath(posts_xpath)
                print('posts:', posts)
                # input('#############MARK2#################')
                for p in posts:
                    author = p.xpath(author_xpath)[0]
                    author_row = self.db_session.query(Authors).filter_by(name=author).first()
                    if not author_row:
                        author_row = Authors(name=author)
                        self.db_session.add(author_row)
                        self.db_session.commit()
                        # input('#############MARK3#################')
                    print(author)
                    body = ''.join(p.xpath(body_xpath))
                    author_row = self.db_session.query(Authors).filter_by(name=author).first()
                    # input('#############{}#################'.format(author_row))
                    thread = self.db_session.query(Threads).filter_by(url=current[0]).first()
                    # input('#############{}#################'.format(thread))
                    post = Posts(body=''.join(body), author_id=author_row.id, thread_id=thread.id)
                    self.db_session.add(post)
                    self.db_session.commit()
                    # input('#############MARK4#################')

                    print(body)
                    input('End of post.')


    def get_links(self, init_links, session):
        '''
            BFS traverse of links
        '''
        crawled = []
        to_crawl = init_links

        while to_crawl:
            current = to_crawl.pop(0)
            crawled.append(current)
            response = session.get(current[0])
            to_crawl = to_crawl + self.get_forums(response, session)

        print('crawled links:', crawled)
        for i in crawled:
            forum = Forums(url=i[0], forum_name=i[1])
            self.db_session.add(forum)
            self.db_session.commit()
        return crawled

    def do_crawl(self, forums, session):
        threads = []
        for link in forums:
            threads = threads + self.get_threads(link, session)
        print(threads)
        return threads






# if __name__ == '__main__':

#     post = PostKey()
#     post_key, session = post.get_post_key()
#     login = Login()
#     index_page, session = login.do_login(post_key, session)
#     crawl = Crawl()
#     init_links = crawl.get_forums(index_page, session)
#     forums = crawl.get_links(init_links, session)
#     thread_links = crawl.do_crawl(forums, session)
#     crawl.get_posts(thread_links, session)






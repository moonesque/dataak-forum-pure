from dataak_forum_pure.models import Threads, Posts, Forums, Authors
from dataak_forum_pure.crawler import PostKey, Login, Post, Crawl


if __name__ == '__main__':

    post = PostKey()
    post_key, session = post.get_post_key()
    login = Login()
    index_page, session = login.do_login(post_key, session)
    crawl = Crawl()
    init_links = crawl.get_forums(index_page, session)
    forums = crawl.get_links(init_links, session)
    thread_links = crawl.do_crawl(forums, session)
    crawl.get_posts(thread_links, session)


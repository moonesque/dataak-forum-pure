from dataak_forum_pure.crawler import PostKey, Login, Crawl


if __name__ == '__main__':

    print('Running crawler...')
    post = PostKey()
    post_key, session = post.get_post_key()
    login = Login()
    index_page, session = login.do_login(post_key, session)
    crawl = Crawl()
    init_links = crawl.get_forums(index_page, session)
    forums = crawl.get_links(init_links, session)
    thread_links = crawl.do_crawl(forums, session)
    try:
        crawl.get_posts(thread_links, session)
        print('Crawl successful.')
    except e:
        print('Crawl failed.')



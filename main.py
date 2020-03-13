from dataak_forum_pure.crawler import Crawler, Account

if __name__ == '__main__':

    print('Running crawler...')
    account = Account()
    session = account.login()
    crawler = Crawler(session)
    try:
        crawler.crawl()
        print('Crawl successful.')
    except Exception as e:
        print('Crawl failed.')
        raise e

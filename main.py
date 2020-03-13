from dataak_forum_pure.crawler import Crawler, Account
from config import config
import logging

if __name__ == '__main__':

    logging.basicConfig(level=config.logging_level)
    logging.info('Running Crawler...')
    try:
        account = Account()
        session = account.login()
        crawler = Crawler(session)
        crawler.crawl()
        logging.info('Crawler executed successfully.')
    except Exception as e:
        logging.error('Crawler failed due to: %s', e)
        raise

from subprocess import Popen, PIPE


def scrape_article(article, mongo_uri, mongo_collection, mongo_db, mongo_user, mongo_password):
    spider_ps = Popen(['scrapy', 'parse', article, '-s', mongo_uri, '-s', mongo_db, '-s', mongo_collection,
                       '-s', mongo_user, '-s', mongo_password, "--pipelines", "-c", "parse_articles"])
    status_code = spider_ps.wait()
    flag = "ERROR: Unable to find spider" not in str(spider_ps.stderr.read())
    return True if status_code == 0 and flag else False


def scrape_international_articles(mongo_uri, mongo_db, mongo_collection, mongo_user, mongo_password):
    status = Popen(['scrapy', 'crawl', '-s', mongo_uri, '-s', mongo_db, '-s', mongo_collection,
                    '-s', mongo_user, '-s', mongo_password, "articles"]).wait()
    return True if status == 0 else False


import json
import logging
import configparser

from flask import Flask, request, Response

import mongo.operations
from spiders_subprocesses.scrape_processes import scrape_article, scrape_international_articles
from mongo.operations import search_articles
app = Flask(__name__)

logging.basicConfig(filename='record.log', level=logging.DEBUG)
logger = app.logger

config = configparser.ConfigParser()
config.read('config.ini')
mongo_uri, mongo_db = "MONGO_URI={}".format(config['MONGO']['URI']), "MONGO_DATABASE={}".format(
    config['MONGO']['Database'])
mongo_collection = "MONGO_COLLECTION={}".format(config['MONGO']['Collection'])
mongo_user, mongo_password = "MONGO_USER={}".format(config['MONGO']['User']), "MONGO_PASSWORD={}".format(
    config['MONGO']['Password'])

app = Flask(__name__)


# Define single article endpoint for scrapy
# Define API for mongodb queries
# Check for duplicates through the middleware when scraping


@app.route('/international-page', methods=['POST'])
def guardian_international_page():
    success_status = scrape_international_articles(mongo_uri, mongo_db, mongo_collection, mongo_user, mongo_password)
    return Response("success", status=200, mimetype='application/json') if success_status else Response("failed",
                                                                                                        status=404,
                                                                                                        mimetype='application/json')


@app.route('/guardian-article', methods=['POST'])
def guardian_article():
    success_status = scrape_article(request.json['article'], mongo_uri,
                                    mongo_db, mongo_collection, mongo_user, mongo_password)
    return Response("success", status=200) if success_status else Response("article not supported", status=406,
                                                                           mimetype='application/json')


@app.route('/find-article/<keyword>', methods=['GET'])
def find_articles(keyword):
    client = mongo.operations.get_client(config['MONGO']['URI'], config['MONGO']['User'], config['MONGO']['Password'])
    articles = json.dumps(search_articles(keyword,
                                          mongo.operations.get_database(client, config['MONGO']['Database']),
                                          config['MONGO']['Collection']), default=str)
    return Response(articles, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()

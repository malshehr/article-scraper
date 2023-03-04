import json
import logging
import configparser

from flask import Flask, request, Response

import mongo.operations
from spiders_subprocesses.scrape_processes import scrape_article, scrape_international_articles
from mongo.operations import search_articles

app = Flask(__name__)

# Managing configuration prior to running the Flask app

logging.basicConfig(filename='article-scraper.log', level=logging.DEBUG)
logger = app.logger

config = configparser.ConfigParser()
config.read('config.ini')
mongo_uri, mongo_db = "MONGO_URI={}".format(config['MONGO']['URI']), "MONGO_DATABASE={}".format(
    config['MONGO']['Database'])
mongo_collection = "MONGO_COLLECTION={}".format(config['MONGO']['Collection'])
mongo_user, mongo_password = "MONGO_USER={}".format(config['MONGO']['User']), "MONGO_PASSWORD={}".format(
    config['MONGO']['Password'])


# API for scraping all the articles present on The Guardian International page
@app.route('/international-page', methods=['POST'])
def guardian_international_page():
    success_status = scrape_international_articles(mongo_uri, mongo_db, mongo_collection, mongo_user, mongo_password)
    return Response("success", status=200, mimetype='application/json') \
        if success_status else Response("failed", status=404, mimetype='application/json')


# API for scraping an article url passed by the user in the body request
@app.route('/guardian-article', methods=['POST'])
def guardian_article():
    success_status = scrape_article(request.json['article'], mongo_uri,
                                    mongo_db, mongo_collection, mongo_user, mongo_password)
    return Response("success", status=200,
                    mimetype='application/json') if success_status else Response("article not supported", status=406,
                                                                                 mimetype='application/json')


# API for finding articles that are relevant to the provided keyword
@app.route('/find-article/<keyword>', methods=['GET'])
def find_articles(keyword):
    client = mongo.operations.get_client(config['MONGO']['URI'], config['MONGO']['User'], config['MONGO']['Password'])
    found_articles = search_articles(keyword,
                                     mongo.operations.get_database(client, config['MONGO']['Database']),
                                     config['MONGO']['Collection'])
    return Response(json.dumps(found_articles, default=str), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()

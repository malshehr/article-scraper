from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from itemadapter import ItemAdapter


def get_client(mongo_uri, mongo_user, mongo_password):
    return MongoClient(mongo_uri, username=mongo_user, password=mongo_password)


def get_database(client, database):
    return client[database]


def insert_item(database, collection, item):
    return database[collection].insert_one(ItemAdapter(item).asdict())


def search_articles(keyword, database, collection):
    query = {'title': {'$regex': keyword}}
    return [item for item in database[collection].find(query)]

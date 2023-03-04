from itemadapter import ItemAdapter

import mongo.operations


class ArticleCollectorPipeline:
    # Initializing the pipeline with proper mongo connection
    def __init__(self, mongo_uri, mongo_db, mongo_collection, mongo_user, mongo_password):
        self.db = None
        self.client = None
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.mongo_user = mongo_user
        self.mongo_password = mongo_password

    # Retrieving mongo configurations from subprocess commands
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION'),
            mongo_user=crawler.settings.get('MONGO_USER'),
            mongo_password=crawler.settings.get('MONGO_PASSWORD')
        )

    # validates the item prior to insertion to the database collection
    def process_item(self, item, spider):
        mongo.operations.insert_item(self.db, self.mongo_collection, item)
        return item

    def open_spider(self, spider):
        self.client = mongo.operations.get_client(self.mongo_uri,  self.mongo_user, self.mongo_password)
        self.db = mongo.operations.get_database(self.client, self.mongo_db)

    def close_spider(self, spider):
        self.client.close()

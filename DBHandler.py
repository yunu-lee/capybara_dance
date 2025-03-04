import datetime
import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()
uri = os.getenv('MONGODB_URI')


if __name__ == '__main__':
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db = client.real_estate

    collection = db['apt']

    doc = {
        'name': 'song',
        'price': 25000,
        'trade_type': 'buy',
        'time': datetime.datetime.now()
    }

    result = collection.insert_one(doc)

    # result = db['movies'].find()
    #
    # for doc in result:
    #     print(doc)
    #     pass

    client.close()

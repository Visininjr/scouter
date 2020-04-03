# author: Joshua Ren
# github: https://github.com/visininjr/
from os_stuff import get_current_dt
from pymongo import MongoClient
import gridfs
import json


class MongoDB:
    def __init__(self, port=27017):
        self.client = MongoClient('localhost', port)
        self.db = self.client['scouter']
        self.fs = gridfs.GridFS(self.db)
        self.author = 'Joshua Ren'

    def insert_one(self, location, type, image, metadata, direction, dt):
        '''
        type contains what type of object is being detected,
        the image, encoding information about the image, and
        some metadata about the image is stored in the db
        returns _id field from db to confirm successful insert into db
        '''
        collection = self.db[type]
        image_string = image.tostring()
        image_id = self.fs.put(image_string, encoding='utf-8')
        post = {
            'location': location,
            'type': type,
            'image': image_id,
            'shape': image.shape,
            'dtype': str(image.dtype),
            'meta': metadata,
            'image_direction': direction,
            'date_requested': dt,
            'author': self.author,
        }
        data = collection.insert_one(post)
        return data.inserted_id

    def update_one(self, location, type, image, metadata, direction, dt):
        item_id = self.db[type].find_one(
            {'location': location, 'image_direction': direction})['_id']
        self.delete_one(type, '_id', item_id)
        return self.insert_one(location, type, image, metadata, direction, dt)

    def get_count(self, collection, key, value):
        return self.db[collection].count_documents({key: value})

    def get_items(self, collection, key, value):
        return [item for item in self.db[collection].find({key: value})]

    def get_collection(self, collection):
        '''
        return list of documents
        '''
        return [item for item in self.db[collection].find()]

    def delete_one(self, collection, key, value):
        item_collection = self.db[collection]
        item_collection.delete_one({key: value})
        return id

    def delete_collection(self, collection):
        item_collection = self.db[collection]
        list_items = self.get_collection(collection)
        for item in list_items:
            item_collection.delete_one({'_id': item['_id']})
        return collection

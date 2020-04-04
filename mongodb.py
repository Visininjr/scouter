# author: Joshua Ren
# github: https://github.com/visininjr/
from os_stuff import get_current_dt
from pymongo import MongoClient
import gridfs
import numpy as np
import json


class My_MongoDB:
    def __init__(self, port=27017):
        self.client = MongoClient('localhost', port)
        self.db = self.client['scouter']
        self.fs = gridfs.GridFS(self.db)
        self.author = 'Joshua Ren'

    def insert_one(self, location, type, image, metadata, direction, count, dt):
        '''
        type is the name of the collection being accessed,
        the image, encoding information about the image, and
        some metadata about the image is stored in the db
        automatically performs check to see if data exists in db
        image is stored as an id in self.fs and is automatically converted back to cv2 when requested
        returns _id field from db to confirm successful insert into db
        '''

        collection = self.db[type]
        image_string = image.tostring()
        image_id = self.fs.put(image_string, encoding='utf-8')
        item_check_location = collection.find_one(
            {'location': location, 'direction': direction})
        item_check_image = collection.find_one(
            {'image': image_id})
        if item_check_location or item_check_image:  # if the item exists, delete it so it can be replaced
            item_id = item_check_location['_id']
            self.delete_documents(type, '_id', item_id)
        post = {
            'location': location,
            'type': type,
            'image': image_id,
            'shape': image.shape,
            'dtype': str(image.dtype),
            'meta': metadata,
            'direction': direction,
            'object_count': count,
            'date_requested': dt,
            'author': self.author,
        }
        data = collection.insert_one(post)
        return data.inserted_id

    def get_document_ids(self, collection, keys, values):
        '''
        returns the _id field of a document query
        if the object does not exist, an id of -1 is returned instead
        '''
        query = {}
        for i in range(len(keys)):
            query[keys[i]] = values[i]
        documents = self.db[collection].find(query)
        return [doc['_id'] if doc else -1 for doc in documents]

    def get_count(self, collection, key, value):
        '''
        returns count of documents of some key in a collection
        '''
        return self.db[collection].count_documents({key: value})

    def get_items(self, collection, key, value):
        '''
        returns a list of items for items with that key value
        '''
        ret = []
        for doc in self.db[collection].find({key: value}):
            image = self.__reshape_image(doc)
            doc['image'] = image
            ret.append(doc)
        return ret

    def get_collection(self, collection):
        '''
        return list of documents in a collection
        '''
        return [item for item in self.db[collection].find()]

    def delete_documents(self, collection, key, value):
        '''
        deletes documents of a specific key value
        returns number of documents deleted
        '''
        item_collection = self.db[collection]
        delete = item_collection.delete_many({key: value})
        return delete.deleted_count

    def delete_collection(self, collection):
        item_collection = self.db[collection]
        delete = item_collection.delete_many({})
        return delete.deleted_count

    def __reshape_image(self, document):
        g_out = self.fs.get(document['image'])
        img = np.frombuffer(g_out.read(), dtype=np.uint8)
        return np.reshape(img, document['shape'])

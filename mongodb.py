# author: Joshua Ren
# github: https://github.com/visininjr/
from os_stuff import get_current_dt
from pymongo import MongoClient
import gridfs


class MongoDB:
    def __init__(self, port):
        self.db = MongoClient('localhost', port)['scouter']
        self.author = 'Joshua Ren'

    def insert_one(self, type, id, data):
        '''

        '''
        column = self.db[type]
        post = {
            '_id': id,
            'type': type,
            'data': data,
            'author': self.author,
        }
        insert = column.insert_one(post)
        return insert.inserted_id  # return location from db confirm successful insert

    def insert_many(self, column, ids, datas):
        column = self.db[column]  # TODO

    def get_column(self, column):
        return [item for item in self.db[column].find()]

    def get_item(self, column, id):
        return self.db[column].find_one({'_id': id})

    def delete_entry(self, column, id):
        column = self.db[column]
        column.delete_one({'_id': id})
        return 'entry ' + id + ' successfully deleted'

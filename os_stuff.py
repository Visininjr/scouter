# author: Joshua Ren
# github: https://github.com/visininjr/
import os
from datetime import datetime
import json


def make_file_name(type, name):
    '''
    creates a file name for detected objects and classifies them
    ./person/conf_current_date_time.png
    '''
    make_dir(type)
    path = './' + type + '/' + name + '.png'
    return path


def get_current_dt():
    '''
    returns current date time
    '''
    return datetime.now()


def make_dir(dir_name):
    '''
    creates a directory
    '''
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def rename_file(p1, p2):
    '''
    renames a file from p1 to p2
    '''
    os.rename(p1, p2)


def get_subdirs(root):
    '''
    gets all subdirectories from a root path
    '''
    return [subdirs for dirs, subdirs, files in os.walk('./streetview_data')]


def file_exists(path):
    '''
    checks to see if the file exists and is a file (i.e. it is not a directory)
    '''
    return os.path.exists(path) and os.path.isfile(path)


def get_API_key(id):
    '''
    returns an API key
    '''
    secrets_filename = '../secret_keys'
    api_keys = {}
    with open(secrets_filename, 'r') as f:
        api_keys = json.loads(f.read())
    return api_keys[id]

# author: Joshua Ren
# github: https://github.com/visininjr/
import requests
import json
import cv2
import numpy as np
from os_stuff import get_API_key, get_current_dt
from item_detector import detect_objects, isolate_from_image, get_image_with_boxes
from mongodb import MongoDB

key = get_API_key('maps_key')


def lat_lng_stringify(lat, lng):
    '''
    turns latitude and longitude coordinates into string
    [45, 45] -> '45, 45'
    '''
    return str(lat) + ',' + str(lng)


def lat_lng_intify(location):
    '''
    turns string latitude and longitude location into list of ints
    '45, 45' -> [45, 45]
    '''
    lat_lng = location.split(',')
    return [lat_lng[0], lat_lng[1]]


def process_image_request(request):
    '''
    takes in a HTTPS request and downloads the image to the specified path.
    '''
    resp = request.raw
    image_arr = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
    return image


def process_metadata_request(location, direction, dt):
    '''
    takes in a HTTPS request and converts the metadata as a json file.
    returns the metadata result
    '''
    metadata_url = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
    metadata_request = requests.get(
        metadata_url + 'location=' + location + '&key=' + key)
    results_metadata = metadata_request.json()
    return results_metadata


def get_map(location):  # todo
    '''
    get data from db
    '''
    lat_lng = lat_lng_intify(location)
    raw_data = db_stuff()  # get data from db

    gmap = reference_my_heatmap2()


def save_streetview_image(location, type='object', use_small_model=False, force_run=False):
    '''
    gets the streetview images of a provided location
    need to take 4 images for each view to get 360 degree perspective
    images are ordered by location. 5 requests to api each run
    location is always in lat,lng to avoid inconsistencies and overlaps
    '''
    db = MongoDB()
    # url for getting images
    url = 'https://maps.googleapis.com/maps/api/streetview?'

    ids = []
    # get 4 images since each view is by default 90 degree fov
    # returns images as north, east, south, west
    for i, direction in enumerate(['north', 'east', 'south', 'west']):
        # update entry instead of adding a new one if they exist in db
        # document exists but want to update
        db_count = db.get_count(type, 'location', location)
        if (db_count >= 4 and force_run) or db_count < 4:
            request = requests.get(url + 'size=640x640' + '&location=' +
                                   location + '&heading=' + str(i * 90) + '&key=' + key, stream=True)
            if request.status_code == 200:
                cv_image = process_image_request(request)
                detected_objects = detect_objects(
                    cv_image, type, use_small_model)
                image_with_boxes = get_image_with_boxes(
                    cv_image, detected_objects[1], detected_objects[2], detected_objects[3])
                metadata = process_metadata_request(
                    location, direction, get_current_dt())
                id = db.insert_one(
                    location, type, image_with_boxes, metadata, direction, get_current_dt())
                ids.append(id)
            else:
                print('streetview image download for location ' +
                      location + direction + 'errored, code: ' + request.status_code)
        else:
            print(
                'streetview image exists for location ' + location + ' ' + direction + '. If you wish to override set the \'force_run\' parameter to True.')
    return ids


def test_error(results):
    try:  # error occurred
        test = results['error_message']
        return test
    except:  # no error
        return ''


def get_location(query):
    '''
    gets locations from user input using google places api
    returns a list of locations with metadata of each location
    '''
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    query_requests = requests.get(url + 'query=' + query + '&key=' + key)
    json_results = query_requests.json()
    results = json_results['results']
    if test_error(results):
        return []
    # json_results['next_page_token'] TODO
    locations = []
    for i in range(len(results)):
        lat = results[i]['geometry']['location']['lat']
        lng = results[i]['geometry']['location']['lng']
        lat_lng_string = lat_lng_stringify(lat, lng)
        locations.append(lat_lng_string)
    return [locations, results]

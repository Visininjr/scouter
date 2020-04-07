# author: Joshua Ren
# github: https://github.com/visininjr/
import requests
import json
import cv2
import numpy as np
from os_stuff import get_API_key, get_current_dt
from item_detector import detect_objects, isolate_from_image, get_image_with_boxes
from mongodb import My_MongoDB

KEY = get_API_key('maps_key')
DEFAULT = 'object'


def lat_lng_stringify(lat, lng):
    '''
    turns latitude and longitude coordinates into string
    [45, 45] -> '45, 45'
    '''
    return str(lat) + ',' + str(lng)


def lat_lng_numify(location):
    '''
    turns string latitude and longitude location into list of floats
    '45, 45' -> [45, 45]
    '''
    lat_lng = location.replace(' ', '').split(',')
    return (float(lat_lng[0]), float(lat_lng[1]))


def test_error(request):
    '''
    tests to see if an error occurred in the https request
    returns error message if there was one
    '''
    try:  # error occurred
        return request['error_message']
    except:  # no error
        return ''


def process_image_request(request):
    '''
    takes in a HTTPS request and returns the image as cv2
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
        metadata_url + 'location=' + location + '&key=' + KEY)
    results_metadata = metadata_request.json()
    return results_metadata


def save_to_db(db, location, cv_image, metadata, direction, dt, use_small_model):
    '''
    saves all images to DEFAULT collection
    also automatically saves images to their specific type collection
    '''
    ids = []
    detected_objects = detect_objects(
        cv_image, use_small_model=use_small_model)
    labels = detected_objects[2] + [DEFAULT]
    for type in set(labels):
        detected_objects = detect_objects(
            cv_image, type, use_small_model)
        object_count = len(detected_objects[1])
        image_with_boxes = get_image_with_boxes(
            cv_image, detected_objects[1], detected_objects[2], detected_objects[3])

        id = db.insert_one(
            location, type, image_with_boxes, metadata, direction, object_count, dt)
        ids.append((type, id))
    return ids


def save_streetview_image(location, use_small_model=False, force_run=False):
    '''
    gets the streetview images of a provided location
    need to take 4 images for each view to get 360 degree perspective
    images are ordered by location. 5 requests to api each run
    location is always in lat,lng to avoid inconsistencies and overlaps
    errors end the query early to save requests workload
    returns ids of images inserted into db
    '''
    db = My_MongoDB()
    url = 'https://maps.googleapis.com/maps/api/streetview?'
    ids = []
    # db count uses default type to get consistent results
    db_count = db.get_count(DEFAULT, 'location', location)
    # enable force_run if document exists but want to update
    if (db_count > 0 and force_run) or db_count == 0:
        # get 4 images since each view is by default 90 degree fov
        # returns images as north, east, south, west
        for i, direction in enumerate(['north', 'east', 'south', 'west']):
            request = requests.get(url + 'size=640x640' + '&location=' +
                                   location + '&heading=' + str(i * 90) + '&key=' + KEY, stream=True)
            metadata = process_metadata_request(
                location, direction, get_current_dt())
            dt = get_current_dt()
            # error check before inserting data into db
            if request.status_code == 200 and metadata['status'] == 'OK':
                cv_image = process_image_request(request)
                ids += save_to_db(db, location, cv_image, metadata,
                                  direction, dt, use_small_model)
            else:
                print(location + ' error getting image: ' +
                      metadata['status'] + ' HTTPS code: ' + str(request.status_code))
                break
    else:
        print('streetview images exist for location ' + location +
              '. If you wish to override this set the \'force_run\' parameter to True.')
    return ids


def get_location(query):
    '''
    gets locations from user input using google places api
    returns a list of locations in lat,lng format with metadata of each location
    '''
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    query_requests = requests.get(url + 'query=' + query + '&key=' + KEY)
    json_results = query_requests.json()
    results = json_results['results']
    if test_error(results):
        return []
    locations = []
    for i in range(len(results)):
        lat = results[i]['geometry']['location']['lat']
        lng = results[i]['geometry']['location']['lng']
        lat_lng_string = lat_lng_stringify(lat, lng)
        locations.append(lat_lng_string)
    return [locations, results]

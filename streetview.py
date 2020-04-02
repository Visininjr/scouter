# author: Joshua Ren
# github: https://github.com/visininjr/
import requests
import json
import cv2
import numpy as np
from os_stuff import make_dir, rename_file, get_API_key, get_current_dt
from item_detector import isolate_from_image
from mongodb import MongoDB
import shutil

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


def process_image_request(path, request):
    '''
    takes in a HTTPS request and downloads the image to the specified path.
    '''
    if request.status_code == 200:
        resp = request.raw
        image_arr = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)

        # for testing
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return request.status_code


def process_metadata_request(location, path, dt):
    '''
    takes in a HTTPS request and downloads the metadata as a json file.
    '''
    metadata_url = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
    metadata_request = requests.get(
        metadata_url + 'location=' + location + '&key=' + key)
    results_metadata = metadata_request.json()
    results_metadata['date_requested'] = dt
    full_path = path + '/metadata.json'
    with open(full_path, 'w') as fp:  # replace with putting into db
        json.dump(results_metadata, fp)


def get_map(location):
    '''
    get data from db
    '''
    lat_lng = lat_lng_intify(location)
    raw_data = db_stuff()  # get data from db

    gmap = reference_my_heatmap2()


def test_error(results):
    try:  # error occurred
        test = results['error_message']
        return test
    except:  # no error
        return ''


def download_streetview_image(location):
    '''
    gets the streetview images of a provided location
    need to take 4 images for each view to get 360 degree perspective
    images are ordered by location. 5 requests to api each run
    '''
    dt = str(get_current_dt())
    path_name = location.replace(',', '_')  # dir where data will be stored
    path = './data/' + location
    make_dir(path)

    # url for getting images
    url = 'https://maps.googleapis.com/maps/api/streetview?'

    # get 4 images since each view is by default 90 degree fov
    # returns images as north, east, south, west
    for i, direction in enumerate(['north', 'east', 'south', 'west']):
        request = requests.get(url + 'size=640x640' + '&location=' +
                               location + '&heading=' + str(i * 90) + '&key=' + key, stream=True)
        full_path = path + '/' + direction + '.jpg'
        if process_image_request(full_path, request) != 200:
            print('HTTP error ' + str(request.status_code) +
                  ' encountered for location ' + path_name + ' direction ' + direction)
    process_metadata_request(location, path, dt)
    print('streetview image download for location ' + path_name + ' success')


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
    print(json_results['next_page_token'])
    locations = []
    for i in range(len(results)):
        lat = results[i]['geometry']['location']['lat']
        lng = results[i]['geometry']['location']['lng']
        lat_lng_string = lat_lng_stringify(lat, lng)
        locations.append(lat_lng_string)
    return [locations, results]

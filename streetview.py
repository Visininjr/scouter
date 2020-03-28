# author: Joshua Ren
# github: https://github.com/visininjr/
import google_streetview.api
import google_streetview.helpers
import requests
import json
from datetime import datetime
from os_stuff import make_dir, rename_file, get_API_key
from item_detector import isolate_from_image
import shutil
import requests

key = get_API_key('maps_key')


def download_streetview_image(location):
    '''
    gets the streetview images of a provided location
    need to take 4 images for each view to get 360 degree perspective
    images are ordered by location. 5 requests to api each run
    '''
    dt = str(datetime.now())
    path_name = location.replace(',', '_')  # dir where data will be stored
    path = './streetview_data/' + location
    make_dir(path)

    # url for getting images
    url = 'https://maps.googleapis.com/maps/api/streetview?'

    # get 4 images since each view is by default 90 degree fov
    for i, direction in enumerate(['north', 'east', 'south', 'west']):
        request = requests.get(url + 'size=640x640' + '&location=' +
                               location + '&heading=' + str(i * 90) + '&key=' + key, stream=True)
        full_path = path + '/' + direction + '.jpg'
        process_image_request(full_path, request)
    process_metadata_request(location, path, dt)


def process_image_request(path, request):
    '''
    takes in a HTTPS request and downloads the image to the specified path.
    '''
    if request.status_code == 200:
        with open(path, 'wb') as out_file:
            shutil.copyfileobj(request.raw, out_file)
    else:
        print('error code ', request.status_code)


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
    with open(full_path, 'w') as fp:
        json.dump(results_metadata, fp)


def get_map(location):
    pass


def get_location(query):
    '''
    gets locations from user input
    returns a list of locations with metadata of each location
    '''
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    query_requests = requests.get(url + 'query=' + query + '&key=' + key)
    json_results = query_requests.json()

    results = json_results['results']
    locations = []
    for i in range(len(results)):
        lat = results[i]['geometry']['location']['lat']
        lng = results[i]['geometry']['location']['lng']
        locations.append(str(lat) + ',' + str(lng))
    return [locations, results]

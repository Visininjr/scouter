# author: Joshua Ren
# github: https://github.com/visininjr/
import google_streetview.api
import google_streetview.helpers
import requests
import json
from datetime import datetime
from os_stuff import make_dir, rename_file, get_API_key
from item_detector import isolate_from_image

key = get_API_key('maps_key')


def download_streetview_image(location):
    '''
    gets the streetview images of a provided location
    need to take 2 images for each view to get 360 degree perspective.
    images are ordered by datetime
    '''
    # for dev purposes
    # make program wait to avoid unnecessary downloads
    input('Press enter to download image...')

    dt = str(datetime.now()).replace(' ', '_')
    path = './data/' + dt
    make_dir(path)

    params_north = [{
        'size': '640x640',  # max 640x640 pixels
        'location': location,  # 'latitude','longitude'
        'heading': '0',
        'pitch': '0',
        'key': key
    }]
    params_south = [{
        'size': '640x640',
        'location': location,
        'heading': '180',
        'pitch': '0',
        'key': key
    }]
    for i, params in enumerate([('north', params_north), ('south', params_south)]):
        results = google_streetview.api.results(params[1])

        # Download images to specified dir
        results.save_links('./data/' + dt + '/links.txt')
        results.download_links('./data/' + dt)

        old_name = path + '/gsv_0.jpg'  # name from download is always gsv_0.jpg
        new_name = path + '/' + params[0] + '.jpg'
        # change name to avoid overwriting file
        rename_file(old_name, new_name)


def get_map(location):
    pass


def get_location(query):
    '''
    gets locations from user input
    returns a list of locations with metadata of each location
    '''
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
    query_requests = requests.get(url + 'query=' + query + '&key=' + key)
    json_requests = query_requests.json()

    results = json_requests['results']
    locations = []
    for i in range(len(results)):
        lat = results[i]['geometry']['location']['lat']
        lng = results[i]['geometry']['location']['lng']
        locations.append(str(lat) + ',' + str(lng))
    return [locations, results]

# author: Joshua Ren
# github: https://github.com/visininjr/
from streetview import save_streetview_image, get_location, process_image_request, lat_lng_numify, lat_lng_stringify
from mongodb import My_MongoDB
from os_stuff import get_API_key
import cv2
import requests
import math
import random

KEY = get_API_key('maps_key')
DEFAULT = 'object'


def pixels_to_coordinates(lat_center, lng_center, x, y, b, h, zoom):
    '''
    based on https://stackoverflow.com/questions/47106276/converting-pixels-to-latlng-coordinates-from-google-static-image
    function that converts the y, x pixel coordinates of a map image
    to the respective latitude, longitude coordinates in the world
    returns latitude, longitude coordinates of a point in a map image
    '''
    parallel_multiplier = math.cos(lat_center * math.pi / 180)
    degrees_X = 360 / math.pow(2, int(zoom) + 8)
    degrees_Y = 360 / math.pow(2, int(zoom) + 8) * parallel_multiplier
    point_lat = lat_center - degrees_Y * (y - h / 2)
    point_lng = lng_center + degrees_X * (x - b / 2)
    return (point_lat, point_lng)


def coordinates_to_pixels(lat_center, lng_center, lat, lng, b, h, zoom):
    '''
    based on https://stackoverflow.com/questions/47106276/converting-pixels-to-latlng-coordinates-from-google-static-image
    function that converts the latitude, longitude coordinates in the world
    to the respective y, x pixel coordinates in a static map image
    returns y,x coordinates of a point in in the world
    '''
    parallel_multiplier = math.cos(lat_center * math.pi / 180)
    degrees_X = 360 / math.pow(2, int(zoom) + 8)
    degrees_Y = 360 / math.pow(2, int(zoom) + 8) * parallel_multiplier
    y = h / 2 - (lat - lat_center) / degrees_Y
    x = b / 2 + (lng - lng_center) / degrees_X
    return (int(y), int(x))  # pixels must be integers


def get_map_corners(lat, lng, zoom, b, h):
    '''
    formula to get the corner coordinates of a map image
    returns tuples of corner coordinates of current map: nw, ne, sw, se
    '''
    ret = []
    nw = (0, 0)
    ne = (b, 0)
    sw = (0, h)
    se = (b, h)
    for x, y in [nw, ne, sw, se]:
        point_lat, point_lng = pixels_to_coordinates(
            lat, lng, x, y, b, h, zoom)
        ret.append((point_lat, point_lng))
    return ret


def get_color(frequency):
    '''
    returns a tuple of BGR (blue, green, red) value
    from frequency of some object
    '''
    return (0, 0, 255)


def add_n_points(n, map_corners, type, base_location):
    '''
    returns ids of n random points inserted into the db
    '''
    db = My_MongoDB()
    ret = []
    if not db.get_documents(DEFAULT, 'location', base_location):
        ids = save_streetview_image(base_location)
        ret += ids

    i = 0
    while i < n:
        lat = round(random.uniform(map_corners[0][0], map_corners[2][0]), 7)
        lng = round(random.uniform(map_corners[0][1], map_corners[1][1]), 7)
        location = lat_lng_stringify(lat, lng)
        # if this point already exists in the db we want reselect a random point
        if db.get_documents(DEFAULT, 'location', location):
            continue
        ids = save_streetview_image(location)
        ret += ids
        i = i + 1 if ids else i
    return ret


def get_map(location, type=DEFAULT, num_points=0, zoom='14', b='640', h='640'):
    '''
    return a static map of a given location
    with points detected objects of some type
    '''

    url = "https://maps.googleapis.com/maps/api/staticmap?"
    request = requests.get(url + 'size=' + b + 'x' + h + '&center=' +
                           location + '&zoom=' + zoom + '&key=' + KEY, stream=True)
    map = process_image_request(request)
    db = My_MongoDB()
    b = int(b)
    h = int(h)
    ids = []

    def add_heat_layer(map, num_points):  # intensity related to object count TODO
        '''
        returns map with location based object frequency added
        '''
        lat_center, lng_center = lat_lng_numify(location)

        if num_points:
            print('adding ' + str(num_points) + ' points...')
            corners = get_map_corners(
                lat_center, lng_center, zoom, b, h)
            add_n_points(num_points, corners, type, location)

        radius = 4
        thickness = -1  # fills circle
        documents = db.get_collection(type)
        for document in documents:
            lat, lng = lat_lng_numify(document['location'])
            y_x_center = coordinates_to_pixels(
                lat_center, lng_center, lat, lng, float(b), float(h), zoom)
            if (y_x_center[0] >= 0 and y_x_center[0] <= h) and (y_x_center[1] >= 0 and y_x_center[1] <= h):
                frequency = document['object_count']
                color = get_color(frequency)
                map = cv2.circle(map, y_x_center, radius, color, thickness)
                ids.append(document['_id'])
        return [map, ids]

    return add_heat_layer(map, num_points)

# author: Joshua Ren
# github: https://github.com/visininjr/
from streetview import get_location, process_image_request, lat_lng_intify
from mongodb import My_MongoDB
from os_stuff import get_API_key
import cv2
import requests
import math

KEY = get_API_key('maps_key')


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
    return (y, x)


def get_map_corners(lat, lng, zoom, b=640, h=640):
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


def get_map(location, zoom='16', b='640', h='640'):
    '''
    return a static map of a given location
    '''
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    request = requests.get(url + 'size=' + b + 'x' + h +
                           '&center=' + location + '&zoom=' + zoom + '&key=' + KEY, stream=True)
    map = process_image_request(request)
    lat_center, lng_center = lat_lng_intify(location)
    # coordinates will be read from db TODO

    def add_dots(map, coordinates):  # intensity related to object count TODO
        '''
        returns map with location based object frequency added
        '''
        radius = 4
        thickness = -1  # fills circle
        color = (0, 0, 255)
        for lat, lng in coordinates:
            y, x = coordinates_to_pixels(
                lat_center, lng_center, lat, lng, float(b), float(h), zoom)
            y_x_center = (int(y), int(x))
            map = cv2.circle(map, y_x_center, radius, color, thickness)
        return map

    return add_dots(map, [(37.7596093, -122.4851074)])

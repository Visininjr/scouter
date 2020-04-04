# author: Joshua Ren
# github: https://github.com/visininjr/
from streetview import get_location, process_image_request, lat_lng_intify
from mongodb import My_MongoDB
from os_stuff import get_API_key
import cv2
import requests
import math

key = get_API_key('maps_key')


def get_map(location, zoom='16'):
    '''
    return a static map of a given location
    '''
    b = h = 640
    lat, lng = lat_lng_intify(location)
    url = "https://maps.googleapis.com/maps/api/staticmap?"
    request = requests.get(url + 'size=' + str(b) + 'x' + str(h) +
                           '&center=' + location + '&zoom=' + zoom + '&key=' + key, stream=True)
    return process_image_request(request)


def pixels_to_coordinates(lat, lng, x, y, b, h, zoom):
    parallel_multiplier = math.cos(lat * math.pi / 180)
    degrees_X = 360 / math.pow(2, int(zoom) + 8)
    degrees_Y = 360 / math.pow(2, int(zoom) + 8) * parallel_multiplier
    point_lat = lat - degrees_Y * (y - h / 2)
    point_lng = lng + degrees_X * (x - b / 2)
    return (point_lat, point_lng)

# def coordinates_to_pixels TODO


def get_map_corners(lat, lng, b=640, h=640, zoom='16'):
    '''
    formula to get the corner coordinates of a map image
    based from stackoverflow post on getting coordinates from an image
    https://stackoverflow.com/questions/47106276/converting-pixels-to-latlng-coordinates-from-google-static-image
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

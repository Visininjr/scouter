import google_streetview.api
import google_streetview.helpers
from datetime import datetime
from os_stuff import make_dir
import os


def get_streetview_image(location):
    """
    gets the streetview images of a provided location
    need to take 2 images for each view to get 360 degree perspective.
    rename object after making it.
    """
    dt = str(datetime.now()).replace(' ', '_')
    path = './data/' + dt
    make_dir(path)

    params_north = [{
        'size': '640x640',  # max 640x640 pixels
        'location': location,
        'heading': '0',
        'pitch': '0',
        'key': 'AIzaSyCXHmcksWqO3g5RyIufIcFhaYfbsDQLqyM'
    }]
    params_south = [{
        'size': '640x640',  # max 640x640 pixels
        'location': location,
        'heading': '180',
        'pitch': '0',
        'key': 'AIzaSyCXHmcksWqO3g5RyIufIcFhaYfbsDQLqyM'
    }]
    for i, params in enumerate([params_north, params_south]):
        results = google_streetview.api.results(params)

        # Download images to specified dir
        results.save_links('./data/' + dt + '/links.txt')
        results.download_links('./data/' + dt)
        os.rename(path + '/gsv_0.jpg', path + '/' + str(i) + '.jpg')


get_streetview_image('42.3275364,-71.1420638')

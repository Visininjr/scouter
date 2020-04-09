# author: Joshua Ren
# github: https://github.com/visininjr/
from item_detector import detect_objects, isolate_from_image, isolate_from_video, get_image_with_boxes
from streetview import get_location
from os_stuff import file_exists
from map import get_map
from mongodb import My_MongoDB
import numpy as np
import sys
import cv2
import getopt

# picture from http://www.ascii-art.de/ascii/def/dragon_ball.txt
HEADER = ['Welcome to ', '''
                   `\\-.   `
                      \\ `.  `
                       \\  \\ |
              __.._    |   \\.       SCOUTER (IT'S OVER 9000)
       ..---~~     ~ . |    Y
         ~-.          `|    |
            `.               `~~--.
              \\                    ~.
               \\                     \\__. . -- -  .
         .-~~~~~      ,    ,            ~~~~~~---...._
      .-~___        ,'/  ,'/ ,'\\          __...---~~~
            ~-.    /._\\_( ,(/_. 7,-.    ~~---...__
           _...>- |''6=`_/'6'~    9)    ___...--~~~
            ~~--._\\`--') `---'   |'  _..--~~~
                  ~\\   /_        /`-.--~~
                    `.  ---    .'   \\_
                      `. ___.-'     | ~-.,-------._
                  ..._../~~   ./       .-'    .-~~~-.
            ,--~~~ ,'...\\` _./.----~~.'/    /'       `-
        _.-(      |\\    `/~ _____..-'/    /      _.-~~`.
       /   |     /. ^---~~~~       ' /    /     ,'  ~.   \\
      (    /    (  .           _ ' /'    /    ,/      \\   )
      (`. |    `\\   - - - - ~    /'      (   /         .  |
       \\.\\|      \\             /'        \\  |`.           /
       /.'\\       `\\         /'           ~-\\         .  /\\
      /,   (        `\\     /'                `.___..-      \\
     | |    \\         `\\_/'                  //      \\.     |
      | |     |                             /' |       |     |
''', 'detector (image) :)', 'detector (video/camera) :)', 'mapper :)']
DEFAULT = 'object'


def main():
    '''
    option flags:
    -1: isolate and write images of an input
    -2: isolate images of an input type in real time or video
    -3: write streetview images from a latitude/longitude

    -s: search for only a specific type of object
    -h: for more accurate, but slower detection
    '''
    print(HEADER[1])
    (options, args) = getopt.getopt(sys.argv[1:], '1234sh')
    if ('-1', '') in options:  # isolate and write images of an input
        print(HEADER[0] + HEADER[2])
        type = DEFAULT
        image_name = input('Please provide a specific image.\n')
        image = cv2.imread(image_name)
        if np.shape(image) == ():  # if the image doesn't exist
            print('image not found... :(')
            exit()
        results = detect_objects(image)
        if ('-s', '') in options:
            type = input(
                'Please provide an object type. Types can be found in labels.txt.\n')
            # reference labels.txt for valid types
            results = detect_objects(image, type)
        if not results[1]:  # if no results were found, then bboxes will be empty
            print('no objects of type ' + type + ' found. :(')
        # TODO insert to DB?
        image_with_boxes = get_image_with_boxes(
            np.copy(image), results[1], results[2], results[3])
        cv2.imshow('image', image_with_boxes)  # show image with boxes
        cv2.waitKey(0)

        isolated_images = isolate_from_image(
            image, results[1], results[2], results[3])
        for im_set in isolated_images:  # show all isolated images as well
            cv2.imshow(im_set[1] + ' ' + str(im_set[2]), im_set[0])
            cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif ('-2', '') in options:  # isolate images of an input type in real time or video
        print(HEADER[0] + HEADER[3])
        use_small_model = (False if ('-h', '') in options else True)
        video_name = input(
            'Please provide a video file path (default is real time video).\n')
        if not file_exists(video_name):
            print('Video not found. Real time video will be used instead...')
            video_name = 0  # 0 is the analogous to real time input
        if ('-s', '') in options:
            type = input(
                'Please provide an object type. Types can be found in labels.txt.\n')
            isolate_from_video(video_name, type, use_small_model)
        else:
            isolate_from_video(video_name, use_small_model=use_small_model)
    elif ('-3', '') in options:  # write streetview images from a latitude/longitude
        print(HEADER[0] + HEADER[4])
        query = input(
            'Please enter the name of a location or input a location in the following format: latitude,longitude.\n').replace('/', ',')
        search_type = ''
        if ('-s', '') in options:
            search_type = input(
                'Please provide an object type. Types can be found in labels.txt.\n')
        num_points_str = input(
            'Please provide number of points to add. Enter \'0\' if you don\'t want to add any.\n')
        # '' converts to 0
        num_points = int(num_points_str) if num_points_str else 0
        db = My_MongoDB()
        locations = (get_location(query))[0]
        type = search_type if search_type else DEFAULT
        for location in locations:
            map_set = get_map(location, type, num_points)
            map = map_set[0]
            ids = map_set[1]
            print('Map ready!  Displaying now...')
            cv2.imshow(query, map)
            cv2.waitKey(0)
            for id in ids:
                cur_doc = (db.get_documents(type, '_id', id))[0]
                cur_type = cur_doc['type']
                cur_image = cur_doc['image']
                cur_loc = cur_doc['location']
                cur_direction = cur_doc['direction']
                cur_title = cur_type + ' ' + cur_loc + ' ' + cur_direction
                cv2.imshow(cur_title, cur_image)
                cv2.waitKey(0)
            cv2.destroyAllWindows()

    else:
        print('Sorry, please input an option flag... (options in README.md)')
        exit()


if __name__ == '__main__':
    main()

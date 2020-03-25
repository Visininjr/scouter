# author: Joshua Ren
# website: https://renj41.wixsite.com/renj
# github: https://github.com/visininjr/
from item_detector import detect_objects, isolate_from_image, isolate_from_video, plot_image
from streetview import download_streetview_image
from os_stuff import file_exists
import numpy as np
import sys
import cv2
import getopt

# picture from http://www.ascii-art.de/ascii/def/dragon_ball.txt
HEADER = ["""Welcome to:
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
           _...>- |""6=`_/"6"~    9)    ___...--~~~
            ~~--._\\`--') `---'   |'  _..--~~~
                  ~\\   /_        /`-.--~~
                    `.  ---    .'   \\_
                      `. ___.-'     | ~-.,-------._
                  ..._../~~   ./       .-'    .-~~~-.
            ,--~~~ ,'...\\` _./.----~~.'/    /'       `-
        _.-(      |\\    `/~ _____..-' /    /      _.-~~`.
       /   |     /. ^---~~~~       ' /    /     ,'  ~.   \\
      (    /    (  .           _ ' /'    /    ,/      \\   )
      (`. |     `\\   - - - - ~   /'      (   /         .  |
       \\.\\|     \\            /'        \\  |`.           /
       /.'\\      `\\         /'           ~-\\         .  /\\
      /,   (        `\\     /'                `.___..-      \\
     | |    \\         `\\_/'                  //      \\.     |
     | |     |                              /' |       |     |
"""]


def main():
    """
    option flags:
    -1: isolate and write images of an input
    -2: isolate images of an input type in real time or video
    -3: write streetview images from a latitude/longitude

    -s: search for only a specific type of object
    -h: for more accurate, but slower detection
    """
    print(HEADER[0])
    (options, args) = getopt.getopt(sys.argv[1:], '1234sh')
    if ('-1', '') in options:  # isolate and write images of an input
        image_name = input('Please provide a specific image.\n> ')
        image = cv2.imread(image_name)
        if np.shape(image) == ():  # image.shape() errors when image is None
            print('image not found... :(')
            exit()
        results = (detect_objects(image) if ('-h', '')
                   in options else detect_objects(image, use_small_model=True))
        if ('-s', '') in options:
            type = input(
                'Please provide an object type. Types can be found in labels.txt.\n> ')
            # reference labels.txt for valid types
            results = (detect_objects(image, type) if (
                '-h', '') in options else detect_objects(image, type, use_small_model=True))
        if not results[1]:  # if no results were found, then bboxes will be empty
            print('no objects of that type found. :(')
            exit()
        isolate_from_image(
            image, results[0], results[1], results[2], results[3])
    elif ('-2', '') in options:  # isolate images of an input type in real time or video
        use_small_model = (False if ('-h', '') in options else True)
        video_name = input(
            'Please provide a video file path (default is real time video).\n> ')
        if not file_exists(video_name):
            print('Video not found. Real time video will be used instead...')
            video_name = 0  # 0 is the analogous to real time input
        if ('-s', '') in options:
            type = input(
                'Please provide an object type. Types can be found in labels.txt.\n> ')
            isolate_from_video(video_name, type, use_small_model)
        else:
            isolate_from_video(video_name, use_small_model=use_small_model)
    elif ('-3', '') in options:  # write streetview images from a latitude/longitude
        location = input(
            'Please input latitude,longitude coordinates in the following format: \'latitude,longitude\'.')
        location = location.replace(' ', '_').replace('/', ',')
        download_streetview_image(location)

    else:
        print('Sorry, please input an option flag... (options in README.md)')
        exit()


if __name__ == '__main__':
    main()

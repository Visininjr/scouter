from os_stuff import make_file_name
from item_detector import detect_objects, detect_specific, plot_image
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from datetime import datetime


def isolate_from_image(image, type, borders, labels):
    """
    isolates objects in an image.
    writes isolated images to specific directories
    """
    for border_set in borders:
        # ./people/current_date_time.png
        dt = str(datetime.now()).replace(' ', '_')
        path = make_file_name(type, dt)

        # border_set format: [x1, y1, x2, y2]
        x1 = border_set[0]
        x2 = border_set[2]
        y1 = border_set[1]
        y2 = border_set[3]
        isolated_image = image[y1:y2, x1:x2]  # display default: [y, x]

        cv2.imshow(type + ' ' + dt, isolated_image)
        cv2.imwrite(path, isolated_image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    image = cv2.imread('./images/avengers.jpg')
    # reference labels.txt for valid types
    people_borders = detect_specific(image, 'person')
    if not people_borders:
        exit()
    isolate_from_image(
        image, people_borders[0], people_borders[1], people_borders[2])

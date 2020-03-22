from item_detector import detect_objects, detect_people, plot_image
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from datetime import datetime


def isolate_from_image(type, image, borders, labels):
    """
    isolates objects in an image.

    """
    for i, border_set in enumerate(borders):
        # ./people/current_date_time.png
        dt = str(datetime.now()).replace(' ', '_')
        path = './' + type + '/' + dt + '.png'
        print(path)

        # border_set format: [x1, y1, x2, y2]
        x1 = border_set[0]
        x2 = border_set[2]
        y1 = border_set[1]
        y2 = border_set[3]
        new_image = image[y1:y2, x1:x2]  # display default: [y, x]

        cv2.imshow("cropped", new_image)
        cv2.waitKey(0)


def read_from_camera():
    pass


if __name__ == '__main__':
    image = cv2.imread('./images/avengers.jpg')
    people = detect_people(image)
    if not people:
        exit()
    isolate_from_image('people', image, people[0], people[1])

import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox


def detect_objects(im):  # detect objects in an image
    image = cv2.imread(im)
    bbox, label, conf = cv.detect_common_objects(image)
    return (bbox, label, conf)


def plot_image(im, bbox, label, conf):  # plots images with detection
    image = cv2.imread(im)
    output_image = draw_bbox(image, bbox, label, conf)
    plt.imshow(output_image)
    plt.show()

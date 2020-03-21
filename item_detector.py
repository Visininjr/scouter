import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox


def detect_objects(image):  # detect objects in an image
    bboxes, labels, confs = cv.detect_common_objects(image, enable_gpu=True)
    return (bboxes, labels, confs)


def plot_image(image, bbox, label, conf):  # plots images with detection
    output_image = draw_bbox(image, bbox, label, conf)
    plt.imshow(output_image)
    plt.show()

import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox


def detect_objects(image):
    """
    detect objects in an image using cvlib.
    returns borders (boxes) of objects, labels, and confidences of assignment
    """
    bboxes, labels, confs = cv.detect_common_objects(image)
    return [bboxes, labels, confs]


def detect_specific(image, type):
    """
    detect all instances of specific type of an object in an image.
    returns name of type, borders (boxes) of a specific object type,
    labels, and confidences of assignment
    """
    bboxes, labels, confs = detect_objects(image)
    ret_bboxes = []
    ret_labels = []
    ret_confs = []
    for i, label in enumerate(labels):
        if label == type:
            ret_bboxes.append(bboxes[i])
            ret_labels.append(labels[i])
            ret_confs.append(confs[i])
    if not ret_bboxes:
        print('no objects of that type found.')
        return []
    return [type, ret_bboxes, ret_labels, ret_confs]


def plot_image(image, bbox, label, conf):
    """
    plots detected images using matplotlib.
    """
    output_image = draw_bbox(image, bbox, label, conf)
    plt.imshow(output_image)
    plt.show()

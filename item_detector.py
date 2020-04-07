# author: Joshua Ren
# github: https://github.com/visininjr/
from os_stuff import make_file_name, get_current_dt
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox

DEFAULT = 'object'


def detect_objects(image, type=DEFAULT, use_small_model=False):
    '''
    detect objects in an image using cvlib.
    returns type of objects (default is DEFAULT),
    borders (boxes) of objects, labels, and confidences of assignment.
    '''
    bboxes, labels, confs = (cv.detect_common_objects(
        image, confidence=0.25, model='yolov3-tiny') if use_small_model else cv.detect_common_objects(image))
    if type == DEFAULT:
        return ([type, bboxes, labels, confs])
    else:  # we filter a objects of a specific result type
        ret_bboxes = []
        ret_labels = []
        ret_confs = []
        for i, label in enumerate(labels):
            if label == type:
                ret_bboxes.append(bboxes[i])
                ret_labels.append(labels[i])
                ret_confs.append(confs[i])
        return [type, ret_bboxes, ret_labels, ret_confs]


def get_image_with_boxes(image, bbox, label, conf, write_conf_in_image=True):
    '''
    returns image with boxes around each detected object in an image
    '''
    return draw_bbox(image, bbox, label, conf, write_conf=write_conf_in_image)


def isolate_from_image(image, borders, labels, confs):
    '''
    isolates all objects in an image
    returns list of isolated images with their labels and confidences of assignment
    '''
    ret = []
    for i, border_set in enumerate(borders):
        cur_label = labels[i]
        cur_conf = confs[i]

        # border_set format: [x1, y1, x2, y2]
        x1 = border_set[0]
        x2 = border_set[2]
        y1 = border_set[1]
        y2 = border_set[3]
        isolated_image = image[y1:y2, x1:x2]  # display default: [y, x]
        ret.append([isolated_image, cur_label, cur_conf])
    return ret


def isolate_from_video(video, type=DEFAULT, use_small_model=True):
    '''
    isolates objects in real time using device camera and cv2.VidoCapture
    object types and model are adjustable in scouter.py
    '''
    camera = cv2.VideoCapture(video)
    while camera.isOpened():  # stream live video
        status, frame = camera.read()
        # use small model to improve framerate
        type, bbox, label, conf = detect_objects(frame, type, use_small_model)
        out = draw_bbox(frame, bbox, label, conf, write_conf=True)
        cv2.imshow('Real-time Detection of ' + type, out)
        wait_time = (200 if not use_small_model else 1)
        if cv2.waitKey(wait_time) & 0xFF == ord('q'):  # press 'q' to stop
            break

    camera.release()
    cv2.destroyAllWindows()

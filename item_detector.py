# author: Joshua Ren
# github: https://github.com/visininjr/
from os_stuff import make_file_name
import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from datetime import datetime
from cvlib.object_detection import draw_bbox


def detect_objects(image, type='object', use_small_model=False):
    '''
    detect objects in an image using cvlib.
    returns type of objects (default is 'object'),
    borders (boxes) of objects, labels, and confidences of assignment.
    '''
    bboxes, labels, confs = (cv.detect_common_objects(
        image, confidence=0.25, model='yolov3-tiny') if use_small_model else cv.detect_common_objects(image))
    if type == 'object':
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


def isolate_from_image(image, type, borders, labels, confs):
    '''
    isolates all objects in an image one by one.
    writes isolated images to specific dir under object type dir.
    confidence of assignment is in file name.
    return number of objects of specificied type found.
    '''
    for i, border_set in enumerate(borders):
        # file format:
        # ./people/confidence_current_date_time.png
        dt = str(datetime.now())
        cur_conf = str(round(confs[i], 4))
        # confidence is rounded to 4 significant figures for readability
        file_name = (cur_conf + '_' + dt).replace(' ', '_')
        path = make_file_name(type, file_name)

        # border_set format: [x1, y1, x2, y2]
        x1 = border_set[0]
        x2 = border_set[2]
        y1 = border_set[1]
        y2 = border_set[3]
        isolated_image = image[y1:y2, x1:x2]  # display default: [y, x]

        cv2.imshow(type + ': ' + file_name, isolated_image)
        cv2.imwrite(path, isolated_image)
        cv2.waitKey(0)
    cv2.destroyAllWindows()
    return len(borders)


def isolate_from_video(video, type='object', use_small_model=True):
    '''
    isolates objects in real time using device camera and cv2.VidoCapture.
    object types and model are adjustable in scouter.py.
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


def plot_image(image, bbox, label, conf):
    '''
    plots detected images using matplotlib.
    '''
    output_image = draw_bbox(image, bbox, label, conf, write_conf=True)
    plt.imshow(output_image)
    plt.show()

from item_detector import detect_objects
from item_detector import plot_image
import cv2


if __name__ == '__main__':
    im = './images/matrix.jpg'
    image = cv2.imread(im)
    objects = detect_objects(image)
    plot_image(image, objects[0], objects[1], objects[2])

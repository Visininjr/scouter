import os


def make_file_name(type, dt):
    """
    creates a file name for detected objects and classifies them.
    ./person/current_date_time.png
    """
    if not os.path.exists(type):
        os.makedirs(type)
    path = './' + type + '/' + dt + '.png'
    return path


def make_dir(dir_name):
    """
    creates a directory.
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

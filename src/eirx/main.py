import sys
import os
from PIL import Image
from eirx.api import trans_image
import imghdr
import ntpath


def convert():
    if len(sys.argv) != 4:
        print >> sys.stderr, 'Usage:'
        print >> sys.stderr, '  erix MODE SRC DEST'
        return sys.exit(1)

    mode = sys.argv[1]
    src = sys.argv[2]
    dest = sys.argv[3]

    if os.path.isfile(src) and os.path.isfile(dest):
        resize_routine(mode, src, dest)
    elif os.path.isdir(src) and os.path.isabs(dest):
        images_paths = get_images_paths(src)
        if 0 == len(images_paths):
            return

        if not os.path.isdir(dest):
            os.makedirs(dest)

        for img in images_paths:
            dest_img_path = os.path.join(dest, ntpath.basename(img))
            resize_routine(mode, img, dest_img_path)
    else:
        print >> sys.stderr, 'Usage:'
        print >> sys.stderr, '  erix MODE SRC DEST'
        return sys.exit(1)


def resize_routine(mode, src, dest):
    im = Image.open(src)
    fmt = im.format
    trans_image(im, mode).save(dest, format=fmt)


def get_images_paths(src):
    """ Check if folder contains images and return their paths
    :param src: path to the folder
    :return: list with the strings
    """
    if not os.path.isdir(src):
        return list()

    images = list()
    entries = os.listdir(src)
    for entry in entries:
        file_path = os.path.join(src, entry)
        if os.path.isfile(file_path) and imghdr.what(file_path):
            images.append(file_path)

    return images


def view():
    if len(sys.argv) != 3:
        print >> sys.stderr, 'Usage:'
        print >> sys.stderr, '  erixv MODE SRC'
        return sys.exit(1)

    mode = sys.argv[1]
    src = sys.argv[2]

    trans_image(Image.open(src), mode).show()

if __name__ == '__main__':
    convert()

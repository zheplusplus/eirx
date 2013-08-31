import sys
import PIL.Image
from api import trans_image


def convert():
    if len(sys.argv) != 4:
        print >> sys.stderr, 'Usage:'
        print >> sys.stderr, '  erix MODE SRC DEST'
        return sys.exit(1)

    mode = sys.argv[1]
    src = sys.argv[2]
    dest = sys.argv[3]

    im = PIL.Image.open(src)
    fmt = im.format
    trans_image(im, mode).save(dest, format=fmt)


def view():
    if len(sys.argv) != 3:
        print >> sys.stderr, 'Usage:'
        print >> sys.stderr, '  erixv MODE SRC'
        return sys.exit(1)

    mode = sys.argv[1]
    src = sys.argv[2]

    trans_image(PIL.Image.open(src), mode).show()

if __name__ == '__main__':
    view()

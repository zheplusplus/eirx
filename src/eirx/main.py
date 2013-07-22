import sys
import PIL.Image
from parse import parse, adjust


def convert():
    if len(sys.argv) != 4:
        print >> sys.stderr, 'Usage:'
        print >> sys.stderr, '  erix MODE SRC DEST'
        return sys.exit(1)

    mode = sys.argv[1]
    src = sys.argv[2]
    dest = sys.argv[3]

    args = parse(mode)
    im = PIL.Image.open(src)
    fmt = im.format
    adjust(im, **args).save(dest, format=fmt)


def view():
    if len(sys.argv) != 3:
        print >> sys.stderr, 'Usage:'
        print >> sys.stderr, '  erixv MODE SRC'
        return sys.exit(1)

    mode = sys.argv[1]
    src = sys.argv[2]

    args = parse(mode)
    adjust(PIL.Image.open(src), **args).show()

if __name__ == '__main__':
    view()

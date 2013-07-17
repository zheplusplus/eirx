def main():
    import sys
    import PIL.Image
    from eirx.parse import parse

    if len(sys.argv) != 4:
        print >> sys.stderr, 'Usage:'
        print >> sys.stderr, '  erix MODE SRC DEST'
        return sys.exit(1)

    mode = sys.argv[1]
    src = sys.argv[2]
    dest = sys.argv[3]

    r = parse(mode)
    if r is None:
        print >> sys.stderr, 'Unknown mode.'
        return sys.exit(1)
    args = r[0]
    adjust = r[1]
    im = PIL.Image.open(src)
    fmt = im.format
    adjust(im, **args).save(dest, format=fmt)

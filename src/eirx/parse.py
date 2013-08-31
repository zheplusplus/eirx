import re

WHITE_RGBA = (255, 255, 255)
BLACK_RGBA = (0, 0, 0)


def _get_size(size):
    for m in _SIZE_RE:
        match = m[0].match(size)
        if match:
            return m[1](match.groupdict())
    raise ValueError('Invalid size')


def _get_RGBA(opt, index):
    if len(opt) > index + 6:
        return tuple(int(opt[i * 2 + 3: i * 2 + 5], 16) for i in xrange(3))
    raise ValueError('Invalid color format, not xRRGGBB')


def _get_options(opt):
    def not_keep_aspect_ratio(opt_result, opt_string, index):
        opt_result['adjh'] = False
        opt_result['adjw'] = False
        return 0

    def crop(opt_result, opt_string, index):
        opt_result['crop'] = True
        return 0

    def frame(opt_result, opt_string, index):
        opt_result['frame'] = True
        return 0

    def window(opt_result, opt_string, index):
        opt_result['window'] = True
        return 0

    def fcolor(opt_result, opt_string, index):
        if opt_string[index] == 'w':
            opt_result['bgc'] = WHITE_RGBA
            return 1
        elif opt_string[index] == 'b':
            opt_result['bgc'] = BLACK_RGBA
            return 1
        elif opt_string[index] == 'x':
            opt_result['bgc'] = _get_RGBA(opt_string, index)
            return 7
        raise ValueError('Invalid color format')

    opt_result = dict()
    opt_map = dict(
        a=not_keep_aspect_ratio,
        c=crop,
        f=frame,
        w=window,
        F=fcolor,
    )
    i = 0
    while i < len(opt):
        try:
            i += opt_map[opt[i]](opt_result, opt, i + 1)
        except LookupError:
            raise ValueError('Invalid option')
        i += 1
    return opt_result


def adjust(img, w=0, h=0, adjust_width=False, adjust_height=False, crop=False,
           frame=False, bgc=None):
    if adjust_width:
        w = w or int(h * img.size[0] / img.size[1])
    if adjust_height:
        h = h or int(w * img.size[1] / img.size[0])
    if w == 0:
        w = img.size[0]
    if h == 0:
        h = img.size[1]
    if frame:
        img_w = img.size[0]
        img_h = img.size[1]
        offset_x = 0
        offset_y = 0
        resize_w = w
        resize_h = h
        if img_w * h > img_h * w:
            resize_h = int(img_h * w / img_w)
            offset_y = (h - resize_h) / 2
        else:
            resize_w = int(img_w * h / img_h)
            offset_x = (w - resize_w) / 2
        framed = img.resize((resize_w, resize_h), PIL.Image.ANTIALIAS)
        if offset_x == 0 and offset_y == 0:
            return framed
        bg = PIL.Image.new('RGBA', (w, h), bgc or WHITE_RGBA)
        bg.paste(framed, (offset_x, offset_y))
        return bg
    if crop:
        offset_x = max((w - img.size[0]) / 2, 0)
        offset_y = max((h - img.size[1]) / 2, 0)
        crop_x = max((img.size[0] - w) / 2, 0)
        crop_y = max((img.size[1] - h) / 2, 0)
        crop_w = min(w, img.size[0])
        crop_h = min(h, img.size[1])
        cropped = img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
        if offset_x == 0 and offset_y == 0:
            return cropped
        bg = PIL.Image.new('RGBA', (w, h), bgc or WHITE_RGBA)
        bg.paste(cropped, (offset_x, offset_y))
        return bg
    return img.resize((w, h), PIL.Image.ANTIALIAS)


def parse(mode):
    parts = mode.split('-')
    args = _get_size(parts[0])
    if 1 < len(parts):
        for opt, value in _get_options(parts[1]).iteritems():
            args[opt] = value
    return args

_SIZE_RE = (
    (re.compile('^w(?P<w>[0-9]+)h(?P<h>[0-9]+)$'),
        lambda d: dict(w=int(d['w']), h=int(d['h']))),
    (re.compile('^w(?P<w>[0-9]+)$'),
        lambda d: dict(w=int(d['w']), adjh=True)),
    (re.compile('^h(?P<h>[0-9]+)$'),
        lambda d: dict(h=int(d['h']), adjw=True)),
    (re.compile('^(?P<s>[0-9]+)$'),
        lambda d: dict(w=int(d['s']), h=int(d['s']), crop=True)),
)

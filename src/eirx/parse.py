import re
import PIL.Image

def _get_size(size):
    for m in _SIZE_RE:
        match = m[0].match(size)
        if match:
            return m[1](match.groupdict())
    raise ValueError('Invalid size')

def _get_options(opt):
    def not_keep_aspect_ratio(opt_result, opt_string, index):
        opt_result['adjust_height'] = False
        opt_result['adjust_width'] = False
        return 0

    def crop(opt_result, opt_string, index):
        opt_result['crop'] = True
        return 0

    opt_result = dict()
    opt_map = dict(
            a=not_keep_aspect_ratio,
            c=crop,
        )
    i = 0
    while i < len(opt):
        try:
            i += opt_map[opt[i]](opt_result, opt, i + 1)
        except LookupError:
            raise ValueError('Invalid option')
        i += 1
    return opt_result

WHITE_RGBA = (255, 255, 255, 0)
BLACK_RGBA = (0, 0, 0, 0)

def adjust(img, w=0, h=0, adjust_width=False, adjust_height=False, crop=False,
           bgc=None):
    if adjust_width:
        w = w or int(h * img.size[0] / img.size[1])
    if adjust_height:
        h = h or int(w * img.size[1] / img.size[0])
    if w == 0:
        w = img.size[0]
    if h == 0:
        h = img.size[1]
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
            lambda d: dict(w=int(d['w']), adjust_height=True)),
        (re.compile('^h(?P<h>[0-9]+)$'),
            lambda d: dict(h=int(d['h']), adjust_width=True)),
        (re.compile('^(?P<s>[0-9]+)$'),
            lambda d: dict(w=int(d['s']), h=int(d['s']), crop=True)),
    )

import re
import PIL.Image

def parse(mode):
    for m in _MODES:
        match = m[0].match(mode)
        if match:
            return match.groupdict(), m[1]
    return None

def resize(img, w, h):
    w = int(w)
    h = int(h)
    return img.resize((w, h), PIL.Image.ANTIALIAS)

def resize_w(img, w):
    w = int(w)
    return resize(img, w, int(w * img.size[1] / img.size[0]))

def resize_wabs(img, w):
    w = int(w)
    return resize(img, w, img.size[1])

def resize_h(img, h):
    h = int(h)
    return resize(img, int(h * img.size[0] / img.size[1]), h)

def resize_habs(img, h):
    h = int(h)
    return resize(img, img.size[0], h)

_MODES = (
        (re.compile('^w(?P<w>[0-9]+)h(?P<h>[0-9]+)$'), resize),
        (re.compile('^w(?P<w>[0-9]+)$'), resize_w),
        (re.compile('^w(?P<w>[0-9]+)a$'), resize_wabs),
        (re.compile('^h(?P<h>[0-9]+)$'), resize_h),
        (re.compile('^h(?P<h>[0-9]+)a$'), resize_habs),
    )

import PIL.Image
import PIL.ImageFilter
from eirx import parse
import operator


def decolor(im):
    g = im.split()[1]
    im = PIL.Image.merge('RGB', (g, g, g))
    return im

_filters_map = {
    'blur': lambda im: im.filter(PIL.ImageFilter.BLUR),
    'cntr': lambda im: im.filter(PIL.ImageFilter.CONTOUR),
    'edge': lambda im: im.filter(PIL.ImageFilter.FIND_EDGES),
    'dclr': decolor,
}


def _resize_fill(img, w, h, bgc, ratio_f, force_off_y=None):
    img_w = img.size[0]
    img_h = img.size[1]
    offset_x = 0
    offset_y = 0
    resize_w = w
    resize_h = h
    if ratio_f(img_w * h, img_h * w):
        resize_h = int(img_h * w / img_w)
        offset_y = (h - resize_h) / 2 if force_off_y is None else force_off_y
    else:
        resize_w = int(img_w * h / img_h)
        offset_x = (w - resize_w) / 2
    framed = img.resize((resize_w, resize_h), PIL.Image.ANTIALIAS)
    bg = PIL.Image.new('RGBA', (w, h), bgc or parse.WHITE_RGBA)
    bg.paste(framed, (offset_x, offset_y))
    return bg


def adjust(img, w=0, h=0, wma=0, hma=0, size_adj=False, bgc=None, **kwargs):
    if wma != 0:
        w = min(img.size[0], wma)
    if hma != 0:
        h = min(img.size[1], hma)
    if size_adj:
        w = w or int(h * img.size[0] / img.size[1])
        h = h or int(w * img.size[1] / img.size[0])
    if w == 0:
        w = img.size[0]
    if h == 0:
        h = img.size[1]
    if kwargs.get('filters'):
        for f in kwargs['filters']:
            img = _filters_map[f](img)
    if kwargs.get('frame'):
        return _resize_fill(img, w, h, bgc, operator.gt)
    if kwargs.get('top_crop'):
        return _resize_fill(img, w, h, bgc, operator.lt, force_off_y=0)
    if kwargs.get('crop'):
        return _resize_fill(img, w, h, bgc, operator.lt)
    if kwargs.get('window'):
        offset_x = max((w - img.size[0]) / 2, 0)
        offset_y = max((h - img.size[1]) / 2, 0)
        crop_x = max((img.size[0] - w) / 2, 0)
        crop_y = max((img.size[1] - h) / 2, 0)
        crop_w = min(w, img.size[0])
        crop_h = min(h, img.size[1])
        cropped = img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
        if offset_x == 0 and offset_y == 0:
            return cropped
        bg = PIL.Image.new('RGBA', (w, h), bgc or parse.WHITE_RGBA)
        bg.paste(cropped, (offset_x, offset_y))
        return bg
    return img.resize((w, h), PIL.Image.ANTIALIAS)


def trans_image(img, mode):
    return adjust(img, **parse.parse(mode))


def trans_file(filename, mode):
    return trans_image(PIL.Image.open(src), mode)

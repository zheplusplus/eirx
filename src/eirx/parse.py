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

    def fill_color(opt_result, opt_string, index):
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

    def addfilter(opt_result, opt_string, index):
        opt_result['filters'].append(opt_string[index: index + 4])
        return 4

    opt_result = dict(filters=[])
    opt_map = dict(
        a=not_keep_aspect_ratio,
        c=crop,
        f=frame,
        w=window,
        F=fill_color,
        x=addfilter,
    )
    i = 0
    while i < len(opt):
        try:
            i += opt_map[opt[i]](opt_result, opt, i + 1)
        except LookupError:
            raise ValueError('Invalid option')
        i += 1
    return opt_result


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
    (re.compile('^o$'), lambda _: dict()),
)

Eirx - Easy Image Resizer
===

Resize image in an easy way.

Installation
===

    $ pip install eirx

Usage
===

    $ eirx MODE SRC DEST

where *MODE* is one of

* wWIDTHhHEIGHT : to certain width and height (e.g. w200h300 to resize the image to 200px in width and 300px in height)
* wWIDTH : to certain width, with aspect ratio kept
* wWIDTHa : to certain width, without aspect ratio kept
* hHEIGHT : to certain height, with aspect ratio kept
* hHEIGHTa : to certain height, without aspect ratio kept

*SRC* and *DEST* are files.

Quick Start API
===

    >>> from eirx.parse import parse
    >>> from PIL import Image
    >>>
    >>> args, adjust = parse('w200h300')
    >>> im = adjust(Image.open('hello.png'), **args)
    >>> im.show()
    >>> im.save('output.png')

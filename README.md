Eirx - Easy Image Resizer
===

Resize image in an easy way.

Installation
===

    $ pip install eirx

Usage
===

    $ eirx MODE SRC DEST # convert image
    $ eirxv MODE SRC # view converted image

where *MODE* is in a form like *size-options* or *size* only.

*size* should be one of the following format

* wWIDTHhHEIGHT : to certain width and height (e.g. w200h300 means 200px in width and 300px in height)
* wWIDTH : to certain width (and the adjust height option will automatically set in this mode)
* hHEIGHT : to certain height (and the adjust width option will automatically set in this mode)
* LENGTH : to square, with side length set (and the central crop option will automatically set in this mode)

*options* is a string, each character represent an option, the rule is

* a : absolute size; will clear the adjust height or width options
* c : central crop; if the output size is less than the image size, only central part of the image is used (not resize or scratch the image)

*SRC* and *DEST* are files.

For example

    $ eirx w200h400 hello.png output.png
    $ eirx w200 hello.png output.png
    $ eirxv w200h400-c hello.png
    $ eirxv w200-a hello.png

Quick Start API
===

    >>> from eirx.parse import parse
    >>> from PIL import Image
    >>>
    >>> args, adjust = parse('w200h300')
    >>> im = adjust(Image.open('hello.png'), **args)
    >>> im.show()
    >>> im.save('output.png')

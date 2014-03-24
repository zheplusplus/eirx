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

*size* indicates the dimensions of *output image*, and should be one of the following formats

* wWIDTHhHEIGHT / hHEIGHTwWIDTH: to certain width and height (e.g. w200h300 means 200px in width and 300px in height)
* wWIDTH : to certain width (and the size adjusting option will automatically set in this mode)
* hHEIGHT : to certain height (and the size adjusting option will automatically set in this mode)
* LENGTH : to square, with side length set (and the central crop option will automatically set in this mode)
* o: keep original size

Among the size options, `h` or `w` could also be `hma` or `wma`, representing maximum height or maxium width. The rules of size are

* when both width and height are specified (either definite or maximum), the size of the output is the specified value
* when a dimension is set to a maximum size, its value would be `min(original_size, max_size)`
* if only one dimension size is set, the other would be calculated by aspect ratio, or, when `-a` option is set (discussed in the next section), the original size of the image

*options* is a string, each character represent an option, the rule is

* a : absolute size; will clear the size adjusting option
* c : centralize & crop; resize the image to fill the size, and crop the part out of the region
* t : crop top; similar to `c`, but vertically crop the top of the image; usally used for crop head from full-body photo; prior to crop
* w : window mode; if the output size is less than the image size, only central part of the image is used (not resize or scratch the image)
* f : framed mode; scratch the image to output size, with aspect ratio kept; then paste the scratched to the center of the output, and fill the rest part with a certain color
* F : set filling color to white (with `Fw`), black (`Fb`) or customized (`FxRRGGBB`)
* x : apply a filter; read wiki for detail and filter list

*SRC* and *DEST* are files.

For example

    $ eirx wma200hma400 hello.png output.png
    $ eirx wma200 hello.png output.png
    $ eirx w1280h720-Fwc hello.png output.png
    $ eirxv w200h400-c hello.png
    $ eirxv w200-a hello.png
    $ eirxv 400-fFx1010cc hello.png
    $ eirxv o-xdclr hello.png

Quick Start API
===

    >>> from eirx.parse import parse
    >>> from eirx.api import adjust, trans_file
    >>> from PIL import Image
    >>>
    >>> im = trans_file('hello.png', 'w200h300')
    >>> im.save('output.png')
    >>>
    >>> args = parse('w200h300-xedge')
    >>> im = adjust(Image.open('hello.png'), **args)
    >>> im.show()

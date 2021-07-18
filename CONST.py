from PIL import Image ,ImageOps, ImageDraw

LOG = False
REG = True
FORMATS = [".jpg", ".jpeg", ".JPG", ".JPEG", ".jpe" ,".JPE", ".PNG", ".png"]
SIZE = (150, 150)

def get_diveded_str(string, divide):
    dot = string.find(divide)
    return string[dot:]


def compare_str(string):
    isSame = False
    for i in FORMATS:
        if i == string:
            isSame = True
            break
    return isSame


def get_image(path):
    im = Image.open(path)
    im = crop(im, SIZE)
    im.putalpha(prepare_mask(SIZE, 4))
    im.save('resize-output.png')
    print(im.size)
    return 'resize-output.png'

def prepare_mask(size, antialias = 2):
    mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
    return mask.resize(size, Image.ANTIALIAS)


def crop(im, s):
    w, h = im.size
    k = w / s[0] - h / s[1]
    if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    return im.resize(s, Image.ANTIALIAS)

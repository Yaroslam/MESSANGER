from PIL import Image , ImageDraw
import os
HOST = '127.0.0.1'
PORT = 1233
PIC_PATH = './pic/'
DB_PATH = 'databases'
REG = False
FORMATS = [".jpg", ".jpeg", ".JPG", ".JPEG", ".jpe" ,".JPE", ".PNG", ".png"]
SIZE = (150, 150)
style_window = "background-color: #bacdff; border-color: #bacdff"
style_button_log_reg = "background-color: \
                           #6E83C0; \
                           color: rgba(0,0,0,255); \
                           border-style: solid; \
                           border-radius: 35px; border-width: 3px; \
                           border-color: #002385; \
                           font-align: center; \
                           font-size: 36px; \
                           font-type: Roboto;"
style_button_log_reg_clicked = "background-color: \
                           #6E83C0; \
                           color: rgba(0,0,0,255); \
                           border-style: solid; \
                           border-radius: 35px; border-width: 3px; \
                           border-color: #00154e; \
                           font-align: center; \
                           font-size: 36px; \
                           font-type: Roboto;"

style_label = "background-color: \
                           #6E83C0; \
                           color: rgba(0,0,0,255); \
                           border-style: solid; \
                           border-radius: 35px; border-width: 3px; \
                           border-color: #002385; \
                           font-align: center; \
                           font-size: 36px; \
                           font-type: Roboto;"

style_text = "font-size: 36px; \
                           font-type: Roboto;"

style_button_ok = "background-color: \
                           #6E83C0; \
                           color: rgba(0,0,0,255); \
                           border-style: solid; \
                           border-radius: 35px; border-width: 3px; \
                           border-color: #002385; \
                           font-align: center; \
                           font-size: 36px; \
                           font-type: Roboto;"

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


def get_image(new_path ,path):
    if not os.path.isdir(PIC_PATH):
        os.mkdir(PIC_PATH)
    im = Image.open(path)
    im = crop(im, SIZE)
    im.putalpha(prepare_mask(SIZE, 4))
    im.save(PIC_PATH+new_path+'.png')
    print(im.size)
    return PIC_PATH+new_path+'.png'

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

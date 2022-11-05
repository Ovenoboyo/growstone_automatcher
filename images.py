import cv2 as cv
import numpy as np
import subprocess
import PIL.Image as Image
import io

singles = ["error", "ok"]
stones = ["clover", "four_clover", "hadouken", "donut",
          "bronze", "silver", "gold",
          "crescent", "half_moon", "full_moon",
          "snowball", "ice_cube", "icicle", "fireball", "butterfly", "angel_wings", "dragon_wings", "3_ball"]

def screenshot(top=None, height=None):
    raw = subprocess.run(["adb", "shell", "screencap", "-p "],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).stdout.replace(b'\r\n', b'\n')
    stream = io.BytesIO(raw)
    rgba_image = Image.open(stream)
    size = rgba_image.size

    if top is None:
        top = 0
    if height is None:
        height = size[1]
        
    rgba_image = rgba_image.crop((0, top, size[0], size[1]))
    return [cv.cvtColor(np.array(rgba_image), cv.COLOR_RGB2BGR), top]


def info(t):
    img = cv.imread('stone_templates/{}.png'.format(t))
    return t, img


def dim(t):
    img = cv.imread('stone_templates/{}.png'.format(t))
    return img.shape[1], img.shape[0]


def pouch():
    return info('pouch')

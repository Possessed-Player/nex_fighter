import cv2 as cv
import numpy as np
from cvbot.io import read_img, save_img
from cvbot.images import Image
from cvbot.match import mse
from cvbot.capture import get_region


SDIMS = [read_img("src/{}.png".format(i), "grey") for i in range(10)]

def process_n(im):
    """
    Image -> Image
    Given an image of a full-number return a black and white version
    with the black columns at the start and end trimmed
    """
    for x in range(15):
        if im.img[0, x][0] < 50:
            clr = im.img[0, x]      # Scan the first row of the image
                                # Once we hit a pixel with pixel value
                                # save it as the unique color
    bim = cv.inRange(im.img, clr, clr)

    while True:
        psd = False                     # This part will trim/remove
                                        # columns at the start or end
        if not (255 in bim[:, 0]):      # that are full black columns
            bim = bim[:, 1:]
        else:
            psd = True

        if not (255 in bim[:, -1]):
            bim = bim[:, :-1]
        else:
            if psd:
                break

    return Image(bim)

def split_n(im):
    """
    Image -> list(Image)
    *** Initial version, will change soon ***
    Given black and white image of a full-number
    return each digit as its own image in a list
    """
    w, _ = im.size

    prta, prtb, prtc = None, None, None # First, second and third digit

    if w >= 7:
        fxb = None              # First x(column) of part (b) or second digit

        for x in range(w):
            col = im.img[:, x]  # Columns from left to right of the image
            sm = np.sum(col)    # Sum of the pixel values of the column

            if sm == 0:         # Black column
                if prta is None:
                    prta = im.img.copy()[:, :x]
                elif prtb is None and not (fxb is None):
                    prtb = im.img.copy()[:, fxb:x]
            elif not (prta is None) and prtb is None and fxb is None:
                fxb = x
            elif not (prtb is None):
                prtc = im.img.copy()[:, x:]
                break
        else:
            if not (fxb is None):
                prtb = im.img.copy()[:, fxb:]
    else:
        prta = im.img

    return [Image(prta),] + ([] if prtb is None else [Image(prtb),] + 
                      ([] if prtc is None else [Image(prtc),]))

def combine(loi):
    """
    list(int) -> int
    Combine digits in the integer list
    into one full-number
    """
    fn = ""

    for i in loi:
        fn += str(i)

    return int(fn)

def read_n(dims):
    """
    list(Image) -> int
    Read each digit image and return the full-number
    as an integer
    """
    results = []

    for dim in dims:
        best = None
        for i, SDIM in enumerate(SDIMS):
            ndim = dim.resize((SDIM.size))  # Must be the same size before
            df = mse(ndim, SDIM)            # doing mean squared difference
            if best is None or df < best[1]:# Which is just a pixel for pixel
                best = i, df                # comparison

        results.append(best[0])

    return combine(results)

def read_vitals(region):
    """
    Rect -> int
    Return the integer displayed
    in the given screen region
    """
    img = process_n(get_region(region))
    return read_n(split_n(img))

if __name__ == "__main__":
    # -------- Save digits ------------------------
    #img = read_img("test.png")
    #bimg = process_n(img)
    #digits = split_n(bimg)
    #print(len(digits))
    #for i, d in enumerate(digits):
    #    save_img(d, "digit{}.png".format(i))
    # ---------------------------------------------
    pryr = (525, 123, 20, 8)
    hp = (524, 89, 22, 8)
    eng = (534, 155, 22, 8)

    while True:
        print("   HP: {1}, Prayer: {0}, Energy: {2}    ".
              format(read_vitals(pryr),
                     read_vitals(hp),
                     read_vitals(eng)), end="\r")

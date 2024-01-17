import cv2 as cv
import numpy as np
from cvbot.io import read_img
from cvbot.images import Image
from cvbot.match import mse
from cvbot.capture import get_region, get_pixel
from cvbot.colors import clr_find


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

HP_REG   = (528, 89, 22, 8)
PRYR_REG = (528, 123, 22, 8)

def hp():
    """
    None -> int
    Return current HP value
    """
    return read_vitals(HP_REG)

def prayer():
    """
    None -> int
    Return current prayer value
    """
    return read_vitals(PRYR_REG)

INVEN_REG  = (569, 243, 158, 250)
SARA_CLR   = (76, 200, 202)
REST_CLR   = (105, 61, 171)      # Blue, Green, Red(BGR)
EMPT_CLR   = (118, 116, 116)
PFM_PRYR   = (612, 388)
EE_PRYR    = (724, 388)
PRYRON_CLR = (110, 180, 206)

def find_pots(pot=""):
    """
    str -> list((int, int))
    Given name/key of pot to find
    return locations of the pots on screen
    """
    if pot == "s":
        var = 50
        mnht = 0
        clr = SARA_CLR
    elif pot == "r":
        var = 60
        mnht = 0
        clr = REST_CLR
    elif pot == "":
        var = 50
        mnht = 22
        clr = EMPT_CLR
    else:
        print("Potion name/key not found!")
        return [] 

    invim = get_region(INVEN_REG)
    locs = clr_find(invim ,clr, variation=var, 
                    min_wd=15,
                    min_ht=mnht,
                    relative=INVEN_REG) 
    # --------- Test Code -------            # Find locations of blocks of
    #gmim = get_region((0, 0, 800, 600))      # given color
    ## Taking an image of the whole game      # 20 is the color variation
    ## To properly see if the location is     # meaning color can vary
    ## correct                                # by 20 or less in value
    #nim = gmim.draw_rects(locs, rects=True)  # in all blue, green and red
    #print(len(locs))                         # channels
    #nim.show()
    # ---------------------------
    locs = list(sorted(locs, key=lambda x: x[2] * x[3]))
    # Smallest object first, meaning potions with the lowest doses
    # is first in the list

    return  [(loc[0] + (loc[2] // 2), loc[1] + (loc[3] // 2)) for
             loc in locs]

def prayer_on():
    """
    None -> list(bool, bool) 
    Return list of 2 booleans
    the first one is True if pfm prayer is on
    the second is True if ee prayer is on 
    False otherwise
    ASSUMPTION: PRAYER TAB IS OPEN
    """
    clrs = get_pixel(PFM_PRYR), get_pixel(EE_PRYR)

    res = []
    for clr in clrs:
        res.append(tuple(clr[:3]) == PRYRON_CLR)

    return res 

if __name__ == "__main__":
    find_pots("s")

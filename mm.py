from cvbot.match import look_for
from cvbot.io import read_img, save_img
from cvbot.capture import get_region
from cvbot.mouse import click
from cvbot.match import mse
from math import dist
from time import sleep
from world import reset_comp
import numpy as np
from cv2 import inRange
from os.path import join


pth = "src/"
center = 650, 116
si, ei = 193, 2632
lpos = None
reg = (26, 21, 104, 92)
mmreg = (573, 40, 161, 150) 
nfull = read_img(pth+"full4.png")
mmk = {"h" :"home", 
       "b1":"out_boss_a", 
       "b2":"out_boss_b",
       "b3":"out_boss_c",
       "b4":"out_boss_d",
       "b4b":"out_boss_d2",
       "b5":"pre_boss"}
mms = {mmk[l]:read_img(join("src", "mm_" + l + ".png"), "grey") 
       for l in ["h", "b1", "b2", "b3", "b4", "b4b", "b5"]}


def process(im):
    """
    Image -> Image
    Remove noise from minimap image
    and return a clean image
    """
    global reg

    im.img = inRange(im.img, (255, 255, 255, 255), (255, 255, 255, 255))
    im.type = "grey"

    return im

def nprocess(im):
    """
    Image -> Image
    Remove noise from nex minimap image
    and return a clean image
    """
    global reg

    im = im.crop(reg)

    mask = np.logical_and(im.img[:, :, 2] > 80, im.img[:, :, 0] < 150)
    maskb = np.logical_and(im.img[:, :, 1] < 30, im.img[:, :, 0] > 150)
    im.img[mask] = np.array((200, 200, 200, 255), dtype=im.img.dtype)
    im.img[maskb] = np.array((200, 200, 200, 255), dtype=im.img.dtype)
    #im.img = np.where(im.img == (1, 0, 0, 255), np.array((200, 200, 200, 255), dtype=im.img.dtype), im.img)
    im.img[im.img > 200] = 200

    return im

# ----------------- FULL MAP COMPILATION -----------------------------
#
#def compile_into_full():
#    full = read_img(pth+"200.png")
#    full.name = "full"
#    full = process(full)
#    lpos = 0, 0
#
#    st = time()
#    for i in range(200, 2630):
#        a = process(read_img(pth+"{}.png".format(i)))
#        b = process(read_img(pth+"{}.png".format(i+1)))
#
#        t = Image(np.zeros((96, 108, 3), dtype=a.img.dtype))
#        at = t.draw_img(a, (2, 2)) 
#        at.name = "at"
#
#        bst = (None, None)
#        for i in range(5):
#            for j in range(5):
#                bt = t.draw_img(b, (i, j)) 
#                bt.img[:2, :,  :]  = 0 
#                bt.img[:, :2,  :]  = 0 
#                bt.img[-2:, :, :]  = 0 
#                bt.img[:, -2:, :]  = 0 
#                bt.name = "bt"
#                
#                res = mse(at, bt)
#                if bst[0] is None or res < bst[0]:
#                    bst = (res, (i - 2, j - 2))
#
#        lx, ly = bst[1][0] + lpos[0], bst[1][1] + lpos[1]
#        lpos = 0 if lx < 0 else lx, 0 if ly < 0 else ly 
#        full = full.draw_img(b, (lx, ly))
#    et = time()
#
#    print("Compiled 2300+ images in {} seconds!".format(round(et - st)))
#    full.show()
#    cv.imwrite(pth+"full.png", full.img)
#
# ------------------------------------------------------------------------------

def current_loc():
    """
    None -> str | None
    Read the current minimap,
    and return the location as string
    or None if the location is unknown
    """
    global mmreg

    reset_comp()

    # ----------Loading Locally------------------
    # mm = read_img("testb.png") 
    # mm = mm.crop(mmreg)
    # -------------------------------------------
    mm = get_region(mmreg)
    mm = process(mm)
    #-- Save Proccessed MM --
    #save_img(mm, "test.png") 
    #return 
    #------------------------
    df = 500

    for n, im in mms.items():
        res = mse(mm, im)
        if res < df:
            return n


def nget_pos(reset=True):
    """
    bool -> Point
    Return the current location
    in the nex champer using the minimap
    Reset compass when 'reset' is True
    """
    global nfull, mmreg

    if reset: reset_comp()

    mm = get_region(mmreg)
    sleep(0.2)

    of = -1, 9
    mm = nprocess(mm)

    pos = look_for(mm, nfull, 0.6) 

    if pos is None:
        return

    pos = pos[0] + of[0], pos[1] + of[1]

    return pos

def mm_to_wrld(df, dst):
    """
    Point, float -> Point
    Convert minimap position to world position
    """
    # 0  , 0   -> 268 , 200
    # 268, 200 -> +180, -100 -> 448, 100
    # 0  , 0   -> -63 , 42   -> -63, 42
    mlt = ((40 / dst) - 1) 
    wc = 268, 200
    #xcd, xcu, ycd, ycu = 7.85, 5.85, 4.85, 2.45
    xc, yc = 4.55 + mlt, 2.55 + mlt

    #df = pos[0] - center[0], pos[1] - center[1]
    #xc, yc = (xcd, ycd) if df[1] > 0 else (xcu, ycu)
    wdf = round(xc * df[0]), round(yc * df[1])
    wpos = wc[0] + wdf[0], wc[1] + wdf[1]

    return wpos

def nmove_to(tpos, reset=True):
    """
    Point, bool -> bool 
    Given scene image and a nex champer
    minimap position,
    move to that position
    Return False if the current position
    isn't the target position
    """
    global center, lpos
    mxdst = 2

    cpos = nget_pos(reset)
    if cpos is None: # TODO: Test this part
        return False

    if dist(cpos, tpos) > mxdst:
        xd, yd = tpos[0] - cpos[0], tpos[1] - cpos[1]

        if abs(xd) > 40:
            xd = -40 if xd < 0 else 40
        if abs(yd) > 30:
            yd = -30 if yd < 0 else 30

        pos = center[0] + xd, center[1] + yd

        #if lpos is None or cpos != lpos:
        click(pos)
        #else:
        #    pos = choice([(pos[0], 0), (0, pos[1])])
        #    click(pos)

        #st = dist(cpos, tpos) / 12
        sleep(1)

    lpos = cpos

    return dist(cpos, tpos) <= mxdst


if __name__ == "__main__":
    from sys import argv
    from cvbot.mouse import move
    from math import dist

    
    #from cvbot.mouse import ms
    #while True:
    #    print("Position:", nget_pos(reset=False))
    #    print("Mouse:", ms.position, "\n")
    #print(current_loc())
    #from cvbot.capture import get_region
    #import cv2 as cv
    #creg = (0, 0, 770, 530)
    #cptr = lambda: get_region(creg)
    #move_to((71, 77))
    #mmreg = (573, 40, 161, 150)

    #while True:
    #    mm = get_region(mmreg)
    #    pos = get_pos()

    #    if pos is None:
    #        continue

    #    cv.circle(flc.img, pos, 3, (0, 0, 255), 3)
    #    cv.imshow("Full Minimap - Test", flc.img)
    #    cv.waitKey(1)

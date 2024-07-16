from cvbot.images import Image
from cvbot.io import read_img
from cvbot.match import mse
from cvbot.capture import get_pixel
from cvbot.mouse import click
from cvbot.keyboard import press
from cvbot.nums import nread, init_reader
from time import sleep
import cv2 as cv
import numpy as np


inv_reg = (565, 240, 170, 255)
DIGITS = [read_img("src/{}.png".format(i), "grey") for i in range(10)]
sara_clr  = (80, 200, 200, 255), (100, 210, 210, 255)
rest_clr  = (100, 50, 170, 255), (120, 75,  195, 255)
empty_clr = (90,  90,  90, 255), (120, 120, 120, 255)
drop_c = 0
AMP = 620, 380
RNP = {1:(726, 386),
       2:(650, 460)}

def select_tab(tab):
    if tab == "inven":
        p = 650, 220
    elif tab == "mgk":
        p = 750, 220
    elif tab == "qst":
        p = 615, 215
    elif tab == "stng":
        p = 680, 515

    click(p)

def read_dgts(dgts):
    results = []

    for dgt in dgts:
        if dgt is None:
            results.append(None)
            continue
        ndgt = Image(dgt)
        for i, DGT in enumerate(DIGITS):
            ndgt.img = cv.resize(dgt, DGT.img.shape[::-1])
            res = mse(ndgt, DGT)

            if res < 1500:
                results.append(i)
                break
        else:
            results.append(None)
    
    return results

def read_num(im):
    _, w = im.shape

    prta = None
    prtb = None
    prtc = None

    if w >= 7:
        bi = 0
        for i in range(w):
            col = im[:, i]
            sm = np.sum(col)

            if sm == 0:
                if prta is None:
                    #print("1", i)
                    prta = im[:, :i]
                elif prtb is None and bi != 0:
                    prtb = im[:, bi:i]
            elif not (prta is None) and prtb is None and bi == 0:
                #print("2", i)
                bi = i
            elif not (prtb is None):
                #print("3", i)
                prtc = im[:, i:]
                break
        else:
            prtb = im[:, bi:]
    else:
        prta = im
                
    nmbr = read_dgts((prta, prtb, prtc))
    #print(nmbr)

    if nmbr[0] is None:
        nmbr = None
    elif nmbr[1] is None:
        nmbr = nmbr[0]
    elif nmbr[2] is None:
        nmbr = nmbr[:2]
        nmbr = int("".join(str(i) for i in nmbr))
    else:
        nmbr = int("".join(str(i) for i in nmbr))

    return nmbr

def process_num(im):
    for x in range(10):
        if im[0, x][0] < 50:
            clr = im[0, x]

    im = cv.inRange(im, clr, clr)

    while True:
        psd = False 

        if not (255 in im[:, 0]):
            im = im[:, 1:]
        else:
            psd = True
        
        if not (255 in im[:, -1]):
            im = im[:, :-1]
        else:
            if psd:
                break

    return im 

def read_vital(img, reg):
    im = img.crop(reg).img
    ds = process_num(im)

    return read_num(ds)

def hp(img):
    """
    Image -> int[0-99]
    Return current player hp
    """
    hprg = (531, 89, 17, 8)

    return read_vital(img, hprg)

def prayer(img):
    """
    Image -> int[0-99]
    Return current player prayer 
    """
    pyrg = (531, 123, 17, 8)

    return read_vital(img, pyrg)

def prayer_on(prop=1):
    """
    None -> list(bool, bool)
    Return a list of two booleans
    First is for anti magic prayer
    Second is for ranged attack prayer
    Each boolean represent the state of
    the prayer
    False -> Prayer is off
    True  -> Prayer is on
    """
    global AMP, RNP

    press("f3")
    sleep(0.1)
    bpos = RNP[prop]
    aclr, bclr = get_pixel(AMP), get_pixel(bpos)
    rdcs = aclr[2], bclr[2]

    res = []
    for rdc in rdcs:
        res.append(rdc > 140)     

    return res 

def sara_pots(img):
    """
    img -> int[0-14], Point
    Return number of saradomin brew pots in inventory
    and one of the pots location on screen
    """
    global inv_reg, sara_clr

    invim = img.crop(inv_reg)
    dst = cv.inRange(invim.img, sara_clr[0], sara_clr[1])
    blr = cv.GaussianBlur(dst, (9, 9), 3)

    cnts = cv.findContours(blr, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
    pnts = []
    for cnt in cnts:
        x, y, w, h = cv.boundingRect(cnt)
        x += 12 + inv_reg[0]
        y += 5 + inv_reg[1]
        pnts.append(((x, y), w * h))
        #img = cv.circle(invim.img, (x, y), 3, (255, 0, 0), 3)

    #cv.imshow("test", img)
    #cv.waitKey(0)

    if len(pnts):
        pnts.sort(key=lambda x: x[1])
        return len(pnts), pnts[0][0]
    else:
        return 0, None

def rest_pots(img):
    """
    Image -> int[0-14], Point
    Return number of super restore pots in inventory
    and one of the pots location on screen
    """
    global inv_reg, rest_clr

    invim = img.crop(inv_reg)
    dst = cv.inRange(invim.img, rest_clr[0], rest_clr[1])
    blr = cv.GaussianBlur(dst, (9, 9), 3)

    cnts = cv.findContours(blr, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
    pnts = []
    for cnt in cnts:
        x, y, w, h = cv.boundingRect(cnt)
        x += 12 + inv_reg[0]
        y += 6 + inv_reg[1]
        pnts.append(((x, y), w * h))
        #img = cv.circle(invim.img, (x, y), 3, (255, 0, 0), 3)

    #cv.imshow("test2", img)
    #cv.waitKey(0)

    if len(pnts):
        pnts.sort(key=lambda x: x[1])
        return len(pnts), pnts[0][0]
    else:
        return 0, None

def empty_slots(img):
    """
    Image -> int[0-28]
    Return the number of empty slots
    in inventory
    """
    global inv_reg

    invim = img.crop(inv_reg)
    total = 0

    for i in range(28):
        pos = ind_to_pos(i)
        cpos = pos[1] - inv_reg[1], pos[0] - inv_reg[0]
        clr = invim.img[cpos]
        b, g, r = clr[:3]
        res = (50 < b < 62) and (59 < g < 71) and (68 < r < 81)
        if res: total += 1

    return total

def empty_pots(img):
    """
    Image -> int[0-14], Point
    Return number of empty pots in inventory
    and one of the pots location on screen
    """
    global inv_reg, empty_clr 

    invim = img.crop(inv_reg)
    dst = cv.inRange(invim.img, empty_clr[0], empty_clr[1])
    blr = cv.GaussianBlur(dst, (9, 9), 3)

    cnts = cv.findContours(blr, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
    pnts = []
    for cnt in cnts:
        x, y, w, h = cv.boundingRect(cnt)
        area = w * h
        if area < 645:
            continue
        #print(area)
        x += 12 + inv_reg[0]
        y += 15 + inv_reg[1]
        pnts.append((x, y))
        #img = cv.circle(invim.img, (x, y), 3, (255, 0, 0), 3)

    #cv.imshow("test3", img)
    #cv.waitKey(0)

    if len(pnts):
        return len(pnts), pnts
    else:
        return 0, None

def drop_item_pos(pos, long=False):
    """
    Point, bool -> None
    Drop an item in the inventory with
    screen location "pos"
    Add extra y distance for long menus
    if 'long' is True
    """
    global drop_c 
    drop_c += 1
    dpos = pos[0], pos[1] + ((50 if not long else 80) if pos[1] < 450 else 
                             (25 if not long else (15 if pos[1] != 450 else 45)))

    click(pos, "right")
    sleep(0.2)
    click(dpos)
    sleep(1)

def ind_to_pos(i):
    """
    int -> Point
    Convert index number of an item
    to position of that item
    """
    x, y, _, _ = 588, 265, 147, 246
    dfx, dfy = 43, 37
    col, row = i % 4, i // 4
    pos = x + (dfx * col), y + (dfy * row) 
    return pos

def drop_item(i, long=False):
    """
    int, bool -> None
    Drop item with index 'i' starting
    from top left
    Add extra y distance for long menus
    if 'long' is True
    """
    pos = ind_to_pos(i)
    drop_item_pos(pos, long)


if __name__ == "__main__":
    from cvbot.capture import screenshot
    print(" ")
    while True:
        img = screenshot()
        try:
            p = hp(img) 
            print(p, " ", end="\r")
        except Exception as e:
            #print(e)
            pass
        #break

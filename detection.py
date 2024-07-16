import cv2 as cv
import numpy as np


def fill(img):
    fltr = np.array([[0,  0, 0],
                     [1,  1/2, 1],
                     [0,  0, 0]])

    for i in range(10):
        img = cv.filter2D(img, -1, fltr)

    return cv.GaussianBlur(img, (9, 9), 5)

if __name__ == "__main__":
    for i in range(610, 900):
        oimg = cv.imread("imgs/sc{}.png".format(i))
        imga = cv.inRange(oimg, (0, 255, 0), (0, 255, 0))
        imgb = cv.inRange(oimg, (0, 0, 255), (0, 0, 255))
        img = imga + imgb
        img[30:60, 140:370] = 0

        fld = fill(img)
        cv.imshow("filling", fld)
        cv.waitKey(0)
        cnts = cv.findContours(fld, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]

        bst = (None, None)
        for cnt in cnts:
            x, y, w, h = cv.boundingRect(cnt)

            if bst[0] is None or (abs(108 - w) < bst[0]):
                bst = (abs(108 - w), (x, y))
        
        if bst[0] is None:
            continue
        x, y = bst[1] 
        oimg = cv.rectangle(oimg, (x + 40, y + 12), (x + 90, y + 30), (255, 0, 0), 3)
        cv.imshow("test", imga)
        cv.imshow("com", img)
        cv.imshow("org", oimg)
        cv.waitKey(0)

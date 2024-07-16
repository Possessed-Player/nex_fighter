from cvbot.mouse import click_region, click, move
from cvbot.keyboard import hold_for
from cvbot.capture import get_region
import cv2 as cv
import numpy as np
from time import sleep


def reset_comp():
    """
    None -> None
    Click on the compass to reset it
    to the north direction
    """
    reg = (558, 40, 23, 23)
    click_region(reg)

def max_y():
    """
    None -> None
    Maximize the camera y value making it 
    look from uptop
    """
    hold_for("up", 2)

def is_item():
    """
    None -> bool
    Return True if the current object 
    being hovered over by mouse is an item
    """
    reg = 50, 40, 90, 10
    clr = (45, 110, 200, 255), (55, 120, 210, 255)
    itim = get_region(reg)
    count = cv.inRange(itim.img, *clr).sum() // 255

    return count > 120

def pick_items(dc):
    """
    int -> None
    ASSUMPTION: camera is at maximum and y and compass is facing north
    Checks if there are items beneath player model
    and picks them all
    """
    #pos = 270, 202
    #pos = 270, 204

    # 274 -> 266, 206 -> 198
    reset_comp()

    while dc > 0: 
        fpx, fpy = 267, 199
        fnd = False
        for x in range(5):
            for y in range(7):
                pos = fpx + x, fpy + y
                move(pos)
                sleep(0.2)
                if is_item():
                    fnd = True
                
                if fnd:
                    break
            if fnd:
                break
        else:
            return dc

        click(pos)
        sleep(1)
        dc -= 1

    return dc

def full_reset():
    """
    None -> None
    Reset camera position
    to a unique setting(maximum y tilt, and facing north)
    """
    reset_comp()
    max_y()
    
def collect_items(dc):
    """
    int -> int 
    Pick items from the ground
    right beneath player model    
    """
    #full_reset()
    return pick_items(dc)

if __name__ == "__main__":
    from cvbot.mouse import ms
    while True:
        print(ms.position, " ", end="\r")
    #collect_items(4)

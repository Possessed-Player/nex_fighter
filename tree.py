from world import max_y
from cvbot.mouse import click
from cvbot.io import read_img
from cvbot.match import look_for, compare
from cvbot.capture import get_region
from mm import current_loc
from bot import gmreg
from os.path import join
from time import sleep


trp = 120, 300
tlim = read_img(join("src", "tlb.png"), "grey")
dnmnp = 205, 55
dnmnim = read_img(join("src", "dnmnu.png"), "grey")

def tp_tree():
    """
    None -> bool
    Click on magic tree and select teleport
    Return False if tree rt click menu was not found
    """
    max_y()
    click(trp, "right")
    sleep(0.2)

    pos = look_for(tlim, get_region(gmreg, True))
    tfnd = not (pos is None)

    if tfnd:
        sleep(0.5)
        click(pos)
        sleep(5)

    return tfnd

def menu_hand():
    """
    None -> bool
    Choose nex from the dungeon teleport menu
    Return False if the menu wasn't visible
    """
    fvp = 75, 125
    nex = 280, 120

    if not compare(dnmnp, dnmnim):
        return False
    else:
        click(fvp)
        sleep(0.2)
        click(nex)
        sleep(4)
        return True

def main():
    """
    None -> bool
    Teleport to boss area using magic tree
    ASSUMES: PRE-BOSS SETUP IS DONE(REVIEW 'pprep.py')
    Return False if teleport wasn't successful
    """
    if tp_tree():
        if menu_hand():
            return current_loc() == "out_boss_a"

    return False

if __name__ == "__main__":
    print(main())

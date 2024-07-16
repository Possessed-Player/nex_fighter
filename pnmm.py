from cvbot.mouse import click
from cvbot.match import look_for, compare
from cvbot.capture import get_region
from cvbot.io import read_img
from cvbot.keyboard import press
from bot import gmreg
from mm import current_loc, nget_pos
from os.path import join
from time import sleep


opim = read_img(join("src", "opim.png"), "grey")
psim = read_img(join("src", "pass.png"), "grey")
nxpa = read_img(join("src", "nex_prompt_a.png"), "grey")
nxpb = read_img(join("src", "nex_prompt_b.png"), "grey")
DRPS = 285, 200

def door_a():
    """
    None -> bool
    Open first door in pre-nex area
    Return False if door wasn't in the correct place
    """
    drp = 370, 330
    click(drp, "right")
    sleep(0.2)
    opp = look_for(opim, get_region(gmreg))

    fnd = not (opp is None)
    if fnd:
        click(opp)
        sleep(5)
        tries = 1
        while current_loc() != "out_boss_b":
            if tries > 5:
                return False
            click(DRPS)
            sleep(2)
            tries += 1

    return fnd

def pre_nav(skip=False):
    """
    bool -> bool
    Navigate the nex minions area
    and open door to pre-nex room
    Return False if failed to reach the room
    """
    mva = (715, 120)
    mvb = (690, 155)
    dps = (455, 280)
    dpsb = (472, 283)

    if not skip:
        click(mva)
        sleep(6.5)
        if current_loc() == "out_boss_c":
            click(mvb)
            sleep(5.5)
            if current_loc() == "out_boss_d":
                click(dps, "right")
            elif current_loc() == "out_boss_d2":
                click(dpsb, "right")
            else:
                return False
        else:
            return False

    sleep(0.2)
    opp = look_for(opim, get_region(gmreg, True))

    fnd = not (opp is None)
    if fnd or skip:
        if not skip: 
            click(opp)
            sleep(6)
        tries = 1
        while current_loc() != "pre_boss":
            if tries > 5:
                return False
            click(DRPS)
            sleep(1.5)
            tries += 1

        return True
        
    return False

def _nex_prompt(clan):
    """
    bool -> bool | None
    Go through nex door prompt
    Return False if prompt wasn't visible
    """
    ppos = 120, 385

    wt = 0
    while not compare(ppos, nxpa):
        sleep(0.1)
        wt += 1
        if wt > 30:
            return False
        
    if clan:
        press("2")
        sleep(2)
        if compare(ppos, nxpb):
            press("1")
    else:
        press("1")
    
    sleep(2)
    return None if nget_pos() is None else True

def nex_door(clan):
    """
    bool -> bool
    Go through nex ancient door
    Return False if not successful
    """
    drp = 410, 195
    ndrp = 286, 195

    click(drp, "right")
    psp = look_for(psim, get_region(gmreg, True))

    fnd = not (psp is None)
    if fnd:
        click(psp)
        sleep(3)
        while True:
            ans = _nex_prompt(clan)
            if ans is None:
                sleep(10)
                click(ndrp)
                sleep(1)
            else:
                sleep(3)
                return ans

    return fnd

def main(clan=False):
    """
    bool -> bool
    Navigate area outside of nex champer
    to reach nex champer
    ASSUMES: TELEPORTED TO THE NEX AREA AND
    STANDING IN THE TELE TILE(NO MOVEMENT HAPPENED!)
    Return False if navigation wasn't successful
    """
    if door_a():
        if pre_nav():
            if nex_door(clan):
                return True

    return False

if __name__ == "__main__":
    print(pre_nav(skip=True))

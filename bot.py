import player
import world
from time import sleep
from cvbot.keyboard import press
from cvbot.mouse import click, move


HP_THRESH = 60
PRYR_THRESH = 50

def heal():
    """
    None -> None
    Use saradomin pots if available
    ASSUMPTION: INVENTORY IS OPEN
    """
    ploc = player.find_pots("s")
    click(ploc[0])

def restore():
    """
    None -> None
    Use restore pots if available
    ASSUMPTION: INVENTORY IS OPEN
    """
    ploc = player.find_pots("r")
    click(ploc[0])

def switch_tab(tab):
    """
    str -> None
    Switch the current tab to
    the given tab name/key
    """
    if tab == "inven":
        press("F1")
    elif tab == "pryr":
        press("F3")

def hp_handler():
    """
    None -> None
    When called checks for current HP
    and heals if the HP is lower than the
    prefered threshold
    """
    if player.hp() < HP_THRESH:
        #switch_tab("inven") # Default tab, no need to switch to
        heal()

def pryr_handler():
    """
    None -> None
    When called checks for current prayer
    and restores if the prayer is lower than the
    prefered threshold
    """
    if player.prayer() < PRYR_THRESH:
        #switch_tab("inven") # Will be the default tab, no need to switch to
        restore()

def pryr_switcher():
    """
    None -> None
    Makes sure the pfm and ee prayers are on
    if not turn them on
    """
    switch_tab("pryr")
    sleep(0.1)

    pfm, ee = player.prayer_on()

    if not pfm and not ee:
        click(player.PFM_PRYR[:2])
        sleep(0.1)
        click(player.EE_PRYR[:2])
    else:
        if not pfm:
            click(player.PFM_PRYR[:2])

        if not ee:
            click(player.EE_PRYR[:2])

    # Switch to default tab before returning
    switch_tab("inven")

def drop_item(pos, long):
    """
    Point, bool -> None
    Drop item at the position 'pos'
    on screen, if long is True
    assume the item right-click menu
    to be long
    """
    # Anything higher than 455 is considered last row
    # 17 at the last row for long menu, 33 for short menu
    if pos[1] > 455:
        dpos = pos[0], pos[1] + (17 if long else 23)
    else:
        if long and pos[1] > 420:
            dpos = pos[0], pos[1] + (57 if long else 45)
        else:
            dpos = pos[0], pos[1] + (75 if long else 45)

    click(pos, btn="right")
    sleep(0.1)
    click(dpos)

def drop_empty_pots(n):
    """
    int -> int
    Given number of empty pots to drop
    drop that number if possible and
    return the actual number of dropped pots
    """
    acn = 0

    pots = player.find_pots("")

    for pot in pots:
        if n == 0:
            break
        acn += 1
        drop_item(pot, long=False)
        n -= 1
        sleep(0.5)

    return acn

CLCT_REG = 264, 197, 10, 10

def collect_items():
    """
    None -> None
    Collect all items under character
    """
    while True:
        for x in range(CLCT_REG[2]):
            for y in range(CLCT_REG[3]):
                pos = x + CLCT_REG[0], y + CLCT_REG[1]
                move(pos)
                sleep(0.1)

                if world.is_item():
                    click(pos)
                    sleep(0.5)

                continue
        else:
            break 


if __name__ == "__main__":
    collect_items()

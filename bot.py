import player
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

if __name__ == "__main__":
    while True:
        pryr_handler()
        sleep(5)
        pryr_switcher()
        sleep(1)

from mm import current_loc
from cvbot.mouse import click
from cvbot.keyboard import press, combo_press
from bot import gmreg
import player
from cvbot.capture import get_region
from cvbot.match import look_for, compare
from cvbot.io import read_img
from time import sleep
from os.path import join


tkim = read_img(join("src", "dtlk.png"), "grey")
rcmim = read_img(join("src", "reclaim.png"), "grey")

def nav_to_death():
    """
    None -> None
    Move to death location and talk
    to the NPC
    """
    mva = 629, 151
    dtp = 298, 212

    if current_loc() == "home":
        click(mva)
        sleep(4)

        click(dtp, "right")
        sleep(0.2)
        tpos = look_for(tkim, get_region(gmreg))
        if not (tpos is None):
            click(tpos)
            sleep(5)

def death_handle():
    """
    None -> None
    Go through death prompts,
    select armor from the menu
    and remove potions
    """
    pos = 220, 60
    lkbtn = 440, 325

    if compare(pos, rcmim):
        click(lkbtn)
        sleep(2)
        press("1") 
        sleep(2)
        click(lkbtn)
        sleep(1)


def main():
    """
    None -> None
    Locate and talk to death NPC, retrieve
    lost items and get rid of potions
    """
    player.select_tab("inven")
    sleep(0.5)
    combo_press("ctrl+g")
    sleep(1)
    press("f2")
    sleep(0.5)
    nav_to_death()
    death_handle()

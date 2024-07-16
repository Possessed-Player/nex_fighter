from cvbot.mouse import click
from cvbot.keyboard import kbd, press
from cvbot.match import compare, look_for
from cvbot.io import read_img
from cvbot.capture import get_region
from time import sleep
from mm import current_loc 
from os.path import join
from player import select_tab
from world import max_y
import death


zmim  = read_img(join("src", "396zm.png"), "grey")
grim  = read_img(join("src", "grs.png"), "grey")
dthim = read_img(join("src", "death.png"), "grey") # TODO: GET MESSAGE IMAGE
chtreg = (11, 373, 500, 120)
invis = False

def home_tele():
    """
    None -> None 
    Teleport player to the home location
    """
    htp = 575, 255

    select_tab("mgk")
    sleep(0.2)
    click(htp)
    sleep(2)

    if current_loc() != "home":
        sleep(5)
        home_tele()

    sleep(1)

def set_zoom():
    """
    None -> None
    Set the scene zoom to 39.06%
    """
    zmp = 640, 295
    mnbtn = 616, 302

    select_tab("stng")
    sleep(0.2)
    while not compare(zmp, zmim):
        click(mnbtn)
        sleep(0.5)

def death_note():
    """
    None -> bool
    Return False if death message not visible
    """
    return not (look_for(dthim, get_region(chtreg)) is None)

def set_gear():
    """
    None -> None
    Choose nex gear
    """
    ast = 580, 480
    grp = 415, 45
    nxgr = 465, 100
    clsb = 505, 55

    select_tab("qst")
    sleep(0.2)
    click(ast)
    sleep(1)

    if not compare(grp, grim):
        set_gear

    click(nxgr)
    sleep(1)

    if compare(grp, grim):
        click(clsb)
        sleep(0.5)

    if death_note():
        death.main()
        main()

def main():
    """
    None -> None
    Prepare player for nex fight,
    (1) Teleport to home
    (2) Set approp. zoom
    (3) Wear gear
    """
    global invis

    home_tele()
    if not invis:
        kbd.type("::renderself")
        press("Enter")
        invis = True 
    max_y()
    set_zoom()
    set_gear()
    select_tab("inven")
  

if __name__ == "__main__":
    main()

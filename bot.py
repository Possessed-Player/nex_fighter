from cvbot.capture import get_region
from cvbot.match import look_for, compare#, find_all
from cvbot.mouse import click
from cvbot.mouse import move as mmove
from cvbot.io import read_img
from cvbot.keyboard import hold_for, press
#from cvbot.colors import count_clr, threshold
from math import dist
import player, world, mm, nex, npcs
import numpy as np
from random import randrange
from time import sleep, time

#caim = read_img("src/c_attack.png", "grey")
# SAVING IMAGES
#from cv2 import imwrite
#SIND = 0
# ---------------------

gmreg = (0, 0, 770, 530)
ldt = 0
lsdrp = 0
ranged = 99
atim    = read_img("src/atk.png", "grey")
teleim  = read_img("src/teletab.png", "grey")
tprom   = read_img("src/taim.png", "grey")
nxcmim  = read_img("src/nkcim.png", "grey")
corners = {
    "tl":(75, 73),
    "tr":(138, 72),
    "bl":(138, 142),
    "br":(75, 137)
}
MIDDLE = (107, 107)
FATK = True
FRUN = True
DHTHRESH = 65
PTHRESH = 40
HTHRESH = 65

def closest_corner(nv):
    """
    Point -> Point
    """
    global gmreg, corners

    cpos = mm.nget_pos()
    if cpos is None: # TODO: Test this part
        return
    bdst = None
    nnv = nv / np.linalg.norm(nv)

    for pos in corners.values():
        dst = dist(cpos, pos)
        cv = (pos[0] - cpos[0], pos[1] - cpos[1])
        cnrm = np.linalg.norm(cv)
        ncv = (cv / cnrm) if cnrm != 0 else (0, 0)

        dp = np.dot(nnv, ncv)

        if dp < 0:
            if dst < 10:
                continue
            elif bdst is None or dst < bdst[0]:
                bdst = (dst, pos)

    return bdst[1] if not (bdst is None) else list(corners.values())[0]

def change_view():
    """
    None -> None
    Move the camera view to a different x angle
    """
    hold_for("right", randrange(25, 50) / 100)

def attack(pos):
    """
    Point -> bool
    Attack mob in position 'pos'
    Return False if the attack wasn't successful
    """
    global atim, gmreg, FATK
    click(pos, "right")
    sleep(0.1)
    img = get_region(gmreg, True)
    apos = look_for(atim, img, 0.9)

    res = not (apos is None)

    if res:
        if FATK:
            sleep(2)
            FATK = False
        click(apos)
    else:
        mmove((pos[0] + 220, pos[1]))
    
    return res

def reset_window():
    from cvbot.windows import get_window
    wn = "runewild"
    t = get_window(wn)
    t.repos(0, 0)

def use_sara(img):
    """
    Image -> bool 
    Use saradomin potion
    Return False if no saradomin potions left
    TODO: Test 
    """
    global ldt, ranged

    n, pos = player.sara_pots(img)

    ans = n != 0

    if ans:
        df = time() - ldt
        if df < 2:
            return ans
            #img = get_region(gmreg)
            #hp = player.hp(img)
            #if hp > (HTHRESH - 10):
            #    return ans
            #sleep(2 - df)
        click(pos)
        ranged -= 10.5
        ranged = 1 if ranged < 1 else ranged
        ldt = time()
        
    return ans

def use_rest(img):
    """
    Image -> None
    Use super restore potion
    Return False if no restore potions left
    TODO: Test
    """
    global ldt, ranged

    n, pos = player.rest_pots(img)

    ans = n != 0

    if ans:
        df = time() - ldt
        if df < 2:
            return ans
            #sleep(2 - df)
            #img = get_region(gmreg)
            #pr = player.prayer(img)
            #if pr > PTHRESH:
            #    return ans
        click(pos)
        ranged += 32
        ranged = 99 if ranged > 99 else ranged
        ldt = time()

    return ans

def flee():
    """
    None -> None
    Exit the boss room    
    TODO: Test 
    """
    tpos = (160, 105)

    cpos = mm.nget_pos()
    dst = dist(cpos, tpos) if cpos else 100

    def aux_htp():
        bpos = 754, 218
        hpos = 574, 256
        click(bpos)
        sleep(0.2)
        click(hpos)
        sleep(1)


    tries = 0
    while dst > 40:
        mm.nmove_to(tpos)
        sleep(1)
        cpos = mm.nget_pos(False)
        dst = dist(cpos, tpos) if cpos else 100
        tries += 1
        if tries > 10:
            aux_htp()
            return

    cpos = mm.nget_pos(False)
    if not (cpos is None):
        dst = dist(cpos, tpos)
        mdf = tpos[0] - cpos[0], tpos[1] - cpos[1]
        wp = mm.mm_to_wrld(mdf, dst)
    else:
        aux_htp()
        return

    #click(wp)
    #mpos = (155, 105)
    #cpos = (317, 199)
    #
    #while not mm.nmove_to(mpos):
    #    sleep(0.1)

    click(wp, "right")
    sleep(0.2)
    res = look_for(teleim, get_region(gmreg))
    if res:
        click(res)
        pwt = 0
        ppos = (103, 389)
        while not compare(ppos, tprom):
            sleep(0.1)
            pwt += 1
            if pwt > 100:
                aux_htp()
                return

        press("1")
        sleep(0.5)
    else:
        aux_htp()

def qk_prayer(pbl, prop=1):
    """
    list(bool, bool) -> None
    Turn the turned off prayer on
    TODO: Test 
    """
    if not pbl[0]:
        click(player.AMP)
    if not pbl[1]:
        click(player.RNP[prop])

    press("f1")
    sleep(0.1)

def attack_nex():
    """
    None -> bool 
    Attack nex
    Return True if attack was successful
    TODO: Test
    """
    global FATK
    img = get_region(gmreg)
    pos = nex.position(img)

    if not (pos is None):
        return attack(pos)
    else:
        return False

def is_red(clr):
    """
    4 channel color -> bool
    Return False if the color is not pure red
    NOTE: function not used
    """
    return np.all(clr == [0, 0, 255, 255])

def attack_npc(npc):
    """
    str -> bool
    Attack nex minion with name 'npc'
    and return false if the minion is dead
    TODO: Test 
    """
    global gmreg

    ans = npcs.ded_record.get(npc)
    #print(npc, "dead?", not (ans is None) and ans)
    def aux(cp, mp):
        if not npcs.npc_dead(cp, get_region(gmreg)):
            res = not attack(cp)

            sleep(1)       
            if res:
                if npcs.ccounts[npc] > 2:
                    res = mm.nget_pos() == mp
                else:
                    npcs.ccounts[npc] += 1
                    res = False
            else:
                npcs.ccounts[npc] += 1
                res = npcs.npc_dead(cp, get_region(gmreg))
        else:
            res = True

        npcs.ded_record[npc] = res 
        return res 

    def aux_inrange(opos, tpos):
        pos_rng = opos[0] - 8, opos[1] - 8, opos[0] + 8, opos[1] + 8

        return (pos_rng[0] < tpos[0] < pos_rng[2] and
                pos_rng[1] < tpos[1] < pos_rng[3])

    if not (ans is None) and ans:
        return False
    else:
        pos, mpos = npcs.npcs[npc]
        cmpos = mm.nget_pos()
        if cmpos is None:
            return True 
        elif aux_inrange(mpos, cmpos):
            xdf, ydf = mpos[0] - cmpos[0], mpos[1] - cmpos[1]
            cpos = pos[0] + round(xdf * 2.5), pos[1] + round(ydf * 2.7)
            res = aux(cpos, cmpos)
        elif mm.nmove_to(mpos, False):
            res = aux(pos, mpos)
        else:
            res = False

        return not res

def drop_empty(img):
    """
    Image -> None 
    Drop all the empty pots
    return the number of dropped bots
    Drop restore potions if inventory
    is full
    """
    global FRUN

    n, poss = player.empty_pots(img)

    if n != 0:
        ned = 0
        for pos in poss:
            player.drop_item_pos(pos)
            ned += 1
            if ned == 3:
                break

    es = player.empty_slots(img) + n

    for _ in range(3 - es):
        _, rpos = player.rest_pots(img) 
        player.drop_item_pos(rpos, True)
        img = get_region(gmreg)

#def black_circles(img):
#    """
#    Image -> bool
#    Return True if the black circle nex attack is currently charging
#    """
#    #reg = (245, 208, 20, 15)
#    #c = count_clr(img.copy().crop(reg), (60, 60, 60), 40)
#    #print("COLORS:", c)
#    #return 200 > c > 100
#    global caim
#
#    screg = (13, 35, 510, 333) 
#    wimg = img.copy().crop(screg)
#    res = find_all(caim, wimg, 0.73)
#    return not (res is None) and len(res) > 10
#    # --------------------- OLD LOGIC ------------------------------
#    #dst = threshold(wimg, (50, 50, 50), 25)
#    #
#    #cnts = cv.findContours(dst.img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#    #cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#    #n = 0
#    
#    #for c in cnts:
#    #    peri = cv.arcLength(c, True)
#    #    approx = cv.approxPolyDP(c, 0.04 * peri, True)
#    #    #area = cv.contourArea(c)
#    #    ((_, _), r) = cv.minEnclosingCircle(c)
#    #    if len(approx) > 5 and 5 < r < 20:
#    #        #((x, y), r) = cv.minEnclosingCircle(c)
#    #        #cv.circle(stim.img, (int(x), int(y)), int(r), (0, 255, 0), 2)
#    #        n += 1    
#    
#    #return n >= 10 
#    #---------------------------------------------

#def move_to_whites(img):
#    """
#    Image -> None 
#    Click on a white region on the game(to avoid black circles)
#    """
#    screg = (13, 35, 510, 333) 
#    wimg = img.copy().crop(screg)
#    center = (265, 200)
#
#    dst = threshold(wimg, (200, 200, 200), 70)
#    pnts = tuple(zip(*np.where(dst.img == 255)[::-1]))
#    pnts = sorted(pnts, key=lambda s:dist(center, s))
#    for pnt in pnts:
#        x, y = pnt
#        regim = dst.img[y-15:y+15, x-15:x+15].copy()
#        regim[regim == 255] = 1
#        sm = regim.sum()
#        if sm >= 500:
#            click((pnt[0] + screg[0], pnt[1] + screg[1]))
#            sleep(2)
#            return
    
def main(prprf, knmns, hpth):
    """
    int > 1, bool, 99 > int > 0 -> None
    Main bot function, coordinates
    bot actions
    """
    global lsdrp, ranged, FATK, FRUN, DHTHRESH, HTHRESH

    world.full_reset()
    nhp = 3400 
    threshold = 100
    dst = 100 
    sdatk = True
    FRUN = True
    orc = 0
    lsdrp = time()
    latm = time()
    DHTHRESH = hpth

    while True:
        if dst is None:
            orc += 1
            if (orc >= 10 and (0 < nhp < 3400) and (nhp != 2720 or npcs.ded_record.get("fumus"))
                and (nhp != 2040 or npcs.ded_record.get("umbra")) and 
                (nhp != 1360 or npcs.ded_record.get("cruor")) and 
                (nhp != 680 or npcs.ded_record.get("glacies"))):
                if nhp > 200:
                    mm.nmove_to(MIDDLE)
                orc = 0
            elif orc >= 2:
                change_view()
        else:
            orc = 0

        img = get_region(gmreg)

        HTHRESH = DHTHRESH #(DHTHRESH if not ((npcs.ded_record.get("fumus") and 
                          #           (not npcs.ded_record.get("umbra")))
                          #           and (nhp >= 2040))
                          #          else DHTHRESH + 20)

        php = player.hp(img)
        php = 99 if php is None else php

        dst, npos = nex.distance(img) 

        if not (dst is None) and (threshold >= 20):
            if dst < 100:
                st = 0.1
                if (php < HTHRESH and nhp > 200):# or ((0 < nhp < 100) and (nhp % 20 != 0)):
                    mm.nmove_to(closest_corner(npos))
                    st = 0.5 
                
                pryl = player.prayer_on(prprf)
                if False in pryl:
                    qk_prayer(pryl, prprf)
                else:
                    press("f1")

                #print("Nex too close moving away...")
                sleep(st)
                sdatk = True

        # ---- Image Saving -----------------
        #if dst is None:
        #    imwrite("new_train/{}.png".format(SIND), img.img)
        #    SIND += 1
        # ----------------------------------

        pryl = player.prayer_on(prprf)
        if False in pryl:
            qk_prayer(pryl, prprf)
            if player.prayer(img) == 0:
                use_rest(img)
                sleep(0.1)
        else:
            press("f1")
            sleep(0.1)

        if not (php is None) and php < HTHRESH:
            if not use_sara(img):
                if nhp > 300 and php < 40:
                    flee()
                    return
            else:
                #print("HP low, using sara pot...")
                sdatk = True
                sleep(0.1)
        else:
            if player.prayer(img) < PTHRESH or (ranged < 70):
                if not use_rest(img):
                    if not npcs.ded_record.get("cruor"):
                        flee()
                        return
                else:
                    #print("Prayer low, using restore pot...")
                    sdatk = True
                    sleep(0.1)

        nhp = nex.hp(img)

        if knmns:
            if npcs.ded_record.get("fumus") != True:
                if threshold >= 80 and (nhp == 2720 or (nhp > 2720 and threshold == 80)):
                    threshold = 80
                    sdatk = True
                    if attack_npc("fumus"):
                        #print("Looking for: fumus") 
                        continue
            if npcs.ded_record.get("umbra") != True:
                if threshold >= 60 and (nhp == 2040 or (nhp > 2040 and threshold == 60)):
                    threshold = 60
                    sdatk = True
                    if php < HTHRESH:
                        continue
                    elif attack_npc("umbra"):
                        #print("Looking for: umbra") 
                        continue
            if npcs.ded_record.get("cruor") != True:
                if threshold >= 40 and (nhp == 1360 or (nhp > 1360 and threshold == 40)):
                    threshold = 40
                    sdatk = True
                    if attack_npc("cruor"):
                        #print("Looking for: cruor")
                        continue
            if npcs.ded_record.get("glacies") != True:
                if threshold >= 20 and (nhp == 680 or (nhp > 680 and threshold == 20)):
                    threshold = 20
                    sdatk = True
                    if attack_npc("glacies"):
                        #print("Looking for: glacies")
                        continue

        if nhp != 0:
            if nhp < 100:
                mm.reset_comp()
                click((265, 200), times=3, delay=0.1, quick=True)
            elif sdatk or ((time() - latm) > 5):
                #print("Looking for: nex")
                if attack_nex():
                    sdatk = False
                    latm = time()
        elif mm.nget_pos() is None:
                return
        else:
            threshold = 100
            sdatk = True
            if (time() - lsdrp) > 30:
                #print("Collecting loot...")
                #tbd = time()
                mm.reset_comp()
                click((265, 200), times=3, delay=0.1, quick=True)
                drop_empty(img)
                #stm = 4 - (time() - tbd)
                #sleep(stm if stm >= 0 else 0)
                tries = 0
                fnd = True 
                while look_for(nxcmim, get_region(nex.screg)) is None:
                    tries += 1
                    if tries > 40:
                        fnd = False
                        break
                    sleep(0.1)

                if fnd: 
                    player.drop_c -= world.collect_items(5)

                lsdrp = time()
                FATK = True
                FRUN = False

                if player.sara_pots(img)[0] < 4 or player.rest_pots(img)[0] < 2:
                    npcs.ded_record = {}
                    npcs.reset_count()
                    flee()
                    return
                sleep(1)
            mm.nmove_to(corners["tl"])
            npcs.ded_record = {}
            npcs.reset_count()

    
if __name__ == "__main__":
    reset_window()
    #img = get_region(gmreg)
    main(1, True, 80)
    #reset_window()
    #mm.reset_comp()
    #press("f3")
    ##qk_prayer((True, False), 1)
    #qk_prayer((True, False), 2)
    #print(player.prayer_on(2))
    #main()
    #import pnmm
    #flee()
    #pnmm.pre_nav(True)
    

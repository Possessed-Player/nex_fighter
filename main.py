import pprep, tree, pnmm, bot#, essence
from cvbot.keyboard import combo_press

def save_prefs(prfs):
    with open("prefs.txt", "w") as f:
        f.write(("{}," * len(prfs))[:-1].format(*prfs))

def read_prefs():
    with open("prefs.txt", "r") as f:
        rd = f.read()

    rc, rp, ls, ht = rd.split(",")
    return rc == "True", int(rp), ls == "True", int(ht)

if __name__ == "__main__":
    # TESTING PART
    #print(read_prefs())
    #---------------------------------------------------------------------
    bot.reset_window()
    print("\n\n")
    dfans = input("<Press any key to start with saved preferences>\n" + \
                  "(Press P followed by enter to edit preferences)")
    if dfans.lower() == "p":
        clnans = ""
        while not (clnans in ("g", "c")):
            clnans = input("For global nex type 'g' for clan type 'c'(followed by enter): ").lower()

        clan = clnans == "c"


        prans = ""
        while not (prans in ("e", "r")):
            prans = input("For Eagle Eye type 'e' for Rigour type 'r'(followed by enter): ").lower()

        pryr = 1 if prans == "e" else 2

        nmans = ""
        while not (nmans in ("i", "k")):
            nmans = input("To ignore nex minions type 'i' to kill nex minions type 'k'(followed by enter): ").lower()

        knm = nmans == "k"

        hpans = ""
        while True:
            try:
                hpans = int(input("Type hp to heal at(followed by enter): "))
                break
            except:
                continue

        hpth = hpans

        save_prefs((clan, pryr, knm, hpans))
    else:
        clan, pryr, knm, hpth = read_prefs()

    while True:
        pprep.main()
        if tree.main():
            #if essence.count() < 30:
            #    print("[INFO] Out of essence, exitting...")
            #    break
            if pnmm.main(clan):
                #try:
                while True:
                    if bot.mm.current_loc() != "home":
                        if bot.mm.nget_pos(False) is None:
                            if pnmm.pre_nav(skip=True):
                                combo_press("ctrl+q")
                                if pnmm.nex_door(clan):
                                    bot.main(pryr, knm, hpth)
                                else:
                                    break
                            else:
                                break
                        else:
                            bot.main(pryr, knm, hpth)
                    else:
                        break
                #except Exception as e:
                #    print(e)

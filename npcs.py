from cvbot.colors import count_clr
from cvbot.images import Image

ded_record = {}
ccounts = {"fumus":  0,
           "umbra":  0,
           "cruor":  0,
           "glacies":0}
npcs = {"fumus":((230, 140), #(212, 150), (240, 142), (210, 154)) ,
                 (71, 77)),   #(75, 73),   (67, 77),   (75, 73))),

        "umbra":((323, 153), #(334, 160), (308, 140)), 
                 (139, 73)),  #(135, 69),  (143, 77))),

        "cruor":((331, 248), #(334, 264), (347, 246)), 
                 (139, 141)), #(139, 137), (135, 141))),

        "glacies":((201, 262), #(188, 244), (216, 283)), 
                   (75, 137))}#, (79, 141), (71, 133)))}

def reset_count():
    """
    None -> None
    Reset the click count for all npcs to 0
    """
    global ccounts

    ccounts = {"fumus":  0,
               "umbra":  0,
               "cruor":  0,
               "glacies":0}

def npc_dead(cpos, img):
    """
    Point, img -> bool
    Detect on given image whether nex npc 
    with is dead or not
    Return True if given npc is dead
    """
    box = (-30, 10, -50, 55)
    timg = Image(img.img[cpos[1]+box[0]:cpos[1]+box[1], 
                         cpos[0]+box[2]:cpos[0]+box[3]])

    rc = count_clr(timg, (0, 0, 255))
    gc = count_clr(timg, (0, 255, 0))

    return (rc > 0 and ((401 > rc > 380) or gc < 15))

if __name__ == "__main__":
    from cvbot.io import read_img
    from sys import argv
    tnpc = "nex npc"
    oimg = read_img("test ({}).png".format(argv[1]))
    oimg.show()
    res = npc_dead((387, 210), oimg) 
    print(tnpc, "is", "dead" if res else "alive")

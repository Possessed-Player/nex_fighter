from cvbot.colors import count_clr
from cvbot.capture import get_region
from cvbot.nums import nread, init_reader


init_reader("src/", (255, 255, 255)) # Path to digits images,
ITEM_DESC_REG = (47, 39, 103, 16)    # Second arguement is color of number
ITEM_DESC_CLR = (64, 144, 255)
BOSS_HP_REG = (231, 80, 91, 8)

def is_item():
    """
    None -> bool
    Return True if current hovered on
    position have an item on it
    """
    img = get_region(ITEM_DESC_REG)
    cnt = count_clr(img, ITEM_DESC_CLR)
    return cnt > 100

if __name__ == "__main__":
    while True:
        img = get_region(BOSS_HP_REG)
        nex_hp = nread(img)
        print("  {}  ".format(nex_hp), end="\r")

from cvbot.colors import count_clr
from cvbot.capture import get_region


ITEM_DESC_REG = (47, 39, 103, 16)    # Second arguement is color of number
ITEM_DESC_CLR = (64, 144, 255)

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
    from time import sleep
    while True:
        print(is_item())
        sleep(1)

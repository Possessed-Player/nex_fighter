from cvbot.colors import count_clr
from cvbot.capture import get_region
from cvbot.nums import nread, init_reader
from cvbot.yolo.ai import init_model, detect


ITEM_DESC_REG = (47, 39, 103, 16)    # Second arguement is color of number
ITEM_DESC_CLR = (64, 144, 255)
GM_REG        = (12, 34, 512, 335)
BOSS_HP_REG = (231, 80, 91, 8)

init_model("models/nex_tiny.onnx", "nex")
init_reader("src/", (255, 255, 255)) # Path to digits images
                                     # Second argument is thresholding color

def is_item():
    """
    None -> bool
    Return True if current hovered on
    position have an item on it
    """
    img = get_region(ITEM_DESC_REG)
    cnt = count_clr(img, ITEM_DESC_CLR)
    return cnt > 100

def nex_pos():
    """
    None -> None | Point
    Find nex in 'GM_REG' on screen and return
    its position if found, None if not found
    """
    img = get_region(GM_REG)
    res = detect(img, 0.5)
    if res:
        pos, _, _ = res[0]
        img.img[pos[1] + ((pos[3] - pos[1]) // 2), :] = np.array((0, 0, 255, 255), dtype=img.img.dtype)
        img.img[:, pos[0] + ((pos[2] - pos[0]) // 2)] = np.array((0, 0, 255, 255), dtype=img.img.dtype)
        print(res)
        imshow("test", img.img)
        waitKey(1)

def nex_hp():
    img = get_region(BOSS_HP_REG)
    return nread(img)

if __name__ == "__main__":
    from cv2 import imshow, waitKey
    import numpy as np
    while True:
        nex_pos()

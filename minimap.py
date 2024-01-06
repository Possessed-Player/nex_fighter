from cvbot.io import read_img
from cvbot.match import look_for
from cvbot.capture import get_region
import numpy as np


mmreg = (573, 40, 161, 150) # (x, y, width, height) of the screen region
reg = (26, 21, 104, 92)
fmapimg = read_img("src/full_map.png")

def process(img):
    """
    Image -> Image
    Remove noise from nex minimap image
    and return a clean image
    """
    global reg

    # Crop the outer extra parts of the minimap
    cimg = img.crop(reg)

    # Remove current move flag(removed by turning it gray)
    mask = np.logical_and(cimg.img[:, :, 1] < 30, cimg.img[:, :, 0] > 150)
    cimg.img[mask] = np.array((200, 200, 200), dtype=cimg.img.dtype)
    # Remove other small unnecessary part of the room
    maskb = np.logical_and(cimg.img[:, :, 2] > 80, cimg.img[:, :, 0] < 150)
    cimg.img[maskb] = np.array((200, 200, 200), dtype=cimg.img.dtype)
    # add 255 when not loading images from disk

    # Make sure the highest gray color is 200, and turn white color to gray
    cimg.img[cimg.img > 200] = 200
    cimg.show()

    return cimg


def get_pos():
    global fmapimg, mmreg

    # Get a screenshot of the minimap
    mmimg = get_region(mmreg)
    # ---- Testing code --------
    #mmimg.show()
    # --------------------------
    pmmimg = process(mmimg)

    # offset to actual position
    ofst = -1, 6

    pos = look_for(pmmimg, fmapimg, 0.6)
    if not (pos is None):
        pos = pos[0] + ofst[0], pos[1] + ofst[1]
        # -------- Testing code -------------
        x, y = pos
        # This is actually loaded from disk
        fmc = fmapimg.copy()
        fmc.img[y, :] = np.array((0, 0, 255), dtype=fmapimg.img.dtype)
        fmc.img[:, x] = np.array((0, 0, 255), dtype=fmapimg.img.dtype)

        # This will make the window automatically update itself
        # with waitKey(1), it will wait for 1 millisecond for
        # user input then immediately update itself if no input happened
        cv.imshow("testing", fmc.img)
        cv.waitKey(1)
        # ------------------------------

    return pos

if __name__ == "__main__":
    import cv2 as cv
    from cvbot import windows
    # ----- Make game window position to top-left corner -------
    #win = windows.get_window("runewild")
    #win.repos(0, 0)
    # ---------------------------------------------------------

    img = read_img("images/2600.png")
    process(img)
    #while True:
    #    get_pos()

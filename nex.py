import cv2
import numpy as np
import onnxruntime as ort
#from cvbot.yolo import ai
from time import time
from cvbot.nums import nread, init_reader
from math import dist


init_reader("src/", (255, 255, 255))
reg = (238, 80, 80, 8)
screg = (0, 0, 770, 530) #(13, 35, 510, 333) 
w = "cmodels/nex_tiny_1.onnx"
providers = ['CPUExecutionProvider'] #['CUDAExecutionProvider', 'CPUExecutionProvider']
session = ort.InferenceSession(w, providers=providers)

def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding

    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return im, r, (dw, dh)
#
def ls_pos(img, thresh):
    global session

    outname = [i.name for i in session.get_outputs()]
    outname
    inname = [i.name for i in session.get_inputs()]
    inname

    img = img.img
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = img.copy()
    image, ratio, dwdh = letterbox(image, auto=False)
    image = image.transpose((2, 0, 1))
    image = np.expand_dims(image, 0)
    image = np.ascontiguousarray(image)

    im = image.astype(np.float32)
    im /= 255
    im.shape

    inp = {inname[0]:im}
    #st = time()
    outputs = session.run(outname, inp)[0]
    #et = time()
    #print("Time ->", round(et - st, 3))

    if len(outputs):
        outputs = tuple(outputs)
        outputs = sorted(outputs, key=lambda x: x[6], reverse=True)

        out = outputs[0]
        _, x0, y0, x1, y1, _, scr = out
        if scr < thresh:
            return None
        box = np.array([x0,y0,x1,y1])
        box -= np.array(dwdh*2)
        box /= ratio
        box = box.round().astype(np.int32).tolist()
        pos = (box[0] + ((box[2] - box[0]) // 2), 
               box[1] + ((box[3] - box[1]) // 2))
        return pos
    else:
        return None

def hp(img):
    """
    Image -> int[0-100]
    Read Nex hp from the scene
    DO NOT use outside of nex's room
    """
    global reg

    img = img.crop(reg)
    nhp = nread(img)

    return 0 if nhp is None else nhp

    # ----- Old Logic -----------
    #wts = np.sum(cv.inRange(img.img, (0, 255, 0, 255), (0, 255, 0, 255))) // 255
    #return (wts / 230) * 100
    # ---------------------------

def position(img, thresh=0.5):
    """
    Image, float -> Point | None
    Find nex location on the screen/scene
    and return as a region
    returns None if nex location couldn't be found
    with confidence higher or equal to 'thresh'
    """
    global screg, lpd, LS

    return ls_pos(img, thresh)

    #img = img.crop(screg)
    #results = ai.detect(img, thresh)
    #box = None

    #if results:
    #    res = results[0]
    #    box = res[0] 

    #    return (box[0] + (box[2] // 2) + screg[0], box[1] + (box[3] // 2) + screg[1]) 
    #else:
    #    return None

def distance(img, pos=None):
    """
    Image | None, pos | None -> int, Point | None, None
    Return the distance from nex
    Return None if nex wasn't found
    """
    center = 265, 200
    if pos is None:
        pos = position(img)

    if not (pos is None):
        return dist(pos, center), (pos[0] - center[0], pos[1] - center[1])
    else:
        return None, None

if __name__ == "__main__":
    from cvbot.capture import screenshot
    print(hp(screenshot()))

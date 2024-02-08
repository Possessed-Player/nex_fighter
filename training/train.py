from os import mkdir, system, listdir
from os.path import isdir, join, isfile


def partition(path):
    """
    path -> bool 
    Put image and label files in 'path' in two folders train/val
    based on the ratio 4(train):1(val)
    Return True  - if the partitioning was successful
           False - if it got an error at some point
    """
    files = [] 

    fns = [b[:-4] for b in filter(lambda a: a != "classes.txt" and a.endswith(".txt"), listdir(path))]

    for fn in fns:
        imgp = fn + ".png" 
        lblp = fn + ".txt"
        if isfile(join(path, imgp)):
            files.append((imgp, lblp))
        else:
            print("CORRESPONDING IMAGE FILE IS NOT FOUND!")
            quit()

    n = len(files)
    
    if n < 5:
        print("INSUFFICIENT NUMBER OF LABELLED IMAGES, 5 IS THE MINIMUM NUMBER")
        return False

    tsn = round(n * 0.2)

    fns = {}
    fns["val"] = files[:tsn]
    fns["train"]  = files[tsn:]

    try:
        for fdn, ilfns in fns.items():
            if not isdir(join(path, fdn)):
                mkdir(join(path, fdn))
            for ilfn in ilfns: 
                for f in ilfn:
                    src = join(path, f)
                    dst = join(path, fdn, f)
                    if system('copy "{}" "{}"'.format(src, dst)) != 0:
                        raise Exception("")
    except Exception as e:
        print(e)
        return False

    return True

if __name__ == "__main__":
    partition("train")

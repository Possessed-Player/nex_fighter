from cvbot.capture import get_region
from cvbot.colors import threshold


reg = 68, 151, 64, 15

def count():
    """
    None -> int
    Return Ancient Essence count
    """
    from cvbot.ai import init_ocr, read

    init_ocr(['en'], model_path="src/")
    img = get_region(reg)
    res = read(img, "0123456789")

    try:
        return int(res) 
    except:
        return 30

if __name__ == "__main__":
    print(count())

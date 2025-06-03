import pyautogui
from PIL import Image

import numpy as np

APPLES = {
    i: Image.open(f'./src/apples/{i}.png') for i in range(1, 10)
}

def detect_apples():
    """
    it takes screenshot of the current screen, and returns all detected apples with its value and coordinate.
    """
    detected_apples = []
    for i, apple in APPLES.items():
        bboxes = pyautogui.locateAllOnScreen(apple ,confidence=0.99) # it returns coco format bboxes of class pyscreeze.Box
        detected_apples.extend([(tuple(bbox), i) for bbox in bboxes])

    return detected_apples

def apples_to_arr(detected_apples):
    assert len(detected_apples) == 170

    # each element is ((x, y, w, h), apple_value)
    sorted_detected_apples = sorted(detected_apples, key=lambda x: (x[0][1], x[0][0])) # sort by y first, then by x
    apples_list = [a[1] for a in sorted_detected_apples]

    apples_arr = np.array(apples_list, dtype=np.uint8).reshape(10, 17)
    return apples_arr
    

if __name__ == '__main__':    
    detected_apples = detect_apples()
    apples_arr = apples_to_arr(detected_apples)

    print(apples_arr)
import pyautogui
from PIL import Image

import numpy as np
import os

APPLES = {
    i: Image.open(f'./src/apples/{i}.png') for i in range(1, 10)
}

def detect_apples():
    """
    takes screenshot of the current screen, and returns all detected apples with its value and coordinate.
    """
    detected_apples = []
    for i, apple in APPLES.items():
        bboxes = pyautogui.locateAllOnScreen(apple ,confidence=0.99) # it returns coco format bboxes of class pyscreeze.Box
        detected_apples.extend([(tuple(bbox), i) for bbox in bboxes])

    return detected_apples

def parse_detected_apples(detected_apples):
    """
    takes list of detected apples of format ((x, y, w, h), apple_value)
    returns two 2d numpy array representing the apples on the board, and coordinates of each apple's center.  
    """
    assert len(detected_apples) == 170

    # each element is ((x, y, w, h), apple_value)
    sorted_detected_apples = sorted(detected_apples, key=lambda x: (x[0][1], x[0][0])) # sort by y first, then by x
    apples_list = [a[1] for a in sorted_detected_apples]
    coords_list = [a[0][:2] for a in sorted_detected_apples]
    wh_list = [a[0][2:] for a in sorted_detected_apples]

    apples_arr = np.array(apples_list, dtype=np.uint8).reshape(10, 17)
    coords_arr = np.array(coords_list, dtype=np.int32)
    wh_arr = np.array(wh_list, dtype=np.int32)
    center_coords_arr = (coords_arr + wh_arr/2).reshape(10, 17, -1)
    
    return apples_arr, center_coords_arr

def parse_screen():
    apples = detect_apples()
    apples_arr, center_coords_arr = parse_detected_apples(apples)

    return apples_arr, center_coords_arr
    

if __name__ == '__main__':    
    detected_apples = detect_apples()
    apples_arr, _ = parse_detected_apples(detected_apples)

    # print(apples_arr)
    os.makedirs('./test_case', exist_ok=True)
    np.savetxt('test_case/case_01.txt', apples_arr, fmt='%d' ,delimiter=' ')
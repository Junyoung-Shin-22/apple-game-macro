import numpy as np

def find_first_available_box_index(apples_arr):
    h, w = apples_arr.shape

    for i in range(h):
        for j in range(w):
            for k in range(i, h):
                for l in range(j, w):
                    box = apples_arr[i:k, j:l]
                    if box.sum() == 10: return (i, k, j, l)
                    if box.sum() > 10 : break

def greedy_solver(apples_box):
    apples_box = apples_box.copy()
    score = 0
    solution = []

    while True:
        box_index = find_first_available_box_index(apples_box)
        if box_index is None: break

        solution.append(box_index)
        i, k, j, l = box_index


        score += (apples_box[i:k, j:l] != 0).sum() # increse score by number of removed apples
        apples_box[i:k, j:l] = 0 # fill selected area to 0
    
    return dict(solution=solution, score=score)

if __name__ == '__main__':
    test_case = np.loadtxt('./test_case/case_01.txt', dtype=np.uint8, delimiter=' ')
    print(test_case)

    # box = find_first_available_box(test_case)
    # print(box)
    print(greedy_solver(test_case))
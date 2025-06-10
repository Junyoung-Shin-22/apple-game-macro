import numpy as np

def _optimize_index(apples_arr, index):
    """
    optimizing index by removing preceding zeros area.
    """

    i, k, j, l = index
    
    box = apples_arr[i:k, j:l]
    nonzero_i, nonzero_j = box.nonzero()
    i, j = i+nonzero_i.min(), j+nonzero_j.min()

    return i, k, j, l

def find_first_available_box_index(apples_arr):
    h, w = apples_arr.shape

    for i in range(h):
        for j in range(w):
            for k in range(i, h+1):
                for l in range(j, w+1):
                    box = apples_arr[i:k, j:l]
                    if box.sum() == 10: 
                        optimized_index = _optimize_index(apples_arr, (i, k, j, l))
                        return optimized_index
                    if box.sum() > 10 : break

def find_all_available_box_indices(apples_arr):
    h, w = apples_arr.shape
    box_indices = []

    for i in range(h):
        for j in range(w):
            for k in range(i, h+1):
                for l in range(j, w+1):
                    box = apples_arr[i:k, j:l]
                    if box.sum() == 10: 
                        optimized_index = _optimize_index(apples_arr, (i, k, j, l))
                        if optimized_index not in box_indices:
                            box_indices.append(optimized_index)
                    if box.sum() > 10 : break
    
    return box_indices

def greedy_solver(apples_arr):
    apples_arr = apples_arr.copy()
    score = 0
    solution = []

    while True:
        box_index = find_first_available_box_index(apples_arr)
        if box_index is None: break

        i, k, j, l = box_index

        solution.append((i, k, j, l))
        score += (apples_arr[i:k, j:l] != 0).sum() # increse score by number of removed apples
        
        apples_arr[i:k, j:l] = 0 # fill selected area to 0
    
    return dict(solution=solution, score=score)

def dfs_solver(apples_arr):
    def _dfs(apples_arr, solution=[], score=0, depth=0):
        pass
    
    pass

if __name__ == '__main__':
    test_case = np.loadtxt('./test_case/case_01.txt', dtype=np.uint8, delimiter=' ')
    print(test_case)

    # box = find_first_available_box(test_case)
    # print(box)
    print(greedy_solver(test_case))
import numpy as np
from tqdm import tqdm

def _optimize_move(apples_arr, move):
    """
    optimizing move by removing preceding zeros area.
    """

    i, k, j, l = move
    
    box = apples_arr[i:k, j:l]
    nonzero_i, nonzero_j = box.nonzero()
    i, j = i+nonzero_i.min(), j+nonzero_j.min()

    return (i, k, j, l)

def find_first_available_move(apples_arr):
    h, w = apples_arr.shape

    for i in range(h):
        for j in range(w):
            for k in range(i, h+1):
                for l in range(j, w+1):
                    box = apples_arr[i:k, j:l]
                    if box.sum() == 10: 
                        optimized_move = _optimize_move(apples_arr, (i, k, j, l))
                        return optimized_move
                    if box.sum() > 10 : break

def greedy_solver(apples_arr):
    apples_arr = apples_arr.copy()
    solution = []
    score = 0

    while True:
        move = find_first_available_move(apples_arr)
        if move is None: break

        solution.append(move)

        i, k, j, l = move
        score += (apples_arr[i:k, j:l] != 0).sum() # increse score by number of removed apples
        apples_arr[i:k, j:l] = 0 # fill selected area to 0
    
    return dict(solution=solution, score=score)

def _get_integral_image(arr):
    integral = np.zeros((arr.shape[0] + 1, arr.shape[1] + 1), dtype=np.uint32)
    integral[1:, 1:] = np.cumsum(np.cumsum(arr, axis=0), axis=1)

    return integral

def _get_box_sum(integral_image, i, k, j, l):
    box_sum = (integral_image[i, j] + integral_image[k, l] - integral_image[i, l] - integral_image[k, j])
    
    return box_sum

def find_all_available_moves(apples_arr):
    h, w = apples_arr.shape
    moves = []

    integral_image = _get_integral_image(apples_arr)

    for i in range(h):
        for j in range(w):
            for k in range(i, h+1):
                for l in range(j, w+1):
                    box_sum = _get_box_sum(integral_image, i, k, j, l)
                    if box_sum == 10: 
                        optimized_move = _optimize_move(apples_arr, (i, k, j, l))
                        if optimized_move not in moves:
                            moves.append(optimized_move)
                    if box_sum > 10 : break
    
    return moves

def dfs_solver(apples_arr, target_score, verbose=True):
    visited = set()
    global_best_score = 0

    def _dfs(_apples_arr, solution=[], score=0, depth=0):
        nonlocal global_best_score

        # visit-based pruning
        state = hash(_apples_arr.tobytes())
        if state in visited: # if this state is already visited
            return dict(solution=[], score=0)
        else:
            visited.add(state)

        # rule-based pruning
        remaining_apples = (_apples_arr != 0).sum()
        sum_apples = _apples_arr.sum()
        ub = min(remaining_apples, 10 * (sum_apples//10))# set upper bound
        if score + ub <= global_best_score: # this branch can be pruned safely
            return dict(solution=[], score=0)
        
        moves = find_all_available_moves(_apples_arr)

        # treat leaf node
        if score >= target_score or not moves:
            return dict(solution=solution, score=score)
        
        moves.sort(key=lambda m: (m[1]-m[0])*(m[3]-m[2])) # heuristic: prefer smaller area
        
        # run dfs recursively
        best_solution = None
        best_score = 0
        pbar = tqdm(moves, position=depth, desc=f'depth: {depth}, best_score: {best_score}', leave=False, disable=(not verbose))
        for move in pbar:
            i, k, j, l = move
            box = _apples_arr[i:k, j:l].copy()
            score_to_add = (box != 0).sum()
            _apples_arr[i:k, j:l] = 0

            res = _dfs(_apples_arr, solution=solution+[move,], score=score+score_to_add, depth=depth+1)

            if res['score'] > best_score:
                best_solution = res['solution']
                best_score = res['score']
            
            _apples_arr[i:k, j:l] = box
            pbar.set_description(f'depth: {depth}, best_score: {best_score}')

            # early stopping
            if best_score >= target_score: break
        
        if best_score > global_best_score:
            global_best_score = best_score

        return dict(solution=best_solution, score=best_score)
    
    _apples_arr = apples_arr.copy()
    res = _dfs(_apples_arr)
    return res

if __name__ == '__main__':
    test_case = np.loadtxt('./test_case/case_01.txt', dtype=np.uint8, delimiter=' ')
    print(test_case)

    # box = find_first_available_box(test_case)
    # print(box)
    print(dfs_solver(test_case))
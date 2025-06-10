import numpy as np

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

def find_all_available_moves(apples_arr):
    h, w = apples_arr.shape
    moves = []

    for i in range(h):
        for j in range(w):
            for k in range(i, h+1):
                for l in range(j, w+1):
                    box = apples_arr[i:k, j:l]
                    if box.sum() == 10: 
                        optimized_move = _optimize_move(apples_arr, (i, k, j, l))
                        if optimized_move not in moves:
                            moves.append(optimized_move)
                    if box.sum() > 10 : break
    
    return moves

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

def dfs_solver(apples_arr):
    visited = set()

    def _dfs(apples_arr, solution=[], score=0, depth=0):
        state = hash(str(apples_arr))
        if state in visited: # if this state is already visited
            return dict(solution=[], score=0)
        else:
            visited.add(state)
        
        moves = find_all_available_moves(apples_arr)
        if not moves: # if this state is "leaf"
            return dict(solution=solution, score=score)
        
        # run dfs recursively
        best_solution = None
        best_score = 0
        for move in moves:
            apples_arr_next = apples_arr.copy()

            i, k, j, l = move
            score_to_add = apples_arr_next[i:k, j:l]
            apples_arr_next[i:k, j:l] = 0

            res = _dfs(apples_arr_next, solution=solution+[move,], score=score+score_to_add, depth=depth+1)

            if res['score'] > best_score:
                best_solution = res['solution']
                best_score = res['score']
        
        return dict(solution=best_solution, score=best_score)
    
    res = _dfs(apples_arr)
    return res

if __name__ == '__main__':
    test_case = np.loadtxt('./test_case/case_01.txt', dtype=np.uint8, delimiter=' ')
    print(test_case)

    # box = find_first_available_box(test_case)
    # print(box)
    print(greedy_solver(test_case))
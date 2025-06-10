import pyautogui
import argparse

from screen import parse_screen
from solver import greedy_solver, dfs_solver

def main(target_score):
    apples_arr, coords_arr = parse_screen()
    print(apples_arr)

    # output = greedy_solver(apples_arr)
    output = dfs_solver(apples_arr, target_score, verbose=True)
    solution, score = output['solution'], output['score']

    print('[solution]')
    for move in solution:
        print(move)

    print(f'executing solution. score will be: {score}')
    for move in solution:
        i1, i2, j1, j2 = move
        x1, y1 = coords_arr[i1, j1]
        x2, y2 = coords_arr[i2-1, j2-1]

        x1, y1 = x1 - 15, y1 - 15
        x2, y2 = x2 + 15, y2 + 15
        d = ((x1-x2)**2 + (y1-y2)**2) ** 0.5

        pyautogui.moveTo(x1, y1, duration=0.1)
        pyautogui.dragTo(x2, y2, d/100, button='left')
        # print(x1, y1, x2, y2, d)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_score', '-t', type=int, default=100)
    args = parser.parse_args()

    main(target_score=args.target_score)
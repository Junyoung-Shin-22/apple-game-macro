from PIL import Image
import os

# constants
left, top = 72, 74
right, bottom = 627, 400

apple_w = 27
apple_h = 29

margin_x = 6
margin_y = 4

image = Image.open('./canvas.png')

apples = [
    [image.crop([x, y, x+apple_w, y+apple_h]) for x in range(left, right, apple_w+margin_x)]
        for y in range(top, bottom, apple_h+margin_y)
]

if __name__ == '__main__':
    # manually provide apple indices
    apple_indices = {
        1: (0, 10),
        2: (0, 4),
        3: (0, 3),
        4: (0, 8),
        5: (0, 0),
        6: (0, 2),
        7: (1, 2),
        8: (0, 6),
        9: (0, 12),
    }
    
    os.makedirs('apples', exist_ok=True)

    for x, (i, j) in apple_indices.items():
        apples[i][j].save(f'apples/{x}.png')
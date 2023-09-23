import numpy as np
from CustomWidgets import HomeCard
global x_coord
x_coord = 0
global y_coord
y_coord = 0


def add_to_grid(root, card_name, card_color, num_cards, super_root):
    global x_coord, y_coord
    if x_coord < 740:
        HomeCard(root, name=card_name, color=card_color, count=num_cards,
                 root=root, superroot=super_root).place(x=x_coord, y=y_coord)
        x_coord += 370
    elif x_coord == 740:
        HomeCard(root, name=card_name, color=card_color, count=num_cards,
                 root=root, superroot=super_root).place(x=x_coord, y=y_coord)
        x_coord = 0
        y_coord += 170


def set_center(master_width, master_height, child_width, child_height):
    CENTER_WIDTH = int(np.floor(np.divide(master_width, 2)) - np.floor(np.divide(child_width, 2)))
    CENTER_HEIGHT = int(np.floor(np.divide(master_height, 2)) - np.floor(np.divide(child_height, 2)))
    return (CENTER_WIDTH, CENTER_HEIGHT)


import random
import numpy as np
import pygame

maze_width = 20
maze_height = 20
num_cells = maze_height * maze_width

## direction of movement
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

maze_matrix = [[0 for x in range(maze_width)] for y in range(maze_height)] # 0: unvisited, 1: visited
maze_matrix[0][0] = 1
not_finished = True
path_stack = []
wall_stack = [] # walls to be removed
start_cell = (0, 0)
current_cell = (0, 0)
path_stack.append(start_cell)
count = 0

def custom_random(exclude_dir):
    rand = random.randint(0, 3)
    return custom_random(exclude_dir) if rand in exclude_dir else rand

while not_finished:
    ## termination condition
    if path_stack == []:  # or should count the num of visited cells??
        not_finished = False
        break

    ##  check available neighbor cells
    ##  if non, pop current cell
    ##  else, mark as current cell, put into stack
    exclude_dir = []
    if current_cell[0] == 0 or (current_cell[0] > 0 and maze_matrix[current_cell[0] - 1][current_cell[1]] == 1):
        exclude_dir.append(LEFT)
    if current_cell[0] == maze_width - 1 or (current_cell[0] < maze_width and maze_matrix[current_cell[0] + 1][current_cell[1]] == 1):
        exclude_dir.append(RIGHT)
    if current_cell[1] == 0 or (current_cell[1] > 0 and maze_matrix[current_cell[0]][current_cell[1] - 1] == 1):
        exclude_dir.append(UP)
    if current_cell[1] == maze_height - 1 or (current_cell[1] < maze_height and maze_matrix[current_cell[0]][current_cell[1] + 1] == 1):
        exclude_dir.append(DOWN)

    # print(current_cell)
    if len(exclude_dir) == 4:
        current_cell = path_stack.pop()
        continue
    
    dir = custom_random(exclude_dir)

    new_cell = current_cell
    old_cell = current_cell
    if dir == LEFT:
        new_cell = (current_cell[0] - 1, current_cell[1])
    elif dir == RIGHT:
        new_cell = (current_cell[0] + 1, current_cell[1])
    elif dir == UP:
        new_cell = (current_cell[0], current_cell[1] - 1)
    else:
        new_cell = (current_cell[0], current_cell[1] + 1)

    current_cell = new_cell
    wall = ((old_cell), (current_cell))
    wall_stack.append(wall)
    print(exclude_dir)
    print(dir)
    print(new_cell)
    print(wall_stack)
    print(path_stack)
    print(np.array(maze_matrix))
    print('\n')
    maze_matrix[current_cell[0]][current_cell[1]] = 1 # mark as visited
    path_stack.append(current_cell)
    count += 1

win_width = 500
win_height = 500

pygame.init()
win = pygame.display.set_mode((win_width, win_height))

run = True

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill((0))

    for i in range(0, maze_height + 1):
        for j in range(0, maze_width + 1):
            pygame.draw.rect(win, (0, 0, 255), (j * 20, i * 20, 5, 5))
            if (i == 0 or i == maze_height) and j < maze_width: # horizontal boundaries
                pygame.draw.rect(win, (0, 0, 255), (5 + j * 20, i * 20, 15, 5))
            if (j == 0 or j == maze_height) and i < maze_height: # vertical boundaries
                pygame.draw.rect(win, (0, 0, 255), (j * 20, 5 + i * 20, 5, 15))
            if i < maze_height and j < maze_width:  # horizontal walls
                pygame.draw.rect(win, (0, 0, 255), (5 + j * 20, i * 20, 15, 5))
            if j < maze_width and i < maze_height:  # vertical walls
                pygame.draw.rect(win, (0, 0, 255), (j * 20, 5 + i * 20, 5, 15))
    
    for item in wall_stack: # to remove walls
        wall_pos = tuple(np.subtract(item[1], item[0]))
        if wall_pos == (0, -1): # path going to left
            wall_reference = item[0] # to remove the wall on the left of old cell, right of current cell
            pygame.draw.rect(win, (0, 0, 0), (wall_reference[1] * 20, 5 + wall_reference[0] * 20, 5, 15))
        elif wall_pos == (0, 1): # path going to right
            wall_reference = item[1] # to remove the wall on the right fo old cell, left of current cell
            pygame.draw.rect(win, (0, 0, 0), (wall_reference[1] * 20, 5 + wall_reference[0] * 20, 5, 15))
        elif wall_pos == (-1, 0): # path going to up
            wall_reference = item[0] # to remove the wall above the old cell, below current cell
            pygame.draw.rect(win, (0, 0, 0), (5 + wall_reference[1] * 20, wall_reference[0] * 20, 15, 5))
        else:
            wall_reference = item[1] # to remove the wall above the old cell, below current cell
            pygame.draw.rect(win, (0, 0, 0), (5 + wall_reference[1] * 20, wall_reference[0] * 20, 15, 5))

    pygame.display.update()

pygame.quit()
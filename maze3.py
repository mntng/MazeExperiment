import pygame
import random
# import numpy as np 

maze_width = 8
maze_height = 8
num_cells = maze_height * maze_width

win_width = 500
win_height = 500

## direction of movement
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

## initialize maze matrix
maze_matrix = [[0 for x in range(maze_width)] for y in range(maze_height)] # 0: unvisited, 1: visited
maze_matrix[0][0] = 1 # starting point is visited
cell_stack = []
wall_stack = [] # walls to be removed
start_cell = (0, 0)
current_cell = (0, 0)
end_cell = (maze_width - 1, maze_height - 1)
cell_stack.append(start_cell)

## initialize path matrix for robot
path_matrix = [[0 for x in range(maze_width)] for y in range(maze_height)] # 0: unvisited, 1: visited
path_matrix[0][0] = 1
robot_path_stack = [] # path to be explored
robot_path_stack.append(start_cell)
robot_current_cell = start_cell
maze_not_finished = True
terminal_found = False
stop = False

def custom_random(exclude_dir):
    rand = random.randint(0, 3)
    return custom_random(exclude_dir) if rand in exclude_dir else rand

pygame.init()
win = pygame.display.set_mode((win_width, win_height))

run = True

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    win.fill((0))

    ### draw all the boundaries and walls
    for i in range(0, maze_height + 1):
        for j in range(0, maze_width + 1):
            pygame.draw.rect(win, (0, 0, 255), (j * 20, i * 20, 5, 5))
            if (i == 0 or i == maze_height) and j < maze_width: # horizontal boundaries
                pygame.draw.rect(win, (0, 0, 255), (5 + j * 20, i * 20, 15, 5))
            if (j == 0 or j == maze_width) and i < maze_height: # vertical boundaries
                pygame.draw.rect(win, (0, 0, 255), (j * 20, 5 + i * 20, 5, 15))
            if i < maze_height and j < maze_width:  # horizontal walls
                pygame.draw.rect(win, (0, 0, 255), (5 + j * 20, i * 20, 15, 5))
            if j < maze_width and i < maze_height:  # vertical walls
                pygame.draw.rect(win, (0, 0, 255), (j * 20, 5 + i * 20, 5, 15))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_i]:
        stop = True
    if keys[pygame.K_j]:
        stop = False

    ### create path and break walls ###
    if maze_not_finished and stop == False:
        if cell_stack == []:
            maze_not_finished = False
            continue

        ##  check available neighbor cells
        ##  if none, pop current cell
        ##  else, mark as current cell, put into stack
        exclude_dir = []
        if current_cell[0] == 0 or (current_cell[0] > 0 and maze_matrix[current_cell[1]][current_cell[0] - 1] == 1):
            exclude_dir.append(LEFT)
        if current_cell[0] == maze_width - 1 or (current_cell[0] < maze_width and maze_matrix[current_cell[1]][current_cell[0] + 1] == 1):
            exclude_dir.append(RIGHT)
        if current_cell[1] == 0 or (current_cell[1] > 0 and maze_matrix[current_cell[1] - 1][current_cell[0]] == 1):
            exclude_dir.append(UP)
        if current_cell[1] == maze_height - 1 or (current_cell[1] < maze_height and maze_matrix[current_cell[1] + 1][current_cell[0]] == 1):
            exclude_dir.append(DOWN)

        # print(current_cell)
        if len(exclude_dir) == 4:
            current_cell = cell_stack.pop()
            continue
        
        dir = custom_random(exclude_dir)

        new_cell = current_cell
        old_cell = current_cell
        wall = (current_cell, 'horizontal')

        if dir == LEFT:
            new_cell = (current_cell[0] - 1, current_cell[1])
            wall = (current_cell, 'horizontal') # horizontal path
        elif dir == RIGHT:
            new_cell = (current_cell[0] + 1, current_cell[1])
            wall = (new_cell, 'horizontal')
        elif dir == UP:
            new_cell = (current_cell[0], current_cell[1] - 1)
            wall = (current_cell, 'vertical') # vertical path
        else:
            new_cell = (current_cell[0], current_cell[1] + 1)
            wall = (new_cell, 'vertical')

        current_cell = new_cell
        # wall = ((old_cell), (current_cell))
        wall_stack.append(wall)
        # print(exclude_dir)
        # print(dir)
        # print(new_cell)
        # print(wall_stack)
        # print(cell_stack)
        # print(np.array(maze_matrix))
        # print('\n')
        maze_matrix[current_cell[1]][current_cell[0]] = 1 # mark as visited
        cell_stack.append(current_cell) 
        print(wall)

    # for item in wall_stack: # to remove walls
    #     wall_pos = tuple(np.subtract(item[1], item[0]))
    #     if wall_pos == (0, -1): # path going to left
    #         wall_reference = item[0] # to remove the wall on the left of old cell, right of current cell
    #         pygame.draw.rect(win, (0, 0, 0), (wall_reference[1] * 20, 5 + wall_reference[0] * 20, 5, 15))
    #     elif wall_pos == (0, 1): # path going to right
    #         wall_reference = item[1] # to remove the wall on the right fo old cell, left of current cell
    #         pygame.draw.rect(win, (0, 0, 0), (wall_reference[1] * 20, 5 + wall_reference[0] * 20, 5, 15))
    #     elif wall_pos == (-1, 0): # path going to up
    #         wall_reference = item[0] # to remove the wall above the old cell, below current cell
    #         pygame.draw.rect(win, (0, 0, 0), (5 + wall_reference[1] * 20, wall_reference[0] * 20, 15, 5))
    #     else:
    #         wall_reference = item[1] # to remove the wall above the old cell, below current cell
    #         pygame.draw.rect(win, (0, 0, 0), (5 + wall_reference[1] * 20, wall_reference[0] * 20, 15, 5))

    for item in wall_stack: # to remove walls
        wall_reference = item[0]
        if item[1] == 'horizontal':   # horizontal path
            pygame.draw.rect(win, (0, 0, 0), (wall_reference[0] * 20, 5 + wall_reference[1] * 20, 5, 15))
        else: # vertical path
            pygame.draw.rect(win, (0, 0, 0), (5 + wall_reference[0] * 20, wall_reference[1] * 20, 15, 5))
    
    #3 robot now starts to explore
    if maze_not_finished == False: 
        pygame.draw.rect(win, (255, 0, 0), (5 + robot_current_cell[0] * 20, 5 + robot_current_cell[1] * 20, 15, 15))
        
        if terminal_found == False:
            pygame.draw.rect(win, (255, 255, 255), (5 + end_cell[0] * 20, 5 + end_cell[1] * 20, 15, 15))
            if robot_current_cell == end_cell:
                terminal_found = True
                continue

            if robot_path_stack == []: # no more unvisited path
                terminal_found = True
                continue
        # print("access_stack:", access_stack)
        # print(np.array(path_matrix))
            if robot_current_cell[0] != 0 and \
            path_matrix[robot_current_cell[1]][robot_current_cell[0] - 1] == 0 and \
            (robot_current_cell, 'horizontal') in wall_stack:
                print("turn left")
                print(path_matrix[robot_current_cell[1]][robot_current_cell[0] - 1])
                robot_current_cell = (robot_current_cell[0] - 1, robot_current_cell[1]) # to left
                path_matrix[robot_current_cell[1]][robot_current_cell[0]] = 1
                robot_path_stack.append(robot_current_cell)

            elif robot_current_cell[0] != maze_width - 1 and \
            path_matrix[robot_current_cell[1]][robot_current_cell[0] + 1] == 0 and \
            ((robot_current_cell[0] + 1, robot_current_cell[1]), 'horizontal') in wall_stack:
                print("turn right")
                print(path_matrix[robot_current_cell[1]][robot_current_cell[0] + 1])
                robot_current_cell = (robot_current_cell[0] + 1, robot_current_cell[1]) # to right
                path_matrix[robot_current_cell[1]][robot_current_cell[0]] = 1
                robot_path_stack.append(robot_current_cell)      

            elif robot_current_cell[1] != 0 and \
            path_matrix[robot_current_cell[1] - 1][robot_current_cell[0]] == 0 and \
            (robot_current_cell, 'vertical') in wall_stack:
                print("turn up")
                print(path_matrix[robot_current_cell[1] - 1][robot_current_cell[0]])
                robot_current_cell = (robot_current_cell[0], robot_current_cell[1] - 1) # to up
                path_matrix[robot_current_cell[1]][robot_current_cell[0]] = 1
                robot_path_stack.append(robot_current_cell)  

            elif robot_current_cell[1] != maze_height - 1 and \
            path_matrix[robot_current_cell[1] + 1][robot_current_cell[0]] == 0 and \
            ((robot_current_cell[0], robot_current_cell[1] + 1), 'vertical') in wall_stack:
                print("turn down")
                print(path_matrix[robot_current_cell[1] + 1][robot_current_cell[0]])
                robot_current_cell = (robot_current_cell[0], robot_current_cell[1] + 1) # to down
                path_matrix[robot_current_cell[1]][robot_current_cell[0]] = 1
                robot_path_stack.append(robot_current_cell)     
                
            else:
                robot_current_cell = robot_path_stack.pop()
                continue

        #     if robot_current_cell[0] != 0 and \
        #     path_matrix[robot_current_cell[0] - 1][robot_current_cell[1]] == 0 and \
        #     ((robot_current_cell, (robot_current_cell[0] - 1, robot_current_cell[1])) in wall_stack or \
        #     ((robot_current_cell[0] - 1, robot_current_cell[1]), robot_current_cell) in wall_stack):
        #         robot_current_cell = (robot_current_cell[0] - 1, robot_current_cell[1]) # to left
        #         path_matrix[robot_current_cell[0]][robot_current_cell[1]] = 1
        #         robot_path_stack.append(robot_current_cell)

        #     elif robot_current_cell[0] != maze_width - 1 and \
        #     path_matrix[robot_current_cell[0] + 1][robot_current_cell[1]] == 0 and \
        #     ((robot_current_cell, (robot_current_cell[0] + 1, robot_current_cell[1])) in wall_stack or \
        #     ((robot_current_cell[0] + 1, robot_current_cell[1]), robot_current_cell) in wall_stack):
        #         robot_current_cell = (robot_current_cell[0] + 1, robot_current_cell[1])
        #         path_matrix[robot_current_cell[0]][robot_current_cell[1]] = 1
        #         robot_path_stack.append(robot_current_cell)

        #     elif robot_current_cell[1] != 0 and \
        #     path_matrix[robot_current_cell[0]][robot_current_cell[1] - 1] == 0 and \
        #     ((robot_current_cell, (robot_current_cell[0], robot_current_cell[1] - 1)) in wall_stack or \
        #     ((robot_current_cell, robot_current_cell[1] - 1), robot_current_cell) in wall_stack):
        #         robot_current_cell = (robot_current_cell[0], robot_current_cell[1] - 1) # to up
        #         path_matrix[robot_current_cell[0]][robot_current_cell[1]] = 1
        #         robot_path_stack.append(robot_current_cell)
            
        #     elif robot_current_cell[1] != maze_width - 1 and \
        #     path_matrix[robot_current_cell[0]][robot_current_cell[1] + 1] == 0 and \
        #     ((robot_current_cell, (robot_current_cell[0], robot_current_cell[1] + 1)) in wall_stack or \
        #     ((robot_current_cell, robot_current_cell[1] + 1), robot_current_cell) in wall_stack):
        #         robot_current_cell = (robot_current_cell[0], robot_current_cell[1] + 1) # to down
        #         path_matrix[robot_current_cell[0]][robot_current_cell[1]] = 1
        #         robot_path_stack.append(robot_current_cell)
            
        #     else:
        #         robot_current_cell = robot_path_stack.pop()
        #         continue




    pygame.display.update()

pygame.quit()
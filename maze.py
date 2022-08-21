import pygame
import random

# pygame.init()

win_width = 500
win_height = 500

# win = pygame.display.set_mode((win_width, win_height))

x_red = 50 ## location
y_red = 50

x_blue = 100
y_blue = 100

robot_width = 50
robot_height = 50

obs_width = 50
obs_height = 50

vel = 5

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

maze_matrix = [[0 for x in range(int(win_width/robot_width))] for y in range(int(win_height/robot_height))] 
maze_matrix[0][0] = 1
starting_pos = (0, 0)

ending_x = int(win_width/robot_width) - 1
ending_y = int(win_height/robot_height) - 1
ending_pos = (ending_x, ending_y)

curr_pos = starting_pos
pos_stack = []
pos_stack.append(starting_pos)
not_terminal = True

def custom_random(exclude_dir):
    rand = random.randint(0, 4)
    return custom_random(exclude_dir) if rand in exclude_dir else rand

while not_terminal:
    if curr_pos == ending_pos:
        not_terminal = False
        maze_matrix[ending_x][ending_y] = 1
        break
    exclude_dir = []
    if curr_pos[0] == 0 or (curr_pos[0] > 0 and maze_matrix[curr_pos[0] - 1][curr_pos[1]] == 1): ## left boundary or left is a path
        exclude_dir.append(LEFT)
    elif curr_pos[0] == 9 or (curr_pos[0] < 9 and maze_matrix[curr_pos[0] + 1][curr_pos[1]] == 1):
        exclude_dir.append(RIGHT)

    if curr_pos[1] == 0 or (curr_pos[1] > 0 and maze_matrix[curr_pos[0]][curr_pos[1] - 1] == 1):
        exclude_dir.append(UP)
    elif curr_pos[1] == 9 or (curr_pos[1] < 9 and maze_matrix[curr_pos[0]][curr_pos[1] + 1] == 1):
        exclude_dir.append(DOWN)

    print(exclude_dir)
    if len(exclude_dir) == 4:
        curr_pos = pos_stack.pop()
        continue

    dir = custom_random(exclude_dir)
    print(dir)
    if dir == LEFT:
        curr_pos = (curr_pos[0] - 1, curr_pos[1])
    elif dir == RIGHT:
        curr_pos = (curr_pos[0] + 1, curr_pos[1])
    elif dir == UP:
        curr_pos = (curr_pos[0], curr_pos[1] - 1)
    else:
        curr_pos = (curr_pos[0], curr_pos[1] + 1)

    print(curr_pos)
    maze_matrix[curr_pos[0]][curr_pos[1]] = 1
    print(maze_matrix)
    pos_stack.append(curr_pos)

print(maze_matrix)
# run = True
# blue_move = pygame.USEREVENT
# pygame.time.set_timer(blue_move, 1000)
# while run:
#     pygame.time.delay(100)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#         if event.type == blue_move:
#             if x_blue <= win_width - robot_width:
#                 x_blue += vel
#             elif y_blue <= win_height - robot_height:
#                 x_blue += vel
    
#     keys = pygame.key.get_pressed()

#     if keys[pygame.K_LEFT]:
#         x_red -= vel
#     if keys[pygame.K_RIGHT]:
#         x_red += vel
#     if keys[pygame.K_UP]:
#         y_red -= vel
#     if keys[pygame.K_DOWN]:
#         y_red += vel

#     win.fill((0))

#     for i in range(0, int(win_height/robot_height)):
#         for j in range(0, int(win_width/robot_width)):
#             if i%2 == 0:
#                 if j%2 == 0:
#                     pygame.draw.rect(win, (255, 255, 255), (j*robot_width, i*robot_height, robot_width, robot_height))
#             else:
#                 if j%2 != 0:
#                     pygame.draw.rect(win, (255, 255, 255), (j*robot_width, i*robot_height, robot_width, robot_height))               
               
#     pygame.display.update()

# pygame.quit()
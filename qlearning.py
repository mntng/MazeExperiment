import pygame
import random

pygame.init()

win = pygame.display.set_mode((500, 500))

pygame.display.set_caption("HaHa")

x_red = 50
y_red = 50
x_blue = 100
y_blue = 100
robot_width = 50
robot_height = 50
obs_width = 50
obs_height = 50

vel = 5

location = []
obs_1 = []
obs_2 = []
obs_2_1 = []

for i in range(0, 500):
    obs_1.append(1)

for i in range(0, 5):
    for j in range(0, 100):
        if j < 50:
            obs_2.append(1)
        else:
            obs_2.append(0)

# for i in range(0, 99):
#     if i < 50:
#         obs_2_1.append(1)
#     else:
#         obs_2_1.append(0)

# for i in range(0, 5):
#     obs_2.append(obs_2_1)

for i in range(0, 10):
    for j in range(0, 50):
        if i%2 == 0:
            location.append(obs_1)
        else:
            location.append(obs_2)

print(location)

        
# for i in range(0, 40):
#     r1 = random.randint(40, 460)
#     r2 = random.randint(40, 460)
#     location.append((r1, r2))


run = True
blue_move = pygame.USEREVENT
pygame.time.set_timer(blue_move, 1000)

while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == blue_move: 
            if x_blue <= 500:
                x_blue += vel
            elif y_blue <= 500:
                y_blue += vel

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x_red -= vel
    if keys[pygame.K_RIGHT]:
        x_red += vel
    if keys[pygame.K_UP]:
        y_red -= vel
    if keys[pygame.K_DOWN]:
        y_red += vel
    
    win.fill((0))
    pygame.draw.rect(win, (255, 0, 0), (x_red, y_red, robot_width, robot_height))
    pygame.draw.rect(win, (0, 0, 255), (x_blue, y_blue, robot_width, robot_height))
    pygame.draw.rect(win, (255, 255, 255), (0, 0, obs_width, obs_height))
    pygame.draw.rect(win, (255, 255, 255), (449, 449, obs_width, obs_height))
    # for i in range(0, 10):
    #     for j in range(0, 10):
    #         if location[i * 50][j * 50] == 1:
    #             pygame.draw.rect(win, (255, 255, 255), (i * 50, j * 50, obs_width, obs_height))

    # for i in range(0, 500):
    #     for j in range(0, 500):
    #         if location[i][j] == 1:
    #             pygame.draw.rect(win, (255, 255, 255), (i, j, 1, 1))
        # pygame.draw.rect(win, (255, 255, 255), (l[0], l[1], 1, 1))

    pygame.display.update()

pygame.quit()
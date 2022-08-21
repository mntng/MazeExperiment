import numpy as np

maze_matrix = [[0 for x in range(5)] for y in range(5)]

maze_matrix[1][0] = 1

print(np.array(maze_matrix))
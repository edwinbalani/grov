"""
Demonstrates using custom hillshading in a 3D surface plot.
"""
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import time
from math import sqrt
import copy
import math

def gradient_calculation(z, point1, point2):
    return (z[point2[0]][point2[1]] - z[point1[0]][point1[1]]) / (math.sqrt((point1[0]-point2[0]) ** 2 + (point1[1]-point2[1]) ** 2))

def gradient_difficulty(gradient):
    return 1 + 1 / (1 + math.exp(-gradient))


def command_interpreter(standing_point, command):
    command_words = command.split()
    if (command_words[0].lower() == "east"):
        standing_point[0] += int(command_words[1])
    if (command_words[0].lower() == "west"):
        standing_point[0] -= int(command_words[1])
    if (command_words[0].lower() == "north"):
        standing_point[1] += int(command_words[1])
    if (command_words[0].lower() == "south"):
        standing_point[1] -= int(command_words[1])
    print(standing_point)
    return standing_point


def priority_enqueue(q, key, distance, heur, parent):
    l = len(q) - 1
    if l >= 0:
        while (q[l][1] + q[l][2] > distance + heur and l >= 0):
            l -= 1
        q.insert(l + 1, (key, distance, heur, parent))
    else:
        q.append((key, distance, heur, parent))


def heuristic(standing_point, goal):
    return sqrt((goal[0] - standing_point[0]) ** 2 + (goal[1] - standing_point[1]) ** 2)


def a_star_search(origin, goal, heuristic, coordinates, anomaly, marked, z):
    original_marked = copy.copy(marked)
    pq = list()
    trace = dict()
    pq.append((origin, 0, heuristic(origin, goal), origin))
    while len(pq) > 0:
        boundary = pq.pop(0)
        if boundary[0] == goal:
            return trace, boundary[1], boundary[3]
        if boundary[0] in anomaly:
            trajectory = ax.plot([x[boundary[0][0]][boundary[0][1]]], [y[boundary[0][0]][boundary[0][1]]],
                     [z[boundary[0][0]][boundary[0][1]]], markerfacecolor='k',
                     markeredgecolor='k', marker='o', markersize=5, alpha=0.6)
            print("There is an obastacle at", (boundary[0]))
            print("Start over, avoiding", boundary[0])
            marked = original_marked
            marked[boundary[0]] = True
            return a_star_search(origin, goal, heuristic, coordinates, anomaly, marked, z)
        if (boundary[0][0] + 1 in coordinates[0]) and (boundary[0][1] + 1 in coordinates[1]) and (
                    marked[(boundary[0][0] + 1, boundary[0][1] + 1)] == False):
            grad = gradient_calculation(z, boundary[0], (boundary[0][0] + 1, boundary[0][1] + 1))
            marked[(boundary[0][0] + 1, boundary[0][1] + 1)] = True
            priority_enqueue(pq, (boundary[0][0] + 1, boundary[0][1] + 1), boundary[1] + 1.414 * gradient_difficulty(grad),
                             heuristic((boundary[0][0] + 1, boundary[0][1] + 1), goal), boundary[0])
            trace[(boundary[0][0] + 1, boundary[0][1] + 1)] = boundary[0]
        if (boundary[0][0] + 1 in coordinates[0]) and (boundary[0][1] - 1 in coordinates[1]) and (
                    marked[(boundary[0][0] + 1, boundary[0][1] - 1)] == False):
            grad = gradient_calculation(z, boundary[0], (boundary[0][0] + 1, boundary[0][1] - 1))
            marked[(boundary[0][0] + 1, boundary[0][1] - 1)] = True
            priority_enqueue(pq, (boundary[0][0] + 1, boundary[0][1] - 1), boundary[1] + 1.414 * gradient_difficulty(grad),
                             heuristic((boundary[0][0] + 1, boundary[0][1] - 1), goal), boundary[0])
            trace[(boundary[0][0] + 1, boundary[0][1] - 1)] = boundary[0]
        if (boundary[0][0] - 1 in coordinates[0]) and (boundary[0][1] + 1 in coordinates[1]) and (
                    marked[(boundary[0][0] - 1, boundary[0][1] + 1)] == False):
            grad = gradient_calculation(z, boundary[0], (boundary[0][0] - 1, boundary[0][1] + 1))
            marked[(boundary[0][0] - 1, boundary[0][1] + 1)] = True
            priority_enqueue(pq, (boundary[0][0] - 1, boundary[0][1] + 1), boundary[1] + 1.414 * gradient_difficulty(grad),
                             heuristic((boundary[0][0] - 1, boundary[0][1] + 1), goal), boundary[0])
            trace[(boundary[0][0] - 1, boundary[0][1] + 1)] = boundary[0]
        if (boundary[0][0] - 1 in coordinates[0]) and (boundary[0][1] - 1 in coordinates[1]) and (
                    marked[(boundary[0][0] - 1, boundary[0][1] - 1)] == False):
            grad = gradient_calculation(z, boundary[0], (boundary[0][0] - 1, boundary[0][1] - 1))
            marked[(boundary[0][0] - 1, boundary[0][1] - 1)] = True
            priority_enqueue(pq, (boundary[0][0] - 1, boundary[0][1] - 1), boundary[1] + 1.414 * gradient_difficulty(grad),
                             heuristic((boundary[0][0] - 1, boundary[0][1] - 1), goal), boundary[0])
            trace[(boundary[0][0] - 1, boundary[0][1] - 1)] = boundary[0]
        if (boundary[0][0] in coordinates[0]) and (boundary[0][1] - 1 in coordinates[1]) and (
                    marked[(boundary[0][0], boundary[0][1] - 1)] == False):
            grad = gradient_calculation(z, boundary[0], (boundary[0][0], boundary[0][1] - 1))
            marked[(boundary[0][0], boundary[0][1] - 1)] = True
            priority_enqueue(pq, (boundary[0][0], boundary[0][1] - 1), boundary[1] + 1 * gradient_difficulty(grad),
                             heuristic((boundary[0][0], boundary[0][1] - 1), goal), boundary[0])
            trace[(boundary[0][0], boundary[0][1] - 1)] = boundary[0]
        if (boundary[0][0] in coordinates[0]) and (boundary[0][1] + 1 in coordinates[1]) and (
                    marked[(boundary[0][0], boundary[0][1] + 1)] == False):
            grad = gradient_calculation(z, boundary[0], (boundary[0][0], boundary[0][1] + 1))
            marked[(boundary[0][0], boundary[0][1] + 1)] = True
            priority_enqueue(pq, (boundary[0][0], boundary[0][1] + 1), boundary[1] + 1 * gradient_difficulty(grad),
                             heuristic((boundary[0][0], boundary[0][1] + 1), goal), boundary[0])
            trace[(boundary[0][0], boundary[0][1] + 1)] = boundary[0]
        if (boundary[0][0] - 1 in coordinates[0]) and (boundary[0][1] in coordinates[1]) and (
                    marked[(boundary[0][0] - 1, boundary[0][1])] == False):
            grad = gradient_calculation(z, boundary[0], (boundary[0][0] - 1, boundary[0][1]))
            marked[(boundary[0][0] - 1, boundary[0][1])] = True
            priority_enqueue(pq, (boundary[0][0] - 1, boundary[0][1]), boundary[1] + 1 * gradient_difficulty(grad),
                             heuristic((boundary[0][0] - 1, boundary[0][1]), goal), boundary[0])
            trace[(boundary[0][0] - 1, boundary[0][1])] = boundary[0]
        if (boundary[0][0] + 1 in coordinates[0]) and (boundary[0][1] in coordinates[1]) and (
                    marked[(boundary[0][0] + 1, boundary[0][1])] == False):
            grad = gradient_calculation(z, boundary[0], (boundary[0][0] + 1, boundary[0][1]))
            marked[(boundary[0][0] + 1, boundary[0][1])] = True
            priority_enqueue(pq, (boundary[0][0] + 1, boundary[0][1]), boundary[1] + 1 * gradient_difficulty(grad),
                             heuristic((boundary[0][0] + 1, boundary[0][1]), goal), boundary[0])
            trace[(boundary[0][0] + 1, boundary[0][1])] = boundary[0]
    print("There is no way we can reach the goal.")

filename = cbook.get_sample_data('jacksboro_fault_dem.npz', asfileobj=False)
with np.load(filename) as dem:
    z = dem['elevation']
    nrows, ncols = z.shape
    x = np.linspace(dem['xmin'], dem['xmax'], ncols)
    y = np.linspace(dem['ymin'], dem['ymax'], nrows)
    x, y = np.meshgrid(x, y)

coordinates = (range(0, 45), range(0, 45))
region = np.s_[5:50, 5:50]
x, y, z = x[region], y[region], z[region]

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
ax.set_xlabel("South-North")
ax.set_ylabel("West-East")

ls = LightSource(270, 45)
# To use a custom hillshading mode, override the built-in shading and pass
# in the rgb colors of the shaded surface calculated from "shade".
rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=False)

origin = (5, 5)
goal = (40, 40)
obstacles = [(7, 9), (8, 9), (9, 9), (10, 9), (11, 9), (12, 9),
            (20, 16), (20, 17), (20, 18), (20, 19), (20, 20)]
for i in range(15, 25):
    for j in range(15, 25):
        obstacles.append((i, j))
for i in range(30, 40):
    for j in range(30, 40):
        obstacles.append((i, j))

trajectory = ax.plot([x[origin[0]][origin[1]]], [y[origin[0]][origin[1]]],
                     [z[origin[0]][origin[1]]], markerfacecolor='m',
                     markeredgecolor='w', marker='o', markersize=5, alpha=0.6)
trajectory = ax.plot([x[goal[0]][goal[1]]], [y[goal[0]][goal[1]]],
                     [z[goal[0]][goal[1]]], markerfacecolor='g',
                     markeredgecolor='w', marker='o', markersize=5, alpha=0.6)
plt.show(block=False)
plt.pause(5)

marked = dict()
for i in coordinates[0]:
    for j in coordinates[1]:
        marked[(i, j)] = False

trace, dist, parent = a_star_search(origin, goal, heuristic, coordinates, obstacles, marked, z)
while parent != origin:
    print(parent[0], parent[1])
    trajectory = ax.plot([x[parent[0]][parent[1]]], [y[parent[0]][parent[1]]],
                         [z[parent[0]][parent[1]]], markerfacecolor='r',
                         markeredgecolor='r', marker='o', markersize=5, alpha=0.6)
    parent = trace[parent]
plt.draw()

print("You have reached the goal!")
print("The final distance walked is", dist)
plt.show()

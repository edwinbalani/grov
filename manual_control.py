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


def command_interpreter(standing_point, command):
    command_words = command.split()
    if command_words[0].lower() == "east":
        standing_point[0] += int(command_words[1])
    if command_words[0].lower() == "west":
        standing_point[0] -= int(command_words[1])
    if command_words[0].lower() == "north":
        standing_point[1] += int(command_words[1])
    if command_words[0].lower() == "south":
        standing_point[1] -= int(command_words[1])
    print(standing_point)
    return standing_point


filename = cbook.get_sample_data('jacksboro_fault_dem.npz', asfileobj=False)
with np.load(filename) as dem:
    z = dem['elevation']
    nrows, ncols = z.shape
    x = np.linspace(dem['xmin'], dem['xmax'], ncols)
    y = np.linspace(dem['ymin'], dem['ymax'], nrows)
    x, y = np.meshgrid(x, y)

region = np.s_[5:50, 5:50]
x, y, z = x[region], y[region], z[region]
barriers = [[25, 25], []]

fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
ax.set_xlabel("South-North")
ax.set_ylabel("West-East")

ls = LightSource(270, 45)
# To use a custom hillshading mode, override the built-in shading and pass
# in the rgb colors of the shaded surface calculated from "shade".
rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=False)

origin = [20, 20]
standing_point = origin
goal = [26, 28]
trajectory = ax.plot([x[origin[0]][origin[1]]], [y[origin[0]][origin[1]]],
                     [z[origin[0]][origin[1]]], markerfacecolor='m',
                     markeredgecolor='m', marker='o', markersize=5, alpha=0.6)
trajectory = ax.plot([x[goal[0]][goal[1]]], [y[goal[0]][goal[1]]], [z[goal[0]][goal[1]]], markerfacecolor='g',
                     markeredgecolor='g', marker='o', markersize=5, alpha=0.6)
plt.show(block=False)
plt.pause(5)

while origin != goal:
    command = input("**Please type your command with direction and distance, e.g. east 2**\n")
    standing_point = command_interpreter(standing_point, command)
    trajectory = ax.plot([x[standing_point[0]][standing_point[1]]], [y[standing_point[0]][standing_point[1]]],
                         [z[standing_point[0]][standing_point[1]]], markerfacecolor='r', markeredgecolor='r',
                         marker='o', markersize=5, alpha=0.6)
    plt.draw()

    plt.show(block=False)
    plt.pause(2)

print("You have reached the goal!")
plt.show()



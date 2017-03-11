# Copyright 2017 Edwin Bahrami Balani and Qiaochu Jiang
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This module contains functions for grid data analysis."""

import numpy as np


def window(grid, indices, window_size=5):
    """
    Return a square window from a 2-D grid.
    Note: edge values are padded using `numpy.pad(mode='edge')`
    :param grid: 2-D grid of values
    :param indices: (x, y) tuple of indices
    :param window_size: length of the window, must be odd
    :return:
    """
    if window_size % 2 != 1:
        raise ValueError('window_size must be odd')
    if len(indices) != 2:
        raise ValueError('indices (x, y) must be specified')
    x, y = indices

    # Preemptive padding on all edges prevents having to check if our window falls beyond the end
    # However, we must then adjust our indices due to the grid expansion
    grid = np.pad(grid, window_size, 'edge')
    x += window_size
    y += window_size

    xmin = x - window_size//2
    ymin = y - window_size//2
    xmax = x + window_size//2 + 1
    ymax = y + window_size//2 + 1
    grid = grid[xmin:xmax, ymin:ymax]
    return grid


def gradient(grid, indices, window_size=5, dx=1, dy=1):
    """
    Finds the gradient at a point in a 2-D grid using a polynomial fit
    :param grid: 2-D grid of z-values
    :param indices: (x, y) tuple of indices where gradient will be found
    :param window_size: size of the square window used for the polynomial fit (default 5)
    :param dx: spacing between adjacent x-points (default 1)
    :param dy: spacing betwween adjacent y-points (default 1)
    :return: a 3-D gradient vector
    """
    X, Y, coeff = fit(grid, indices, window_size)

    # Coefficients in order 1, x, y, x^2, x^2.y, x^2.y^2, y^2, x.y^2, x.y
    #                       a, b, c,  d,    e,      f,     g,    h,    i

    # I am not proud of this:
    # TODO rewrite this section for smarter/iterative processing
    # (This also has the benefit of allowing for a general nth-order polynomial fit:
    # see https://gistpreview.github.io/?f9990a6c0eec76c0c8176b050121e694)

    x, y = X[window_size//2, window_size//2], Y[window_size//2, window_size//2]
    return np.array([__wrt_x(x, y, coeff) / dx, __wrt_y(x, y, coeff) / dy])


def fit(grid, indices, window_size=5):
    """
    Calculates a second-order 2-D fit function at a point on a grid
    :param grid: 2-D grid of z-values
    :param indices: (x, y) tuple of indices where gradient will be found
    :param window_size: size of the square window used for the polynomial fit (default 5)
    :return:
    """
    grid = window(grid, indices, window_size=window_size)
    X, Y = np.mgrid[0:window_size, 0:window_size]
    Xf = X.flatten()
    Yf = Y.flatten()
    A = np.array([np.ones(X.size), Xf, Yf, Xf ** 2, Xf ** 2 * Yf, Xf ** 2 * Yf ** 2, Yf ** 2, Xf * Yf ** 2, Xf * Yf]).T
    B = grid.flatten()
    return X, Y, np.linalg.lstsq(A, B)


def __z(x, y, c):
    a = c[0]
    b = c[1]
    c = c[2]
    d = c[3]
    e = c[4]
    f = c[5]
    g = c[6]
    h = c[7]
    i = c[8]
    return a + b*x + c*y + d*x**2 + e*x**2*y + f*x**2*y**2 + g*y**2 + h*x*y**2 + i*x*y


def __wrt_x(x, y, c):
    b = c[1]
    c = c[2]
    d = c[3]
    e = c[4]
    f = c[5]
    h = c[7]
    i = c[8]
    return b + 2*d*x + 2*e*x*y + 2*f*x*y**2 + h*y**2 + i*y


def __wrt_y(x, y, c):
    c = c[2]
    e = c[4]
    f = c[5]
    g = c[6]
    h = c[7]
    i = c[8]
    return c + e*x**2 + 2*f*x**2*y + 2*g*y + 2*h*x*y + i*x


def direc_deriv(grad: np.ndarray, direc: np.ndarray, norm=True):
    """
    Calculates the directional derivative of a function
    :param grad: Gradient vector (2-D)
    :param dir: Direction
    :param: norm: Whether to normalise the direction vector (default True)
    :return:
    """
    if not grad.size == 2:
            raise ValueError("Gradient vector must have 2 components")
    return grad * (np.linalg.norm(direc) if norm else direc)


def slope(grad: np.ndarray):
    """
    Calculates the slope of a function in the direction of its gradient
    :param grad: Gradient vector (2-D)
    :return:
    """
    return direc_deriv(grad, grad, norm=True)

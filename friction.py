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

"""Functions related to probe traction"""

import numpy as np
import analysis

def fix_angle_range(a: float):
    """Fix radian angles to range [0, pi]"""
    while a < 0:
        a += 2*np.pi
    while a > 2*np.pi:
        a -= 2*np.pi
    if a > np.pi:
        a = 2*np.pi - a
    return a


def safe_slope(grad: np.ndarray, mu: float):
    """
    Return a True/False value determining whether the current slope is safe, given a coefficient of friction.
    :param grad: Gradient vector representing steepest slope at a point
    :param mu: Coefficient of friction
    :return:
    """
    if not grad.size == 2:
        raise ValueError("Gradient vector must have two components")
    grad = np.linalg.norm(grad)
    phi = np.arctan2(mu, 1)  # Angle of limiting friction
    slope_angle = fix_angle_range(np.arctan2(grad[1], grad[0]))
    return slope_angle <= phi


def safe_point(grid, indices, mu, window_size=5):
    """
    Determine whether a point is safe for the probe to climb.
    :param grid: 2-D grid of Z values
    :param indices: indices of point
    :param mu: coefficient of friction at point
    :param window_size: window size for gradient fit calculation (default 5)
    :return:
    """
    return safe_slope(analysis.gradient(grid, indices, window_size=window_size), mu)

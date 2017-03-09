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

"""Utility functions for testing purposes"""

import numpy as np

def rgrid(size=10, integers=True, low=None, high=None):
    """Return a grid of random values"""
    if low is None:
        low = 1 if integers else 0
    if high is None:
        high = 21 if integers else 1

    if integers:
        return np.random.randint(low, high, (size, size))
    else:
        return np.random.randn(low, high, (size, size))

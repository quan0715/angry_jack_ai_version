from __future__ import annotations

from typing import Optional

import numpy as np

try:
    from .FFN import FFN
    from .activation_func import get_activation_function
except:
    from FFN import FFN
    from activation_func import get_activation_function

__all__ = ['Dense']


class Dense:
    def __init__(self, output_size: int, input_size: Optional[int] = None, act='relu'):
        self._output_size: int = output_size
        self._input_size: Optional[int] = input_size
        self._activation = get_activation_function(act)
        self._W: Optional[np.ndarray] = None
        self._B: Optional[np.ndarray] = None
        self._parent: Optional[FFN] = None
        self._last_output: Optional[np.ndarray] = None
        if input_size is not None:
            self._W = (np.random.random((output_size, input_size)) - 0.5) * 2
            self._B = (np.random.random((output_size, 1)) - 0.5) * 2

    def set_parent(self, parent: FFN):
        self._parent = parent
        if self._W is None:
            self._input_size = parent.info['outputDim']
            self._W = (np.random.random((self._output_size, self._input_size)) - 0.5) * 2
            self._B = (np.random.random((self._output_size, 1)) - 0.5) * 2

    def forward(self, input: np.ndarray):
        if self._W is None:
            raise Exception('W not set, please specify input size or indicate parent')
        self._last_output = self._activation(self._W @ input - self._B)
        return self._last_output

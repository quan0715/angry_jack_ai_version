__all__ = ['get_activation_function']

import numpy as np

activation_dict = {
    'relu': lambda x: np.where(x > 0, x, 0),
    'sigmoid': lambda x: 1 / (1 + np.exp(-x)),
    'elu': lambda x: np.where(x > 0, x, np.exp(x) - 1),
}


def get_activation_function(name: str):
    return activation_dict[name]

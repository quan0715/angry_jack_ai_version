from typing import List
from enum import Enum
import numpy as np

try:
    from .FFN import *
    from .FFN import FFN
    from .Dense import *
except:
    from FFN import *
    from Dense import *


__all__ = ['FFN', 'Dense', 'create_model', 'get_direction', 'init_from_chromosome']


def create_model(input_size: int,
                 output_size: int,
                 num_hidden_layers: int,
                 hidden_layer_size: int,
                 activation_func: str = 'relu',
                 output_activation_func: str = 'sigmoid') -> FFN:
    model = FFN()
    model.add(Dense(hidden_layer_size, input_size=input_size, act=activation_func))
    for _ in range(num_hidden_layers - 1):
        model.add(Dense(hidden_layer_size, act=activation_func))
    model.add(Dense(output_size, act=output_activation_func))
    return model


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


def get_direction(model: FFN, feature: np.ndarray) -> Direction:
    res = np.argmax(model.forward(feature))
    if res == 0:
        return Direction.UP
    elif res == 1:
        return Direction.DOWN
    elif res == 2:
        return Direction.LEFT
    elif res == 3:
        return Direction.RIGHT
    else:
        raise Exception('error on getdirection, res=', res)


def init_from_chromosome(model: FFN, chromosome: List[np.ndarray[np.ndarray]]):
    for i, layer in enumerate(chromosome):
        w, bias = layer[:, 1:], layer[:, 0:1]
        model.set_weight_and_bias(i, modifiedW=w, modifiedB=bias)


if __name__ == "__main__":
    model: FFN = create_model(24, 4, 2, 40)

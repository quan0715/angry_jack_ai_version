from typing import List

from setting import GAConfig
from .FFN import FFN
from .Dense import Dense

import numpy as np

__all__ = ['FFN', 'Dense', 'create_model', 'create_default_model', 'get_direction', 'init_from_chromosome']


def create_model(input_size: int,
                 output_size: int,
                 hidden_layers: List[int],
                 activation_func: str = 'relu',
                 output_activation_func: str = 'sigmoid') -> FFN:
    model = FFN()
    model.add(Dense(output_size=hidden_layers[0], input_size=input_size, act=activation_func))
    for idx in range(1, len(hidden_layers)):
        model.add(Dense(output_size=hidden_layers[idx], input_size=hidden_layers[idx - 1], act=activation_func))
    model.add(Dense(output_size, act=output_activation_func))
    return model


def create_default_model():
    return create_model(input_size=32, output_size=4, hidden_layers=GAConfig.hidden_layer_size
        , output_activation_func='relu')


def get_direction(model: FFN, feature: np.ndarray):
    res = np.argmax(model.forward(feature))
    assert 0 <= res <= 3
    return res


def init_from_chromosome(model: FFN, chromosome: List[np.ndarray]):
    for i, layer in enumerate(chromosome):
        w, bias = layer[:, 1:], layer[:, 0:1]
        model.set_weight_and_bias(i, modifiedW=w, modifiedB=bias)

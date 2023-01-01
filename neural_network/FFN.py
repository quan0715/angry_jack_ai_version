import numpy as np

from typing import Dict, List, Tuple, Optional
from neural_network import Dense

__all__ = ['FFN']


class FFN:
    def __init__(self) -> None:
        self._layers: List[Dense] = []

    def add(self, layer: Dense):
        layer.set_parent(self)
        self._layers.append(layer)

    @property
    def info(self) -> Dict[str, int]:
        """
        inputDim: input dimension

        outputDim: output dimension

        layers Info: the amount of units for each layer by corresponded index
        """
        info: Dict[str, int] = {'inputDim': self._layers[0]._input_size,
                                'outputDim': self._layers[-1]._output_size,
                                'layersInfo': [layer._output_size for layer in self._layers]}
        return info

    @property
    def last_outputs(self) -> List[np.ndarray]:
        return [layer._last_output.flatten() for layer in self._layers]

    def forward(self, x: np.ndarray):
        if needFlatten := (x.ndim != 2):
            x = np.array([x.flatten()])
        next_input = x.transpose()
        for layer in self._layers:
            next_input = layer.forward(next_input)
        if not needFlatten:
            return next_input
        else:
            return next_input.flatten()

    def get_weight_and_bias(self, layer_idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        returned array on axis 0 is the weight of a neural

        example:

        w, b = getWeightAndBias(1)

        w[0] and b[0] is the weights and bias of the first neural
        """
        return self._layers[layer_idx]._W.copy(), self._layers[layer_idx]._B.copy()

    def set_weight_and_bias(self,
                            layer_idx: int,
                            modifiedW: Optional[np.ndarray] = None,
                            modifiedB: Optional[np.ndarray] = None):
        if modifiedW is not None:
            if self._layers[layer_idx]._W.shape == modifiedW.shape:
                self._layers[layer_idx]._W = modifiedW.copy()
            else:
                print(
                    f'Wrong size for set weight, target w shape is {self._layers[layer_idx]._W.shape}, while yours is {modifiedW.shape}')
        if modifiedB is not None:
            if self._layers[layer_idx]._B.shape == modifiedB.shape:
                self._layers[layer_idx]._B = modifiedB.copy()
            else:
                print(
                    f'Wrong size for set weight, target w shape is {self._layers[layer_idx]._B.shape}, while yours is {modifiedB.shape}')


if __name__ == "__main__":
    print(FFN())

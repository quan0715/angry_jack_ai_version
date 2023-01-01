from neural_network import *

if __name__ == "__main__":
    # create a model, detail in DNN/__init__.py
    model: FFN = create_model(32, 4, [20, 12], activation_func='relu', output_activation_func='elu')
    import numpy as np

    # model input and output
    print('model input and output')
    input1D = np.random.random(model.info['inputDim'])
    input2D = np.random.random((3, model.info['inputDim']))
    result1D = model.forward(input1D)
    result2D = model.forward(input2D)
    print(f'input1D shape: {input1D.shape}, output shape: {result1D.shape}')
    print(f'input2D shape: {input2D.shape}, output shape: {result2D.shape}')

    print("\nget_direction for game")
    print(f'direction: {get_direction(model, input1D)}')
    # modify wight and bias
    print('\nmodify wight and bias')
    w, b = model.get_weight_and_bias(1)
    randomModifiedWeight = np.random.random(w.shape)
    randomModifiedBias = np.random.random(b.shape)
    print(f'output before w and b modified: {result1D}')
    result1D = model.forward(input1D)
    print(f'output after w and b modified: {result1D}')

    # test init_from_chromesome
    rdarr = []
    for i in range(3):
        w = model.get_weight_and_bias(i)[0]
        rdarr.append(np.random.random((w.shape[0], w.shape[1] + 1)))
    model.set_weight_and_bias(1, modifiedW=randomModifiedWeight, modifiedB=randomModifiedBias)
    init_from_chromosome(model, rdarr)

    # output history
    print('\nlast outputs')
    lastOutputs = model.last_outputs
    print(f'last outputs length: {len(lastOutputs)}')
    for i, j in enumerate(lastOutputs):
        print(f'last output in layer {i}')
        print(j)

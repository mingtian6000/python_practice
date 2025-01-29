#simple demo for neutral network
import numpy as np

def step_function(x):
    return 1 if x>0 else 0

def perceptron(input, weight, bias):
    weighted_sum = np.dot(input, weight) + bias
    output = step_function(weighted_sum)
    return output

inputs = np.array([1,0, 1])
weights = np.array([0.5, 0.3, 0.2])
bias = -0.2

outputs = perceptron(inputs, weights, bias)
print(f"inputs: {inputs}")
print(f"outputs: {outputs}")
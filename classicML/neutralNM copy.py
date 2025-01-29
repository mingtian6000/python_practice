import numpy as np

def step_function(x):
    return 1 if x > 0 else 0


def perceptron(inputs, weights, bias):
    weighted_sum = np.dot(inputs, weights) + bias
    output = step_function(weighted_sum)
    return output

# 定义逻辑与运算的输入和对应的正确输出
# 所有可能的二元输入组合
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
# 对应的逻辑与运算的正确输出
correct_outputs = np.array([0, 0, 0, 1])

weights = np.array([0.5, 0.5])
bias = -0.7

for i in range(len(inputs)):
    input_case = inputs[i]
    output = perceptron(input_case, weights, bias)
    correct_output = correct_outputs[i]
    print(f"输入: {input_case}, 正确输出: {correct_output}, 感知机输出: {output}")
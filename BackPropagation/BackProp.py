# Multilayer Neural Network for Exclusive OR (XOR) Function

import numpy as np
import random

class NeuralNetwork(object):

  def __init__(self, input, output):
    self.input_size = 2
    self.output_size = 1
    self.hidden_size = 3
    self.total_size = self.input_size + self.output_size + self.hidden_size

    self.input = input
    self.output = output
    self.shape = input.shape

    # Generate same weights every time
    np.random.seed(1)

    # weights matrix w1 (3X3 matrix) input layer (2 + 1 for bias), hidden layer (3)
    self.w1 = 2 * np.random.random((self.input_size+1, self.hidden_size))
    # weights matrix w2 (3X1 matrix) output layer (1), hidden layer (3)
    self.w2 = 2 * np.random.random((self.hidden_size, self.output_size))

  def sigmoid(self, s):
    # activation function
    return 1/(1+np.exp(-s))
  
  def sigmoidPrime(self, s):
    #derivative of sigmoid
    return s * (1 - s)

  def forward(self, X):
    # forward propagate the calculations
    self.z1 = np.dot(X, self.w1)
    self.z2 = self.sigmoid(self.z1)
    self.z3 = np.dot(self.z2, self.w2)
    self.o = self.sigmoid(self.z3)
    return self.o

  def backward(self, X, y, o):
    # backward propagate through the network
    self.o_error = y - o
    self.o_delta = self.o_error*self.sigmoidPrime(o)
    self.z2_error = self.o_delta.dot(self.w2.T)
    self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2)

    self.w1 += X.T.dot(self.z2_delta)
    self.w2 += self.z2.T.dot(self.o_delta)

  def train (self):
    o = self.forward(self.input)
    self.backward(self.input, self.output, o)
    


if __name__=='__main__':

  # training_data = np.array(([0,0,1], [1,0,1], [0,1,1], [1,1,1], [0.1,1.1,1], [0.99,1.11,1], [0.01,1.21,1], [0.01,0.11,1]), dtype=float)
  # expec_output = np.array(([0], [1], [1], [0], [1], [0], [1], [0]), dtype=int)

  training_data = np.loadtxt('training_input.txt')
  expec_output = np.loadtxt('training_output.txt', ndmin=2)
  training_data = np.hstack((training_data, np.ones((training_data.shape[0], 1), dtype=training_data.dtype)))

  net = NeuralNetwork(training_data, expec_output)
  for i in range(10000):
    net.train()
    if(i % 100) == 0:
      print ("Error: " + str(np.mean(np.abs(net.o_error))))
    
  print(net.o)
  np.savetxt('corrected_weights1.txt', net.w1)
  np.savetxt('corrected_weights2.txt', net.w2)  
  
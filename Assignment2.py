import matplotlib.pyplot as plt
import numpy as np
import math 
import cv2
from re import I
from scipy.io import loadmat
from scipy import signal
import pandas
from pandas import Series
from sklearn.utils import shuffle

img = cv2.imread("Suez Canal.png").astype(np.int64);

# Structuring Element 3x3 or 9x9
B = np.ones((3,3), dtype='int')
a = 5
b = 1

blueChannel= img[:,:,0].astype(np.int64)
greenChannel = img[:,:,1].astype(np.int64) 
redChannel = img[:,:,2].astype(np.int64)

# redChannel,greenChannel,blueChannel = cv2.split(img).astype('int64')

def Dilation(I,B):
    S = I.shape
    F = B.shape
    output = I.copy()
    for i in range(S[0]):
        for j in range(S[1]):
            k = I[i:i+F[0], j:j+F[1]]
            maximum = np.max(k)
            output[i,j] = maximum
    return output

def Erosion(I,B):
    S = I.shape
    F = B.shape
    output = I.copy()
    for i in range(S[0]):
        for j in range(S[1]):
            k = I[i:i+F[0], j:j+F[1]]
            minimum = np.min(k)
            output[i,j] = minimum
    return output

def Opening(I,B):
    i1 = Erosion(I,B)
    i2 = Dilation(i1,B)
    return i2

def Closing(I,B):
    i1 = Dilation(I,B)
    i2 = Erosion(i1,B)
    return i2

def main_Function(I,a,b,B):
    FinalOutput = I + (a * (I - Opening(I,B))) - (b * (Closing(I,B) - I))
    return FinalOutput

RedChannelOutput = main_Function(redChannel,a,b,B)
GreenChannelOutput = main_Function(greenChannel,a,b,B)
BlueChannelOutput = main_Function(blueChannel,a,b,B)

FinalRGB = cv2.merge([BlueChannelOutput,GreenChannelOutput,RedChannelOutput])
FinalRGB =FinalRGB.astype(np.int64)
cv2.imwrite("NewRBGContrast 3x3 a=5 b=1.jpg",FinalRGB)
cv2.waitKey(0)
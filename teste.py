import roboticstoolbox as rtb
import numpy as np
import sympy as sp
from sympy.matrices import Matrix
from sympy import *

# robot = rtb.models.Panda()
# print(robot)

# x = np.array([1,2,3,4])
# print(x)

# b = x + 2
# print(b)

# c = np.sqrt(b)
# print(c)

# y = np.array([45, 60, 90, 180])
# print(y)

# grad = np.sin(y)
# print(grad)

# A = np.array([[1, 2],[3, 4]])
# B = np.array([[5, 0],[-8, 3]])
# print(A + B)

# robot = rtb.models.Puma560()
# print(robot)

#_____________________________________________________________________________________________-

#Matriz de transformación para la traslación en X, Y, Z
def Transl (x, y, z):
    return Matrix([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])

#Matriz de rotación en X para un angulo alfa
def RotX(alfa):
    return Matrix([
        [1, 0, 0, 0],
        [0, cos(alfa), -sin(alfa), 0],
        [0, sin(alfa), cos(alfa), 0],
        [0, 0, 0, 1]
    ])

#Matriz de rotación en Y para un angulo phi
def RotY(phi):
    return Matrix([
        [cos(phi), 0, sin(phi), 0],
        [0, 1, 0, 0],
        [-sin(phi), 0, cos(phi), 0],
        [0, 0, 0, 1]
    ])

#Matriz de rotación en Z para un angulo theta
def RotZ(theta):
    return Matrix([
        [cos(theta), -sin(theta), 0, 0],
        [sin(theta), cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

q, d, a, al = sp.symbols("q d a al")
A = Rotz(q) * Transl(0,0,d) * Transl(a,0,0) * Rotx(al)

import sympy as sp
from sympy.matrices import Matrix
from sympy import *

# #Matriz de transformación para la traslación en X, Y, Z
# def Transl (x, y, z):
#     return Matrix([
#         [1, 0, 0, x],
#         [0, 1, 0, y],
#         [0, 0, 1, z],
#         [0, 0, 0, 1]
#     ])    

# #Matriz de rotación en X para un angulo alfa
# def RotX(alfa):
#     return Matrix([
#         [1, 0, 0, 0],
#         [0, cos(alfa), -sin(alfa), 0],
#         [0, sin(alfa), cos(alfa), 0],
#         [0, 0, 0, 1]
#     ])

# #Matriz de rotación en Y para un angulo phi
# def RotY(phi):
#     return Matrix([
#         [cos(phi), 0, sin(phi), 0],
#         [0, 1, 0, 0],
#         [-sin(phi), 0, cos(phi), 0],
#         [0, 0, 0, 1]
#     ])

# #Matriz de rotación en Z para un angulo theta
# def RotZ(theta):
#     return Matrix([
#         [cos(theta), -sin(theta), 0, 0],
#         [sin(theta), cos(theta), 0, 0],
#         [0, 0, 1, 0],
#         [0, 0, 0, 1]
#     ])

# q, d, a, al = sp.symbols("q d a al")
# A = RotZ(q) * Transl(0,0,d) * Transl(a,0,0) * RotX(al)
# print(A)

def A_01(ang1):
    return Matrix([
        [cos(ang1), 0, -sin(ang1), 0],
        [sin(ang1), 0, cos(ang1), 0],
        [0, -1, 0, 0],
        [0, 0, 0, 1]
    ])

def A_12(ang2,a2, d2):
    return Matrix([
        [cos(ang2), -sin(ang2), 0, a2*cos(ang2)],
        [sin(ang2), cos(ang2), 0, a2*sin(ang2)],
        [0, 0, 1, d2],
        [0, 0, 0, 1]
    ])

def A_23(ang3, a3):
    return Matrix([
        [cos(ang3), 0, sin(ang3), a3*cos(ang3)],
        [sin(ang3), 0, -cos(ang3), a3*sin(ang3)],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])

def A_34(ang4, d4):
    return Matrix([
        [cos(ang4), 0, -sin(ang4), 0],
        [sin(ang4), 0, cos(ang4), 0],
        [0, -1, 0, d4],
        [0, 0, 0, 1]
    ])

def A_45(ang5):
    return Matrix([
        [cos(ang5), 0, sin(ang5), 0],
        [sin(ang5), 0, -cos(ang5), 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])

def A_56(ang6, d6):
    return Matrix([
        [cos(ang6), -sin(ang6), 0, 0],
        [sin(ang6), cos(ang6), 0, 0],
        [0, 0, 1, d6],
        [0, 0, 0, 1]
    ])

def T1(ang_1, ang_2, a_2, d_2, ang_3, a_3):
    return A_01(ang_1) * A_12(ang_2, a_2, d_2) * A_23(ang_3, a_3)

def T2(ang_4, d_4, ang_5, ang_6, d_6):
    return A_34(ang_4, d_4) * A_45(ang_5) * A_56(ang_6, d_6)

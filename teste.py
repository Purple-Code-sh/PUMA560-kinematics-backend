import sympy as sp
from sympy.matrices import Matrix
from sympy import *

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

# # Testing values to T1
# G1, G2, A2, D2, G3, A3= sp.symbols("G1 G2 A2 D2 G3 A3")
# Mat_A = T1(G1, G2, A2, D2, G3, A3)
# print(Mat_A)

# # Testing values to T2
# G4, D4, G5, G6, D6 = sp.symbols("g4 d4 g5 g6 d6")
# Mat_B = T2(G4, D4, G5, G6, D6)
# print(Mat_B)
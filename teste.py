import math
from sympy.matrices import Matrix

def A_01(ang1):
    return Matrix([
        [math.cos(math.radians(ang1)), 0, -math.sin(math.radians(ang1)), 0],
        [math.sin(math.radians(ang1)), 0, math.cos(math.radians(ang1)), 0],
        [0, -1, 0, 0],
        [0, 0, 0, 1]
    ])

def A_12(ang2, a2, d2):
    return Matrix([
        [math.cos(math.radians(ang2)), -math.sin(math.radians(ang2)), 0, a2 * math.cos(math.radians(ang2))],
        [math.sin(math.radians(ang2)), math.cos(math.radians(ang2)), 0, a2 * math.sin(math.radians(ang2))],
        [0, 0, 1, d2],
        [0, 0, 0, 1]
    ])

def A_23(ang3, a3):
    return Matrix([
        [math.cos(math.radians(ang3)), 0, math.sin(math.radians(ang3)), a3 * math.cos(math.radians(ang3))],
        [math.sin(math.radians(ang3)), 0, -math.cos(math.radians(ang3)), a3 * math.sin(math.radians(ang3))],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])

def A_34(ang4, d4):
    return Matrix([
        [math.cos(math.radians(ang4)), 0, -math.sin(math.radians(ang4)), 0],
        [math.sin(math.radians(ang4)), 0, math.cos(math.radians(ang4)), 0],
        [0, -1, 0, d4],
        [0, 0, 0, 1]
    ])

def A_45(ang5):
    return Matrix([
        [math.cos(math.radians(ang5)), 0, math.sin(math.radians(ang5)), 0],
        [math.sin(math.radians(ang5)), 0, -math.cos(math.radians(ang5)), 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])

def A_56(ang6, d6):
    return Matrix([
        [math.cos(math.radians(ang6)), -math.sin(math.radians(ang6)), 0, 0],
        [math.sin(math.radians(ang6)), math.cos(math.radians(ang6)), 0, 0],
        [0, 0, 1, d6],
        [0, 0, 0, 1]
    ])

def T1(ang_1, ang_2, a_2, d_2, ang_3, a_3):
    return A_01(ang_1) * A_12(ang_2, a_2, d_2) * A_23(ang_3, a_3)

def T2(ang_4, d_4, ang_5, ang_6, d_6):
    return A_34(ang_4, d_4) * A_45(ang_5) * A_56(ang_6, d_6)

def round_matrix(matrix, decimals=2):
    def round_and_check(value):
        rounded_value = round(value, decimals)
        if abs(rounded_value - int(rounded_value)) < 10**-decimals:
            return int(rounded_value)
        return rounded_value
    
    return matrix.applyfunc(round_and_check)

# Valores de prueba
G1 = 90
G2 = 10
A2 = 431.80
D2 = 149.09
G3 = 70
A3 = -20.32
G4 = 0
D4 = 433.07
G5 = 0
G6 = 0
D6 = 56.25

Mat_T1 = T1(G1, G2, A2, D2, G3, A3)
Mat_T2 = T2(G4, D4, G5, G6, D6)
#Mat_T = Mat_T1 * Mat_T2
Mat_T = Mat_T1 * A_34(G4,D4) #imprime solo T para A_04, la cual expresa la posición del centro de la muñeca, sin tomar en cuenta las rotaciones del efector final.

# Redondear la matriz final
Mat_T_rounded = round_matrix(Mat_T)

print(Mat_T_rounded)

# Las coordenadas obtenidas en la cuarta columna se leen tomando en consideración
# la regla de la mano derecha. Con el pulgar apuntando hacia arriba:
#   Z positivo esta en la direccion que apunta el pulgar
#   X positivo esta en la direccion que apunta el indice
#   Y positivo esta en la direccion que apunta el dedo medio

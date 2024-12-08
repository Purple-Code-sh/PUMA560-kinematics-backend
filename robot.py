import math
import roboticstoolbox as rtb
from spatialmath import SE3
import numpy as np

# Crear el modelo del PUMA 560
puma = rtb.models.DH.Puma560()

def fkine_con_grados(theta1_deg, theta2_deg, theta3_deg):
    """
    Calcula la cinemática directa del PUMA 560 tomando como entrada
    los primeros 3 ángulos en grados. Las últimas 3 juntas se asumen en 0°.
    Redondea todos los valores a 2 decimales.
    """

    # Convertir a radianes
    theta1_rad = math.radians(theta1_deg)
    theta2_rad = math.radians(theta2_deg)
    theta3_rad = math.radians(theta3_deg)

    # Asignar las últimas 3 juntas a 0 rad (0°)
    theta4_rad = 0.0
    theta5_rad = 0.0
    theta6_rad = 0.0

    # Vector q de configuración
    q = [theta1_rad, theta2_rad, theta3_rad, theta4_rad, theta5_rad, theta6_rad]

    # Cinemática directa
    T = puma.fkine(q)

    # Extraer la posición final (x, y, z)
    x, y, z = T.t

    # Redondear la matriz T_final.A
    T_rounded = np.round(T.A, 2)

    # Imprimir resultados con 2 decimales
    print("=== Cinemática Directa ===")
    print(f"Ángulos ingresados (grados): θ1={theta1_deg:.2f}, θ2={theta2_deg:.2f}, θ3={theta3_deg:.2f}, θ4=0°, θ5=0°, θ6=0°")
    print("Matriz de transformación final T_final (4x4):")
    print(T_rounded)
    print(f"Posición final del efector: x={x:.2f}, y={y:.2f}, z={z:.2f}")


if __name__ == "__main__":
    # Ejemplo: q=[0°, -90°, 90°, 0°, 0°, 0°]
    fkine_con_grados(15.54, 90.13, 89.95)

import math
import roboticstoolbox as rtb
from spatialmath import SE3

# Crear el modelo PUMA 560
puma = rtb.models.DH.Puma560()

def verificar_coherencia(theta1_deg, theta2_deg, theta3_deg, config='lun'):
    """
    Verifica la coherencia entre:
    - Angulos ingresados (primeros 3 DOF en grados, últimos 3 en 0).
    - La pose resultante (fkine).
    - La inversa (ikine_a) sobre esa pose.
    
    Parámetros:
    - theta1_deg, theta2_deg, theta3_deg: Angulos en grados de las primeras 3 juntas.
    - config: configuración para la inversa, por defecto 'lun'.

    Imprime por pantalla los valores para comparación.
    """

    # Convertir a radianes
    theta1_rad = math.radians(theta1_deg)
    theta2_rad = math.radians(theta2_deg)
    theta3_rad = math.radians(theta3_deg)

    # Asignar las últimas 3 juntas a 0 rad
    theta4_rad = 0.0
    theta5_rad = 0.0
    theta6_rad = 0.0

    # Vector q de configuración
    q = [theta1_rad, theta2_rad, theta3_rad, theta4_rad, theta5_rad, theta6_rad]

    # Cinemática directa
    T = puma.fkine(q)

    # Extraer la posición final (x, y, z)
    x, y, z = T.t

    print("=== Verificación de Coherencia ===")
    print(f"Ángulos iniciales (grados): θ1={theta1_deg}, θ2={theta2_deg}, θ3={theta3_deg}, θ4=0, θ5=0, θ6=0")
    print("Cinemática directa resultante:")
    print(f"Posición final: x={x:.4f}, y={y:.4f}, z={z:.4f}")
    print("Matriz de transformación T_final:")
    print(T.A)

    # Aplicar inversa analítica con la configuración dada
    sol = puma.ikine_a(T, config=config)

    if sol.success:
        q_inv = sol.q
        # Convertir los primeros 3 ángulos inversos a grados
        inv_theta1_deg = math.degrees(q_inv[0])
        inv_theta2_deg = math.degrees(q_inv[1])
        inv_theta3_deg = math.degrees(q_inv[2])

        print("\nCinemática inversa sobre la pose final:")
        print(f"Config utilizada: {config}")
        print(f"Solución inversa (primeros 3 ángulos en grados): θ1={inv_theta1_deg:.2f}, θ2={inv_theta2_deg:.2f}, θ3={inv_theta3_deg:.2f}")

        # Comparar con los originales
        diff1 = inv_theta1_deg - theta1_deg
        diff2 = inv_theta2_deg - theta2_deg
        diff3 = inv_theta3_deg - theta3_deg

        print("\nDiferencias respecto a los ángulos originales (en grados):")
        print(f"Δθ1={diff1:.2f}°, Δθ2={diff2:.2f}°, Δθ3={diff3:.2f}°")

    else:
        print("\nNo se encontró solución inversa con la configuración especificada.")


if __name__ == "__main__":
    # Ejemplo: supongamos que el frontend muestra θ1=0°, θ2=-90°, θ3=90°
    # En el frontend ves estos valores, y quieres verificar coherencia:
    verificar_coherencia(0, -90, 90, config='lun')

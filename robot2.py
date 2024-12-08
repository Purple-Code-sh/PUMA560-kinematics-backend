import math

def ik_3dof_puma(px, py, pz, ARM=1, ELBOW=1):
    # Parámetros DH PUMA 560 (primeros 3 eslabones)
    a2 = 431.8
    d2 = 149.09
    a3 = 20.32  # prueba cambiar a3 = 20.32 si no hay solución
    d4 = 433.07

    # θ1
    theta1 = math.atan2(ARM * py, ARM * px)

    r = math.sqrt(px**2 + py**2) - a2
    s = pz - d2

    D = (r**2 + s**2 - a3**2 - d4**2) / (2 * a3 * d4)
    if abs(D) > 1:
        raise ValueError("Posición fuera de alcance para θ3 (|D|>1).")

    # θ3 con codo arriba/abajo
    theta3 = math.atan2(ELBOW * math.sqrt(1 - D**2), D)
    alpha = math.atan2(s, r)
    beta = math.atan2(d4 * math.sqrt(1 - D**2), a3 + d4*D)

    theta2 = alpha - ELBOW * beta

    # Normalizar ángulos (-pi, pi)
    def angle_wrap(ang):
        while ang > math.pi:
            ang -= 2*math.pi
        while ang <= -math.pi:
            ang += 2*math.pi
        return ang

    return angle_wrap(theta1), angle_wrap(theta2), angle_wrap(theta3)

# Ejemplo de uso:
px, py, pz = 300.0, 200.0, 400.0  # ejemplo de punto de la muñeca
try:
    t1, t2, t3 = ik_3dof_puma(px, py, pz, ARM=1, ELBOW=1)
    print("Solución 3DOF:", math.degrees(t1), math.degrees(t2), math.degrees(t3))
except ValueError as e:
    print("Error:", e)

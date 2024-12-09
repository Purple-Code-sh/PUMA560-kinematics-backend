import math

def calcular_theta1(px, py, pz, d2, ARM):
    """
    Calcula el ángulo theta1 en base a la fórmula de tan⁻¹(sin/cos).
    """
    raiz = math.sqrt(max(px**2 + py**2 - d2**2, 0))  # Siempre positivo
    sin_theta1 = -ARM * py * raiz - px * d2
    cos_theta1 = -ARM * px * raiz + py * d2
    theta1 = math.atan2(sin_theta1, cos_theta1)
    return math.degrees(theta1)  # Convertir a grados


def calcular_theta2(px, py, pz, a2, d2, d4, a3, ARM, ELBOW):
    """
    Calcula el ángulo theta2 en base a la fórmula de tan⁻¹(sin/cos).
    """
    R = math.sqrt(max(px**2 + py**2 + pz**2 - d2**2, 0))  # R siempre positivo
    r = math.sqrt(max(px**2 + py**2 - d2**2, 0)) # r siempre positivo

    # Calcular sin y cos de alpha
    sin_alpha = -pz / R
    cos_alpha = -(ARM * r)/R

    # Calcular sin y cos de beta
    cos_beta = (a2**2 + R**2 - (d4**2 + a3**2)) / (2 * a2 * R)
    sin_beta = math.sqrt(max(1 - cos_beta**2, 0))  # Siempre positivo

    # Calcular sin y cos de theta2
    sin_theta2 = sin_alpha * cos_beta + cos_alpha * sin_beta * (ARM * ELBOW)
    cos_theta2 = cos_alpha * cos_beta - sin_alpha * sin_beta * (ARM * ELBOW)

    theta2 = math.atan2(sin_theta2, cos_theta2)
    return math.degrees(theta2)  # Convertir a grados


def calcular_theta3(px, py, pz, a2, d2, d4, a3, ARM, ELBOW):
    """
    Calcula el ángulo theta3 en base a la fórmula de tan⁻¹(sin/cos).
    """
    R = math.sqrt(max(px**2 + py**2 + pz**2 - d2**2, 0))  # R siempre positivo

    # Calcular sin y cos de phi
    cos_phi = (a2**2 + (d4**2 + a3**2) - R**2) / (2 * a2 * math.sqrt(d4**2 + a3**2))
    sin_phi = ARM * ELBOW * math.sqrt(max(1 - cos_phi**2, 0))  # Siempre positivo

    # Calcular sin y cos de beta
    sin_beta = d4 / math.sqrt(d4**2 + a3**2)
    cos_beta = abs(a3) / math.sqrt(d4**2 + a3**2)

    # Calcular sin y cos de theta3
    sin_theta3 = sin_phi * cos_beta - cos_phi * sin_beta
    cos_theta3 = cos_phi * cos_beta + sin_phi * sin_beta

    theta3 = math.atan2(sin_theta3, cos_theta3)
    return math.degrees(theta3)  # Convertir a grados


if __name__ == "__main__":
    # Ejemplo de parámetros
    px, py, pz =  -149.09, 848.20, 20.23
    a2, d2, d4, a3 = 431.80, 149.09, 433.07, -20.32
    ARM, ELBOW = -1, -1

    # Calcular los ángulos
    theta1 = calcular_theta1(px, py, pz, d2, ARM)
    theta2 = calcular_theta2(px, py, pz, a2, d2, d4, a3, ARM, ELBOW)
    theta3 = calcular_theta3(px, py, pz, a2, d2, d4, a3, ARM, ELBOW)

    # Imprimir resultados
    print(f"Theta1: {theta1:.2f}°")
    print(f"Theta2: {theta2:.2f}°")
    print(f"Theta3: {theta3:.2f}°")
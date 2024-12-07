import roboticstoolbox as rtb
import numpy as np

# Modelo del robot usando Denavit-Hartenberg (ejemplo básico)
def create_robot():
    # Configura aquí tu robot de 3 grados de libertad
    return rtb.DHRobot([
        rtb.RevoluteDH(a=1, alpha=0),  # Primer grado de libertad
        rtb.RevoluteDH(a=1, alpha=0),  # Segundo grado de libertad
        rtb.RevoluteDH(a=1, alpha=0),  # Tercer grado de libertad
    ], name="My3DOFRobot")

# Calcular ángulos para coordenadas XYZ
def calculate_angles(robot, xyz):
    try:
        # Cinemática inversa para obtener ángulos
        solution = robot.ikine_LM(np.array(xyz))
        if solution.success:
            return solution.q  # Devuelve los ángulos calculados
        else:
            raise ValueError("No se encontró solución válida para las coordenadas dadas.")
    except Exception as e:
        raise ValueError(f"Error en cálculo: {e}")

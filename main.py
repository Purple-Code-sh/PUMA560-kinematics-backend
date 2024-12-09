import math
from sympy.matrices import Matrix
import json
from fastapi import FastAPI, WebSocket

def A_01(theta1):
    return Matrix([
        [math.cos(math.radians(theta1)), 0, -math.sin(math.radians(theta1)), 0],
        [math.sin(math.radians(theta1)), 0, math.cos(math.radians(theta1)), 0],
        [0, -1, 0, 0],
        [0, 0, 0, 1]
    ])

def A_12(theta2, a2, d2):
    return Matrix([
        [math.cos(math.radians(theta2)), -math.sin(math.radians(theta2)), 0, a2 * math.cos(math.radians(theta2))],
        [math.sin(math.radians(theta2)), math.cos(math.radians(theta2)), 0, a2 * math.sin(math.radians(theta2))],
        [0, 0, 1, d2],
        [0, 0, 0, 1]
    ])

def A_23(theta3, a3):
    return Matrix([
        [math.cos(math.radians(theta3)), 0, math.sin(math.radians(theta3)), a3 * math.cos(math.radians(theta3))],
        [math.sin(math.radians(theta3)), 0, -math.cos(math.radians(theta3)), a3 * math.sin(math.radians(theta3))],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])

def A_34(theta4, d4):
    return Matrix([
        [math.cos(math.radians(theta4)), 0, -math.sin(math.radians(theta4)), 0],
        [math.sin(math.radians(theta4)), 0, math.cos(math.radians(theta4)), 0],
        [0, -1, 0, d4],
        [0, 0, 0, 1]
    ])

def round_matrix(matrix, decimals=2):
    def round_and_check(value):
        rounded_value = round(value, decimals)
        if abs(rounded_value - int(rounded_value)) < 10**-decimals:
            return int(rounded_value)
        return rounded_value
    
    return matrix.applyfunc(round_and_check)

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


A2 = 431.80
D2 = 149.09
A3 = -20.32
D4 = 433.07
THETA4 = 0

app = FastAPI()
# To start the server
# uvicorn main:app --reload --host 0.0.0.0 --port 8000

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        req = json.loads(data)

        # Obtener X, Y, Z y config del mensaje
        X = req.get("X", -149.09)
        Y = req.get("Y", 848.20)
        Z = req.get("Z", 20.23)
        arm = req.get("arm", -1)
        elbow = req.get("elbow", -1)

        try:
            # Calcular los ángulos
            theta1_deg = calcular_theta1(X, Y, Z, D2, arm)
            theta2_deg = calcular_theta2(X, Y, Z, A2, D2, D4, A3, arm, elbow)
            theta3_deg = calcular_theta3(X, Y, Z, A2, D2, D4, A3, arm, elbow)

            # Calcular las matrices
            T_0_1 = round_matrix(A_01(theta1_deg))
            T_0_2 = round_matrix(A_01(theta1_deg) * A_12(theta2_deg, A2, D2))
            T_0_3 = round_matrix(A_01(theta1_deg) * A_12(theta2_deg, A2, D2) * A_23(theta3_deg, A3))
            T_0_4 = round_matrix(A_01(theta1_deg) * A_12(theta2_deg, A2, D2) * A_23(theta3_deg, A3) * A_34(THETA4, D4))

            # Extraer coordenadas x, y, z de cada matriz
            coords_0_1 = [float(T_0_1[0, 3]), float(T_0_1[1, 3]), float(T_0_1[2, 3])]
            coords_0_2 = [float(T_0_2[0, 3]), float(T_0_2[1, 3]), float(T_0_2[2, 3])]
            coords_0_3 = [float(T_0_3[0, 3]), float(T_0_3[1, 3]), float(T_0_3[2, 3])]
            coords_0_4 = [float(T_0_4[0, 3]), float(T_0_4[1, 3]), float(T_0_4[2, 3])]

            # Preparar respuesta
            response = {
                "theta1_deg": theta1_deg,
                "theta2_deg": theta2_deg,
                "theta3_deg": theta3_deg,
                "coords_0_1": coords_0_1,
                "coords_0_2": coords_0_2,
                "coords_0_3": coords_0_3,
                "coords_0_4": coords_0_4
            }

            await websocket.send_text(json.dumps(response))
        except Exception as e:
            await websocket.send_text(json.dumps({"error": str(e)}))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sympy.matrices import Matrix
import math
from math import atan2, sqrt, cos, sin, radians, degrees

# Crear la aplicación FastAPI
app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar "*" por el origen del frontend en producción, como "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos: GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # Permitir todos los headers
)

# Modelo de datos para la solicitud
class IKRequest(BaseModel):
    X: float
    Y: float
    Z: float
    roll: float = 0  # Opcional
    pitch: float = 0  # Opcional
    yaw: float = 0  # Opcional

# Función para calcular la cinemática inversa
def inverse_kinematics(X, Y, Z, roll=0, pitch=0, yaw=0, a2=431.80, d2=149.09, a3=431.80, d4=149.09, d6=56.25):
    T_target = Matrix([
        [1, 0, 0, X],
        [0, 1, 0, Y],
        [0, 0, 1, Z],
        [0, 0, 0, 1]
    ])

    theta1_1 = atan2(Y, X)
    theta1_2 = atan2(-Y, -X)

    r = sqrt(X**2 + Y**2) - a2
    s = Z - d2

    # Recalcular D con los nuevos parámetros
    try:
        D = (r**2 + s**2 - a3**2 - d4**2) / (2 * a3 * d4)
    except ZeroDivisionError:
        return {"error": "Parámetros inválidos: División por cero en el cálculo de D."}

    print(f"Depuración: r = {r}, s = {s}, D = {D}")  # Depuración adicional

    if abs(D) > 1:
        return {"error": f"Posición fuera del alcance del robot. r: {r}, s: {s}, D: {D}"}

    theta3_1 = atan2(sqrt(1 - D**2), D)
    theta3_2 = atan2(-sqrt(1 - D**2), D)

    theta2_1 = atan2(s, r) - atan2(d4 * sqrt(1 - D**2), a3 + d4 * D)
    theta2_2 = atan2(s, r) - atan2(d4 * -sqrt(1 - D**2), a3 + d4 * D)

    solutions = []
    for theta1 in [theta1_1, theta1_2]:
        for theta3, theta2 in [(theta3_1, theta2_1), (theta3_2, theta2_2)]:
            T03 = A_01(theta1) * A_12(theta2, a2, d2) * A_23(theta3, a3)
            T36 = T03.inv() * T_target

            theta5 = atan2(sqrt(T36[0, 2]**2 + T36[1, 2]**2), T36[2, 2])
            theta4 = atan2(T36[1, 2], T36[0, 2])
            theta6 = atan2(-T36[2, 1], T36[2, 0])

            solutions.append((degrees(theta1), degrees(theta2), degrees(theta3),
                              degrees(theta4), degrees(theta5), degrees(theta6)))

    return {"solutions": solutions}


# Transformaciones homogéneas para cada articulación
def A_01(theta1):
    return Matrix([
        [cos(theta1), 0, -sin(theta1), 0],
        [sin(theta1), 0, cos(theta1), 0],
        [0, -1, 0, 0],
        [0, 0, 0, 1]
    ])

def A_12(theta2, a2, d2):
    return Matrix([
        [cos(theta2), -sin(theta2), 0, a2 * cos(theta2)],
        [sin(theta2), cos(theta2), 0, a2 * sin(theta2)],
        [0, 0, 1, d2],
        [0, 0, 0, 1]
    ])

def A_23(theta3, a3):
    return Matrix([
        [cos(theta3), 0, sin(theta3), a3 * cos(theta3)],
        [sin(theta3), 0, -cos(theta3), a3 * sin(theta3)],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])


# Endpoint para calcular la cinemática inversa
@app.post("/inverse-kinematics/")
async def calculate_ik(request: IKRequest):
    try:
        # Llamar a la función de cinemática inversa
        result = inverse_kinematics(request.X, request.Y, request.Z, request.roll, request.pitch, request.yaw)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

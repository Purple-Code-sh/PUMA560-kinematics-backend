from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from roboticstoolbox import DHRobot, RevoluteDH
from spatialmath import SE3
import json
import numpy as np

app = FastAPI()

# Longitudes de los eslabones
L1 = 120  # Longitud del primer eslabón en cm
L2 = 80   # Longitud del segundo eslabón en cm

# Crear el modelo del robot usando parámetros DH
robot = DHRobot([
    RevoluteDH(a=0, d=0, alpha=0),    # Articulación base (rotación horizontal)
    RevoluteDH(a=L1, d=0, alpha=0),   # Primer eslabón
    RevoluteDH(a=L2, d=0, alpha=0)    # Segundo eslabón
], name="Robot 2-DOF")

# Configurar límites amplios de las articulaciones para pruebas
robot.q_lim = np.array([
    [-np.pi, np.pi],           # Límite para la articulación 1
    [-np.pi, np.pi],           # Límite para la articulación 2
    [-np.pi, np.pi]            # Límite para la articulación 3
])

# Alcance máximo y mínimo del robot
R_max = L1 + L2  # Alcance máximo
R_min = abs(L1 - L2)  # Alcance mínimo


@app.websocket("/ws/web")
async def websocket_web_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Conexión WebSocket establecida con la página web")

    try:
        while True:
            # Recibir coordenadas XYZ en formato JSON
            data = await websocket.receive_text()
            coordinates = json.loads(data)
            print("Coordenadas recibidas:", coordinates)
            
            try:
                # Extraer coordenadas
                x, y, z = coordinates["x"], coordinates["y"], coordinates["z"]

                # Validar si las coordenadas están dentro del espacio de trabajo
                distance = np.sqrt(x**2 + y**2)
                if not (R_min <= distance <= R_max):
                    raise ValueError(
                        f"Coordenadas fuera del espacio de trabajo. "
                        f"Distancia mínima: {R_min} cm, máxima: {R_max} cm"
                    )

                # Crear el marco objetivo (SE3) con orientación fija
                target_pose = SE3(x, y, 0)  # Sin rotación adicional
                print(f"Marco objetivo (SE3): {target_pose}")

                # Configuración inicial para la cinemática inversa
                q0 = [np.pi / 4, -np.pi / 4, 0]
                print("Configuración inicial (q0):", q0)
                
                # Calcular ángulos con iteraciones extendidas usando ikine_LM
                solution = robot.ikine_LM(
                    target_pose, 
                    q0=q0, 
                    ilimit=2000, 
                    slimit=1000, 
                    tol=1e-6
                )

                # Verificar si se encontró una solución válida
                if solution.success:
                    angles = solution.q  # Ángulos calculados
                    response = {"angles": angles.tolist(), "status": "success"}
                else:
                    print("Información del error:", solution.reason)
                    response = {"error": "No se encontró una solución válida.", "status": "failure"}

            except ValueError as e:
                response = {"error": str(e), "status": "failure"}
            except Exception as e:
                print("Error inesperado en cinemática inversa:", e)
                response = {"error": f"Error inesperado: {e}", "status": "failure"}
            
            # Enviar respuesta al cliente
            print("Respuesta enviada al cliente:", response)  # Depuración
            await websocket.send_text(json.dumps(response))

    except WebSocketDisconnect:
        print("Conexión WebSocket cerrada.")

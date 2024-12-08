import math
import json
from fastapi import FastAPI, WebSocket
import roboticstoolbox as rtb

app = FastAPI()

# Cargar el modelo PUMA 560 predefinido en roboticstoolbox
puma = rtb.models.DH.Puma560()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Esperar mensaje JSON con X, Y, Z
    # Ejemplo de mensaje a enviar desde el frontend:
    # {"X":0.0203, "Y":-0.1501, "Z":0.6718, "config":"lun"}
    #
    # config es opcional, puedes pasarlo o no. Si no llega, usaremos 'lun'.

    while True:
        data = await websocket.receive_text()
        req = json.loads(data)

        # Obtener X, Y, Z y config del mensaje
        X = req.get("X", 0.0203)
        Y = req.get("Y", -0.1501)
        Z = req.get("Z", 0.6718)
        config = req.get("config", "lun")

        # Crear la matriz T a partir de las coordenadas XYZ para el efector
        # Suponemos aquí que la orientación es la misma que la pose en q=[0,-90°,90°,0,0,0].
        # En un caso real, deberías obtener T completa con orientación (R, p).
        # Para esta demo, crearemos una T con la orientación de la configuración inicial.
        # Usaremos la fkine inversa para una pose conocida o simplemente usaremos T desde el ejemplo.
        
        # Si no tienes orientación, asume R = identidad (esto no siempre es correcto):
        # PUMA 560 necesita las 6 DOF. Si solo das XYZ, la inversa analítica puede no ser única.
        # Para este ejemplo, asumamos que la pose coincide con la orientación de q=[0, -90°, 90°, 0, 0, 0]
        # la cual ya conocemos.
        
        # Configuración base para tener una orientación conocida
        q_test = [0, -math.pi/2, math.pi/2, 0, 0, 0]
        T_base = puma.fkine(q_test)

        # Reemplazamos la parte de traslación con (X,Y,Z)
        # Esto es solo una demostración. En un caso real debes tener la orientación también.
        T = T_base.A
        T[0,3] = X
        T[1,3] = Y
        T[2,3] = Z

        # Convertimos de nuevo a SpatialMath SE3
        T_final = rtb.SE3(T)

        # Resolver inversa analítica
        try:
            sol = puma.ikine_a(T_final, config=config)
            if sol.success:
                q = sol.q
                # Extraer primeros 3 ángulos
                theta1_rad, theta2_rad, theta3_rad = q[0], q[1], q[2]

                # Convertir a grados
                theta1_deg = math.degrees(theta1_rad)
                theta2_deg = math.degrees(theta2_rad)
                theta3_deg = math.degrees(theta3_rad)

                # Preparar respuesta
                response = {
                    "theta1_deg": theta1_deg,
                    "theta2_deg": theta2_deg,
                    "theta3_deg": theta3_deg
                }

                await websocket.send_text(json.dumps(response))
            else:
                await websocket.send_text(json.dumps({"error": "No se encontró solución"}))
        except Exception as e:
            await websocket.send_text(json.dumps({"error": str(e)}))

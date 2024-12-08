import math
import roboticstoolbox as rtb

# Cargar el modelo PUMA 560 definido por Peter Corke
puma = rtb.models.DH.Puma560()

# Prueba una configuración simple
q = [0, -math.pi/2, math.pi/2, 0, 0, 0]

# Cinemática directa
T = puma.fkine(q)
print("Pose con q=[0, -90°, 90°, 0, 0, 0]:")
print(T)

# Intentar la inversa analítica
# Debes indicar la configuración, por ejemplo 'run' (right, up, no-flip)
sol_a = puma.ikine_a(T, config='run')

print("Solución inversa ikine_a (analítica):")
print("q=", sol_a.q)
print("exitflag:", sol_a.success)

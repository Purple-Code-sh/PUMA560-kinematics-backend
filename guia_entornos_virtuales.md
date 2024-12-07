
# Guía Completa para Manejo de Entornos Virtuales en Python (Linux Ubuntu)

## 1. Crear un entorno virtual
Un entorno virtual es una instalación aislada de Python que permite trabajar con dependencias específicas sin afectar el sistema global. Para crear uno dentro de la carpeta `.venv`:

```bash
python3 -m venv .venv
```

**Nota:** Asegúrate de tener instalado el paquete `venv` en tu sistema. Si no lo tienes, instálalo con:

```bash
sudo apt install python3-venv
```

---

## 2. Activar el entorno virtual
Para usar el entorno virtual, debes activarlo con:

```bash
source .venv/bin/activate
```

### Cómo confirmar que está activado
1. El nombre del entorno (`(.venv)`) aparecerá al inicio de tu terminal.
2. Puedes verificar qué intérprete de Python está en uso con:

```bash
which python
```

Esto debe mostrar una ruta dentro de la carpeta `.venv`.

---

## 3. Desactivar el entorno virtual
Para salir del entorno virtual y volver al sistema global:

```bash
deactivate
```

---

## 4. Borrar el entorno virtual
Si deseas eliminar un entorno virtual para crear uno nuevo o limpiar dependencias innecesarias:

```bash
rm -rf .venv
```

---

## 5. Instalar y manejar paquetes con `pip`
Dentro del entorno activado, sigue estos pasos para manejar paquetes:

1. **Actualizar `pip` (recomendado):**

   ```bash
   python3 -m pip install --upgrade pip
   ```

2. **Verificar la versión de `pip`:**

   ```bash
   python3 -m pip --version
   ```

3. **Instalar paquetes necesarios:**

   ```bash
   python3 -m pip install nombre_paquete
   ```

4. **Instalar paquetes desde un archivo `requirements.txt`:**

   ```bash
   python3 -m pip install -r requirements.txt
   ```

5. **Ver los paquetes instalados:**

   ```bash
   pip list
   ```

---

## 6. Generar un archivo `requirements.txt`
Un archivo `requirements.txt` es útil para compartir las dependencias de tu proyecto. Para generarlo:

```bash
pip freeze > requirements.txt
```

Esto guardará todas las dependencias instaladas en el entorno en ese momento.

---

## 7. Ejecutar un programa dentro del entorno virtual
Con el entorno activado, puedes ejecutar tu programa con:

```bash
python3 nombre_archivo.py
```

---

## 8. Crear un entorno limpio desde `requirements.txt`
Si necesitas recrear el entorno en otra máquina o después de limpiar el actual:

1. Crea y activa un nuevo entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instala las dependencias necesarias:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

---

## 9. Buenas prácticas al trabajar con entornos virtuales

- **Mantén un archivo `requirements.txt` actualizado:**  
  Cada vez que instales un paquete nuevo, actualiza el archivo con:

  ```bash
  pip freeze > requirements.txt
  ```

- **Usa nombres descriptivos para entornos grandes:**  
  Si trabajas en varios proyectos, puedes usar nombres como `.env-project1`.

- **No incluyas el entorno en tu sistema de control de versiones (ej. Git):**  
  Añade `.venv` a tu archivo `.gitignore`.

- **Revisa dependencias:**  
  Instala solo lo necesario para evitar inflar el entorno.

---

## Resumen de Comandos

| **Acción**                       | **Comando**                               |
|----------------------------------|-------------------------------------------|
| Crear un entorno virtual         | `python3 -m venv .venv`                   |
| Activar el entorno virtual       | `source .venv/bin/activate`               |
| Confirmar entorno activado       | `which python`                            |
| Desactivar el entorno virtual    | `deactivate`                              |
| Borrar un entorno virtual        | `rm -rf .venv`                            |
| Actualizar pip                   | `python3 -m pip install --upgrade pip`    |
| Instalar paquetes                | `python3 -m pip install paquete`          |
| Ver paquetes instalados          | `pip list`                                |
| Guardar dependencias             | `pip freeze > requirements.txt`           |
| Instalar desde requirements.txt  | `python3 -m pip install -r requirements.txt` |
| Ejecutar un programa             | `python3 nombre_archivo.py`               |

---

## 10. Estructura típica de un proyecto con entorno virtual
Para mantener tu proyecto organizado, usa una estructura como esta:

```
proyecto/
├── .venv/                  # Entorno virtual (no incluir en Git)
├── main.py                 # Archivo principal del programa
├── requirements.txt        # Lista de dependencias
└── README.md               # Documentación del proyecto
```

**Nota:** Asegúrate de agregar `.venv` a tu archivo `.gitignore` para evitar subirlo a repositorios.

---


## En este caso, para iniciar el servidor que esta en main.py se utiliza lo siguiente
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Backend for 3-DOF Robotic Arm Inverse Kinematics

This backend application provides the calculations required for inverse kinematics of a 3-DOF robotic arm. It communicates with the frontend via WebSocket and computes the joint angles and trajectory points based on input coordinates and configuration.

---

## Features

- Calculates joint angles (\(	heta_1, 	heta_2, 	heta_3\)) using inverse kinematics formulas.
- Computes and sends transformation matrices and joint coordinates.
- Handles real-time WebSocket communication with the frontend.
- Utilizes FastAPI for lightweight and high-performance backend implementation.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/backend-repo-name.git
   ```
2. Navigate to the project folder:
   ```bash
   cd backend-repo-name
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate  # For Windows, use env\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## How It Works

1. **Input**:
   - Accepts target coordinates (\(X, Y, Z\)) and configuration options (`arm` and `elbow`) from the frontend via WebSocket.

2. **Inverse Kinematics Calculations**:
   - Computes joint angles using trigonometric equations and robot parameters.
   - Transformation matrices (\(T_{0_1}, T_{0_2}, T_{0_3}, T_{0_4}\)) are calculated to determine joint positions.

3. **Output**:
   - Returns the calculated joint angles and joint coordinates as JSON data to the frontend for visualization.

---

## Endpoints

- **WebSocket Endpoint**: `/ws`
   - Handles real-time communication between the frontend and backend.

---

## Technologies Used

- **Python**: Programming language.
- **FastAPI**: Framework for building the backend.
- **SymPy**: Library for symbolic mathematics, used for matrix operations.
- **Uvicorn**: ASGI server for running FastAPI.

---

## Example Input/Output

### Input:
```json
{
  "X": -149.09,
  "Y": 848.20,
  "Z": 20.23,
  "arm": -1,
  "elbow": -1
}
```

### Output:
```json
{
  "theta1_deg": 30.0,
  "theta2_deg": 45.0,
  "theta3_deg": 60.0,
  "coords_0_1": [100.0, 200.0, 300.0],
  "coords_0_2": [150.0, 250.0, 350.0],
  "coords_0_3": [200.0, 300.0, 400.0],
  "coords_0_4": [250.0, 350.0, 450.0]
}
```

---

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.

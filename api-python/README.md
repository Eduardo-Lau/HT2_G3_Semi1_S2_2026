# API 2 - Python (Flask)

API desarrollada en Python con Flask para la **Instancia-2** de la Hoja de Trabajo 2 (Seminario de Sistemas 1).

## Endpoints

- `GET /check`: Endpoint de verificación de estado (Health Check) que retorna código de estado `HTTP 200 OK`.
- `GET /info`: Endpoint que retorna los metadatos requeridos en formato JSON:
  ```json
  {
    "Instancia": "Maquina 2 - Api 2",
    "Curso": "Seminario de Sistemas 1 A",
    "Grupo": "Grupo 1"
  }
  ```

## Configuración y Ejecución Local

1. Crear entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar variables de entorno (editar `.env` si es necesario):
   ```bash
   PORT=5000
   INSTANCE_NAME="Maquina 2 - Api 2"
   COURSE_NAME="Seminario de Sistemas 1 A"
   GROUP_NAME="Grupo 1"
   ```

4. Iniciar el servidor:
   ```bash
   python app.py
   ```
   O usando Gunicorn (en Linux / Azure VM):
   ```bash
   gunicorn -w 2 -b 0.0.0.0:5000 app:app
   ```


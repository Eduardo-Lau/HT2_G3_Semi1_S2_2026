import os
from flask import Flask, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Mantener el orden de las llaves en la respuesta JSON
app.json.sort_keys = False

# Endpoint de verificación de estado (Health Check)
# Retorna HTTP 200 (OK)
@app.route('/check', methods=['GET'])
def check():
    return Response("OK", status=200, mimetype='text/plain')

# Endpoint de información de la API e Instancia
# Retorna la estructura JSON especificada en la Hoja de Trabajo 2
@app.route('/info', methods=['GET'])
def info():
    data = {
        "Instancia": os.getenv("INSTANCE_NAME", "Maquina 2 - Api 2"),
        "Curso": os.getenv("COURSE_NAME", "Seminario de Sistemas 1 - A"),
        "Grupo": os.getenv("GROUP_NAME", "Grupo 3")
    }
    return jsonify(data), 200

# Endpoint raíz informativo
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "mensaje": "API 2 (Python/Flask) activa",
        "endpoints": ["/check", "/info"]
    }), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"[API 2 - Python/Flask] Servidor escuchando en http://{host}:{port}")
    print(f"[Configuración] Instancia: {os.getenv('INSTANCE_NAME', 'Maquina 2 - Api 2')}")
    print(f"[Configuración] Curso: {os.getenv('COURSE_NAME', 'Seminario de Sistemas 1 - A')}")
    print(f"[Configuración] Grupo: {os.getenv('GROUP_NAME', 'Grupo 3')}")
    app.run(host=host, port=port, debug=False)


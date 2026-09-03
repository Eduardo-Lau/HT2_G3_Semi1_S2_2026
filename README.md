# Hoja de Trabajo 2 - Despliegue de APIs en Máquinas Virtuales con Balanceador de Carga en Azure

**Curso:** Seminario de Sistemas 1 (USAC)  
**Proyecto:** Entorno distribuido con dos APIs independientes (JavaScript y Python) balanceadas con Azure Load Balancer y prueba de tolerancia a fallos.

---

## Estructura del Repositorio

```text
HT2/
├── Context/
│   └── Hoja de trabajo 2.pdf     # Enunciado y requerimientos oficiales
├── api-node/                     # API 1: JavaScript (Node.js + Express) -> Instancia-1
│   ├── server.js                 # Servidor Express con /check y /info
│   ├── package.json              # Dependencias y scripts npm
│   ├── .env                      # Variables de entorno
│   ├── .env.example
│   └── README.md
├── api-python/                   # API 2: Python (Flask) -> Instancia-2
│   ├── app.py                    # Servidor Flask con /check y /info
│   ├── requirements.txt          # Dependencias (Flask, Flask-CORS, Gunicorn)
│   ├── .env                      # Variables de entorno
│   ├── .env.example
│   └── README.md
├── deploy/                       # Scripts y servicios para máquinas virtuales en Azure
│   ├── api-node.service          # Archivo de servicio systemd para API 1
│   ├── api-python.service        # Archivo de servicio systemd para API 2
│   ├── setup_vm1.sh              # Script de aprovisionamiento desatendido para Instancia-1
│   └── setup_vm2.sh              # Script de aprovisionamiento desatendido para Instancia-2
├── AZURE_DEPLOY_GUIDE.md         # Guía detallada para Azure y guion del video de 5 min
├── test_apis.py                  # Script para probar los endpoints localmente o en la nube
├── .gitignore                    # Reglas para Git (ignorar venv, node_modules, etc.)
└── README.md                     # Este archivo
```

---

## Endpoints Requeridos

Ambas APIs implementan los mismos dos endpoints obligatorios:

### 1. `GET /check`
- **Propósito:** Endpoint de verificación de estado para el Health Probe del Balanceador.
- **Respuesta:** Código `HTTP 200 OK`.

### 2. `GET /info`
- **Propósito:** Endpoint que retorna la información de la instancia en formato JSON.
- **Estructura:**
  ```json
  {
    "Instancia": "Maquina X - Api X",
    "Curso": "Seminario de Sistemas 1 A",
    "Grupo": "Grupo #"
  }
  ```

---

## Pruebas Locales

1. **Instalar dependencias de API 1:**
   ```bash
   cd api-node
   npm install
   npm start
   ```
   *Estará corriendo en `http://localhost:3000`.*

2. **Instalar dependencias de API 2:**
   *(En otra terminal)*
   ```bash
   cd api-python
   pip install -r requirements.txt
   python app.py
   ```
   *Estará corriendo en `http://localhost:5000`.*

3. **Ejecutar el script de verificación automatizado:**
   *(En otra terminal en la raíz del proyecto)*
   ```bash
   python test_apis.py
   ```

---

## Despliegue en Azure y Video

Consulta el archivo [AZURE_DEPLOY_GUIDE.md](file:///d:/carlo/OneDrive%20-%20Facultad%20de%20Ingenier%C3%ADa%20de%20la%20Universidad%20de%20San%20Carlos%20de%20Guatemala/USAC/S2%202026/Seminario%201/Lab/HT2/AZURE_DEPLOY_GUIDE.md) para el tutorial paso a paso de configuración de Azure Portal, aprovisionamiento con `deploy/setup_vm*.sh` y el guion cronometrado para la grabación del video grupal.


# Hoja de Trabajo 2 - Despliegue de APIs en Máquinas Virtuales con Balanceador de Carga en Azure

**Universidad de San Carlos de Guatemala**  
**Facultad de Ingeniería**  
**Curso:** Seminario de Sistemas 1 - Sección A  
**Grupo:** Grupo 3  
**Proyecto:** Entorno distribuido con dos APIs independientes (JavaScript y Python) balanceadas con Azure Load Balancer y prueba de tolerancia a fallos.

---

## Estructura del Repositorio

```text
HT2/
├── api-node/                     # API 1: JavaScript (Node.js + Express) -> Instancia-1
│   ├── server.js                 # Servidor Express con /check y /info
│   ├── package.json              # Dependencias y scripts npm
│   ├── .env.example              # Plantilla de variables de entorno
│   └── README.md
├── api-python/                   # API 2: Python (Flask) -> Instancia-2
│   ├── app.py                    # Servidor Flask con /check y /info
│   ├── requirements.txt          # Dependencias (Flask, Flask-CORS, Gunicorn)
│   ├── .env.example              # Plantilla de variables de entorno
│   └── README.md
├── deploy/                       # Scripts y servicios para máquinas virtuales en Azure
│   ├── api-node.service          # Archivo de servicio systemd para API 1
│   ├── api-python.service        # Archivo de servicio systemd para API 2
│   ├── setup_vm1.sh              # Script de aprovisionamiento desatendido para Instancia-1
│   └── setup_vm2.sh              # Script de aprovisionamiento desatendido para Instancia-2
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
    "Curso": "Seminario de Sistemas 1 - A",
    "Grupo": "Grupo 3"
  }
  ```

---

## Pruebas Locales

1. **Instalar dependencias e iniciar API 1:**
   ```bash
   cd api-node
   npm install
   npm start
   ```
   *Servicio disponible en `http://localhost:3000`.*

2. **Instalar dependencias e iniciar API 2:**
   *(En otra terminal)*
   ```bash
   cd api-python
   pip install -r requirements.txt
   python app.py
   ```
   *Servicio disponible en `http://localhost:5000`.*

3. **Ejecutar la verificación automatizada:**
   *(En otra terminal en la raíz del proyecto)*
   ```bash
   python test_apis.py
   ```

---

## Guía de Despliegue en Azure

---

### 1. Arquitectura General de la Solución

- **Grupo de Recursos:** `rg-semi1-ht2`.
- **Red Virtual (VNet):** `vnet-ht2` con subred `subnet-ht2` (`10.0.0.0/24`).
- **Máquinas Virtuales (Ubuntu 22.04 LTS):**
  - `Instancia-1`: Aloja la **API 1** (Node.js/Express) en el puerto `3000`.
  - `Instancia-2`: Aloja la **API 2** (Python/Flask) en el puerto `3000`.
- **Reglas de Red (NSG):**
  - Permitir SSH (puerto `22`).
  - Permitir HTTP (puerto `80`).
  - Permitir tráfico en puerto `3000`.
- **Balanceador de Carga (Azure Load Balancer):**
  - **Nombre:** `elb-semi1-ht2-Grupo3`
  - **SKU:** Standard o Basic (público).
  - **Frontend IP:** IP pública con etiqueta DNS (FQDN).
  - **Backend Pool:** Contiene a `Instancia-1` e `Instancia-2`.
  - **Health Probe:** Protocolo `HTTP`, Ruta `/check`, Puerto `3000`, Intervalo `5s`, Umbral de error `2`.
  - **Load Balancing Rule:** Frontend port `80` -> Backend port `3000`, Protocolo `TCP`, Health probe asignada, Sesión de persistencia `None` (para alternancia round-robin).

---

### 2. Paso a Paso: Creación y Configuración en Azure Portal

#### Paso 2.1: Crear Red Virtual y NSG
1. En el portal de Azure, crear un **Resource Group** (`rg-semi1-ht2`).
2. Crear un **Virtual Network** (VNet):
   - Nombre: `vnet-ht2`
   - Subred: `subnet-ht2` (`10.0.0.0/24`).
3. En el **Network Security Group (NSG)** de la subred o de las VMs, agregar las siguientes **Inbound security rules**:
   - `Allow-SSH`: Port `22`, Protocol `TCP`, Action `Allow`.
   - `Allow-HTTP`: Port `80`, Protocol `TCP`, Action `Allow`.
   - `Allow-API-Port`: Port `3000`, Protocol `TCP`, Action `Allow`.

---

#### Paso 2.2: Crear las Máquinas Virtuales

Crear dos máquinas virtuales con sistema operativo **Ubuntu Server 22.04 LTS**:

##### **Máquina 1: Instancia-1**
- **Virtual machine name:** `Instancia-1`
- **Autenticación:** Llave SSH o contraseña (usuario `azureuser`).
- **Networking:** Asignar a `vnet-ht2` / `subnet-ht2`.
- **Public IP:** Crear una IP pública (`ip-instancia-1`).

##### **Máquina 2: Instancia-2**
- **Virtual machine name:** `Instancia-2`
- **Autenticación:** Llave SSH o contraseña (usuario `azureuser`).
- **Networking:** Asignar a `vnet-ht2` / `subnet-ht2`.
- **Public IP:** Crear una IP pública (`ip-instancia-2`).

---

#### Paso 2.3: Desplegar las APIs en las VMs

Subir los archivos mediante Git, SFTP (Termius/FileZilla) o crearlos directamente en la instancia.

##### En `Instancia-1` (API 1 - Node.js):
1. Conectarse por SSH a `Instancia-1`:
   ```bash
   ssh azureuser@<IP_PUBLICA_INSTANCIA_1>
   ```
2. Clonar el repositorio o copiar la carpeta `HT2`:
   ```bash
   cd HT2
   chmod +x deploy/setup_vm1.sh
   ./deploy/setup_vm1.sh
   ```
   *El script instala automáticamente Node.js, las dependencias, crea el servicio `api-node.service` y arranca la API.*
3. Probar localmente en la VM:
   ```bash
   curl http://localhost:3000/check
   curl http://localhost:3000/info
   ```

##### En `Instancia-2` (API 2 - Python/Flask):
1. Conectarse por SSH a `Instancia-2`:
   ```bash
   ssh azureuser@<IP_PUBLICA_INSTANCIA_2>
   ```
2. Clonar el repositorio o copiar la carpeta `HT2`:
   ```bash
   cd HT2
   chmod +x deploy/setup_vm2.sh
   ./deploy/setup_vm2.sh
   ```
   *El script instala automáticamente Python, crea el entorno virtual `venv`, instala Flask/Gunicorn, crea el servicio `api-python.service` y arranca la API.*
3. Probar localmente en la VM:
   ```bash
   curl http://localhost:3000/check
   curl http://localhost:3000/info
   ```

---

#### Paso 2.4: Crear y Configurar el Azure Load Balancer

1. En Azure Portal, buscar y seleccionar **Load balancers** -> **+ Create**.
2. **Configuración básica:**
   - **Resource group:** `rg-semi1-ht2`
   - **Name:** `elb-semi1-ht2-Grupo3`
   - **Region:** Misma región de las VMs.
   - **Type:** Public.
   - **SKU:** Standard (o Basic).
3. **Frontend IP Configuration:**
   - Agregar configuración IP de front-end:
     - Nombre: `frontend-ip-ht2`
     - IP Version: IPv4
     - Public IP address: Crear nueva (`pip-elb-ht2`) y asignarle una etiqueta de nombre DNS (`semi1-ht2-grupo3`).
4. **Backend Pools:**
   - Nombre: `backend-pool-ht2`
   - Virtual Network: `vnet-ht2`
   - Backend IP configurations: Agregar `Instancia-1` e `Instancia-2`.
5. **Health Probes (Sonda de Estado):**
   - Nombre: `hp-check`
   - Protocol: `HTTP`
   - Port: `3000`
   - Path: `/check`
   - Interval: `5` segundos
   - Unhealthy threshold: `2` intentos consecutivos.
6. **Load Balancing Rules:**
   - Nombre: `rule-http-ht2`
   - Frontend IP address: `frontend-ip-ht2`
   - Protocol: `TCP`
   - Port (Frontend): `80` (o `3000`)
   - Backend port: `3000`
   - Backend pool: `backend-pool-ht2`
   - Health probe: `hp-check`
   - Session persistence: **None** (para permitir la alternancia round-robin entre instancias).

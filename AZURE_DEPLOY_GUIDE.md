# Guía de Despliegue en Microsoft Azure y Grabación de Video

**Curso:** Seminario de Sistemas 1 (USAC)  
**Actividad:** Hoja de Trabajo 2 - Despliegue de APIs en Máquinas Virtuales con Balanceador de Carga en Azure  

---

## 1. Arquitectura General de la Solución

- **Grupo de Recursos:** `rg-semi1-ht2` (o el de tu suscripción estudiantil).
- **Red Virtual (VNet):** `vnet-ht2` con subred `subnet-ht2` (ej. `10.0.0.0/24`).
- **Máquinas Virtuales (Ubuntu 22.04 o 24.04 LTS):**
  - `Instancia-1`: Aloja la **API 1** (Node.js/Express) en el puerto `3000`.
  - `Instancia-2`: Aloja la **API 2** (Python/Flask) en el puerto `3000`.
- **Reglas de Red (NSG):**
  - Permitir SSH (puerto `22`).
  - Permitir HTTP (puerto `80`).
  - Permitir tráfico en puerto `3000` (o el puerto configurado).
- **Balanceador de Carga (Azure Load Balancer):**
  - **Nombre obligatorio:** `elb-semi1-ht2-Grupo#` (reemplazar `#` por tu número de grupo).
  - **SKU:** Basic o Standard (público).
  - **Frontend IP:** IP pública con etiqueta DNS (FQDN).
  - **Backend Pool:** Contiene a `Instancia-1` e `Instancia-2`.
  - **Health Probe:** Protocolo `HTTP`, Ruta `/check`, Puerto `3000` (o `80` si usas proxy/reverse), Intervalo `5s`, Umbral de error `2`.
  - **Load Balancing Rule:** Frontend port `80` -> Backend port `3000`, Protocolo `TCP`, Health probe asignada, Sesión de persistencia `None` (para alternancia round-robin).

---

## 2. Paso a Paso: Creación y Configuración en Azure Portal

### Paso 2.1: Crear Red Virtual y NSG
1. En el portal de Azure, crea un **Resource Group** (ej. `rg-semi1-ht2`).
2. Crea un **Virtual Network** (VNet):
   - Nombre: `vnet-ht2`
   - Subred: `subnet-ht2` (`10.0.0.0/24`).
3. En el **Network Security Group (NSG)** de la subred o de las VMs, agrega las siguientes **Inbound security rules**:
   - `Allow-SSH`: Port `22`, Protocol `TCP`, Action `Allow`.
   - `Allow-HTTP`: Port `80`, Protocol `TCP`, Action `Allow`.
   - `Allow-API-Port`: Port `3000`, Protocol `TCP`, Action `Allow`.

---

### Paso 2.2: Crear las Máquinas Virtuales

Crea dos máquinas virtuales con sistema operativo **Ubuntu Server 22.04 LTS**:

#### **Máquina 1: Instancia-1**
- **Virtual machine name:** `Instancia-1` (exactamente como lo pide la práctica).
- **Autenticación:** SSH key o Contraseña (recuerda tu usuario, ej. `azureuser`).
- **Networking:** Asignar a `vnet-ht2` / `subnet-ht2`.
- **Public IP:** Crear una IP pública (ej. `ip-instancia-1`).

#### **Máquina 2: Instancia-2**
- **Virtual machine name:** `Instancia-2` (exactamente como lo pide la práctica).
- **Autenticación:** Misma credencial o SSH key.
- **Networking:** Asignar a `vnet-ht2` / `subnet-ht2`.
- **Public IP:** Crear una IP pública (ej. `ip-instancia-2`).

---

### Paso 2.3: Despliegue de las APIs en las VMs

Puedes subir los archivos mediante Git, SFTP (Termius/FileZilla) o crearlos directamente.

#### En `Instancia-1` (API 1 - Node.js):
1. Conéctate por SSH a `Instancia-1`:
   ```bash
   ssh azureuser@<IP_PUBLICA_INSTANCIA_1>
   ```
2. Clona tu repositorio o copia la carpeta `HT2`:
   ```bash
   # Si clonaste el repo:
   cd HT2
   chmod +x deploy/setup_vm1.sh
   ./deploy/setup_vm1.sh
   ```
   *El script `setup_vm1.sh` instalará automáticamente Node.js, las dependencias, creará el servicio `api-node.service` y arrancará la API.*
3. Prueba local en la VM:
   ```bash
   curl http://localhost:3000/check
   curl http://localhost:3000/info
   ```

#### En `Instancia-2` (API 2 - Python/Flask):
1. Conéctate por SSH a `Instancia-2`:
   ```bash
   ssh azureuser@<IP_PUBLICA_INSTANCIA_2>
   ```
2. Clona tu repositorio o copia la carpeta `HT2`:
   ```bash
   # Si clonaste el repo:
   cd HT2
   chmod +x deploy/setup_vm2.sh
   ./deploy/setup_vm2.sh
   ```
   *El script `setup_vm2.sh` instalará automáticamente Python, creará el entorno virtual `venv`, instalará Flask/Gunicorn, creará el servicio `api-python.service` y arrancará la API.*
3. Prueba local en la VM:
   ```bash
   curl http://localhost:3000/check
   curl http://localhost:3000/info
   ```

---

### Paso 2.4: Crear y Configurar el Azure Load Balancer

1. En Azure Portal, busca y selecciona **Load balancers** -> **+ Create**.
2. **Configuración básica:**
   - **Resource group:** `rg-semi1-ht2`
   - **Name:** `elb-semi1-ht2-Grupo#` *(Reemplaza `#` por tu número de grupo, ej. `elb-semi1-ht2-Grupo1`)*
   - **Region:** Misma región de las VMs.
   - **Type:** Public.
   - **SKU:** Standard (o Basic).
3. **Frontend IP Configuration:**
   - Agregar configuración IP de front-end:
     - Nombre: `frontend-ip-ht2`
     - IP Version: IPv4
     - Public IP address: Crear nueva (ej. `pip-elb-ht2`), asignarle una **etiqueta de nombre DNS** (ej. `semi1-ht2-grupo1`).
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
   - Session persistence: **None** (crucial para que el balanceador alterne entre ambas instancias).

---

## 3. Checklist y Guion para la Grabación del Video Grupal

> [!IMPORTANT]
> **Condiciones de la entrega:**
> - Duración máxima: **5 minutos**.
> - Subido a Google Drive con acceso público.
> - Entregar enlace en UEDI y Classroom.
> - La instancia a detener DEBE ser obligatoriamente **`Instancia-2`**.

### Estructura sugerida para el video (Minuto a Minuto):

| Minuto | Sección | Acción en pantalla / Diálogo |
|---|---|---|
| **0:00 - 0:45** | **Presentación del Equipo** | Todos los integrantes deben mostrar su rostro en cámara, decir su nombre completo y carnet. Indicar brevemente el número de grupo y el objetivo de la práctica. |
| **0:45 - 1:30** | **Configuración de VMs** | Mostrar en Azure Portal ambas máquinas virtuales (`Instancia-1` e `Instancia-2`), resaltando sus nombres exactos y sus direcciones **IPv4 públicas**. |
| **1:30 - 2:30** | **Prueba Directa de cada API** | Desde el navegador o Postman/Curl: <br>1. Acceder a `http://<IP_INSTANCIA_1>:3000/info` y mostrar el JSON (`"Maquina 1 - Api 1"`). <br>2. Acceder a `http://<IP_INSTANCIA_2>:3000/info` y mostrar el JSON (`"Maquina 2 - Api 2"`). |
| **2:30 - 3:30** | **Prueba del Balanceador** | 1. Mostrar la configuración del Load Balancer (`elb-semi1-ht2-Grupo#`), su DNS/IP pública y sus probes. <br>2. Consumir el DNS/IP del balanceador en `http://<DNS_ELB>/info`. <br>3. Refrescar varias veces para evidenciar que responde de forma **alternada** entre `Maquina 1` y `Maquina 2`. |
| **3:30 - 4:15** | **Prueba de Tolerancia a Fallos** | 1. Ir a Azure Portal y darle **Stop / Detener** a `Instancia-2`. <br>2. Volver a consultar `http://<DNS_ELB>/info`. Demostrar que el servicio sigue respondiendo sin caerse (ahora atendido únicamente por `Instancia-1`). |
| **4:15 - 5:00** | **Restauración y Cierre** | 1. Iniciar nuevamente `Instancia-2` (Start). <br>2. Esperar a que pase el health probe y demostrar nuevamente que el balanceador vuelve a distribuir carga entre ambas APIs. <br>3. Despedida y fin de la grabación. |


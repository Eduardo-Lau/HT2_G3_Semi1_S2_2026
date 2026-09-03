# API 1 - Node.js (JavaScript)

API desarrollada en Node.js con Express para la **Instancia-1** de la Hoja de Trabajo 2 (Seminario de Sistemas 1).

## Endpoints

- `GET /check`: Endpoint de verificación de estado (Health Check) que retorna código de estado `HTTP 200 OK`.
- `GET /info`: Endpoint que retorna los metadatos requeridos en formato JSON:
  ```json
  {
    "Instancia": "Maquina 1 - Api 1",
    "Curso": "Seminario de Sistemas 1 A",
    "Grupo": "Grupo 1"
  }
  ```

## Configuración y Ejecución Local

1. Instalar dependencias:
   ```bash
   npm install
   ```

2. Configurar variables de entorno (editar `.env` si es necesario):
   ```bash
   PORT=3000
   INSTANCE_NAME="Maquina 1 - Api 1"
   COURSE_NAME="Seminario de Sistemas 1 A"
   GROUP_NAME="Grupo 1"
   ```

3. Iniciar el servidor:
   ```bash
   npm start
   ```
   O en modo desarrollo:
   ```bash
   npm run dev
   ```


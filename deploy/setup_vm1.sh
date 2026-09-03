#!/bin/bash
# ==============================================================================
# Script de Aprovisionamiento para Instancia-1 (API 1 - Node.js)
# Hoja de Trabajo 2 - Seminario de Sistemas 1 (USAC)
# ==============================================================================

set -e

echo "=== [1/5] Actualizando repositorios del sistema ==="
sudo apt-get update -y
sudo apt-get install -y curl git ufw

echo "=== [2/5] Instalando Node.js (v20 LTS) ==="
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi
node -v
npm -v

echo "=== [3/5] Configurando directorio de la aplicación ==="
APP_DIR="/home/$USER/HT2/api-node"

# Si el script se ejecuta dentro de la carpeta clonada o subida:
if [ ! -d "$APP_DIR" ]; then
    mkdir -p "/home/$USER/HT2"
    if [ -d "./api-node" ]; then
        cp -r ./api-node "$APP_DIR"
    elif [ -f "./server.js" ]; then
        mkdir -p "$APP_DIR"
        cp -r ./* "$APP_DIR/"
    fi
fi

cd "$APP_DIR"

if [ ! -f .env ]; then
    echo "Creando archivo .env con valores por defecto..."
    cat <<EOT > .env
PORT=3000
INSTANCE_NAME="Maquina 1 - Api 1"
COURSE_NAME="Seminario de Sistemas 1 A"
GROUP_NAME="Grupo 1"
EOT
fi

echo "=== [4/5] Instalando dependencias de Node.js ==="
npm install

echo "=== [5/5] Configurando y arrancando servicio systemd ==="
SERVICE_FILE="/etc/systemd/system/api-node.service"

sudo bash -c "cat <<EOT > $SERVICE_FILE
[Unit]
Description=API 1 Node.js Express Service (Hoja de Trabajo 2)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$(which node) server.js
Restart=always
RestartSec=5
Environment=NODE_ENV=production
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
EOT"

sudo systemctl daemon-reload
sudo systemctl enable api-node
sudo systemctl restart api-node

echo "=== Estado del servicio ==="
sudo systemctl status api-node --no-pager

echo ""
echo "=== Verificando endpoints locales ==="
sleep 2
echo -n "Test /check: "
curl -s http://localhost:3000/check
echo ""
echo "Test /info: "
curl -s http://localhost:3000/info
echo ""
echo "=== ¡Instancia-1 configurada exitosamente en el puerto 3000! ==="


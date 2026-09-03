#!/bin/bash
# ==============================================================================
# Script de Aprovisionamiento para Instancia-2 (API 2 - Python/Flask)
# Hoja de Trabajo 2 - Seminario de Sistemas 1 (USAC)
# ==============================================================================

set -e

echo "=== [1/5] Actualizando repositorios del sistema ==="
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git curl ufw

echo "=== [2/5] Configurando directorio de la aplicación ==="
APP_DIR="/home/$USER/HT2/api-python"

if [ ! -d "$APP_DIR" ]; then
    mkdir -p "/home/$USER/HT2"
    if [ -d "./api-python" ]; then
        cp -r ./api-python "$APP_DIR"
    elif [ -f "./app.py" ]; then
        mkdir -p "$APP_DIR"
        cp -r ./* "$APP_DIR/"
    fi
fi

cd "$APP_DIR"

if [ ! -f .env ]; then
    echo "Creando archivo .env con valores por defecto..."
    cat <<EOT > .env
PORT=3000
INSTANCE_NAME="Maquina 2 - Api 2"
COURSE_NAME="Seminario de Sistemas 1 A"
GROUP_NAME="Grupo 1"
EOT
fi

echo "=== [3/5] Creando entorno virtual e instalando dependencias ==="
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

echo "=== [4/5] Configurando y arrancando servicio systemd ==="
SERVICE_FILE="/etc/systemd/system/api-python.service"

sudo bash -c "cat <<EOT > $SERVICE_FILE
[Unit]
Description=API 2 Python Flask Service (Hoja de Trabajo 2)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/gunicorn -w 2 -b 0.0.0.0:3000 app:app
Restart=always
RestartSec=5
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
EOT"

sudo systemctl daemon-reload
sudo systemctl enable api-python
sudo systemctl restart api-python

echo "=== Estado del servicio ==="
sudo systemctl status api-python --no-pager

echo ""
echo "=== Verificando endpoints locales ==="
sleep 2
echo -n "Test /check: "
curl -s http://localhost:3000/check
echo ""
echo "Test /info: "
curl -s http://localhost:3000/info
echo ""
echo "=== ¡Instancia-2 configurada exitosamente en el puerto 3000! ==="


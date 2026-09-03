require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Endpoint de verificación de estado (Health Check)
// Retorna HTTP 200 (OK)
app.get('/check', (req, res) => {
  res.status(200).send('OK');
});

// Endpoint de información de la API e Instancia
// Retorna la estructura JSON especificada en la Hoja de Trabajo 2
app.get('/info', (req, res) => {
  const infoData = {
    Instancia: process.env.INSTANCE_NAME || 'Maquina 1 - Api 1',
    Curso: process.env.COURSE_NAME || 'Seminario de Sistemas 1 A',
    Grupo: process.env.GROUP_NAME || 'Grupo 1'
  };
  res.status(200).json(infoData);
});

// Endpoint raíz informativo
app.get('/', (req, res) => {
  res.status(200).json({
    mensaje: 'API 1 (Node.js/Express) activa',
    endpoints: ['/check', '/info']
  });
});

// Iniciar el servidor
app.listen(PORT, '0.0.0.0', () => {
  console.log(`[API 1 - Node.js] Servidor escuchando en http://0.0.0.0:${PORT}`);
  console.log(`[Configuración] Instancia: ${process.env.INSTANCE_NAME || 'Maquina 1 - Api 1'}`);
  console.log(`[Configuración] Curso: ${process.env.COURSE_NAME || 'Seminario de Sistemas 1 A'}`);
  console.log(`[Configuración] Grupo: ${process.env.GROUP_NAME || 'Grupo 1'}`);
});


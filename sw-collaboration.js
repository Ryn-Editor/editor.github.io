// Service Worker para manejar el servidor de colaboración
const CACHE_NAME = 'collaboration-server-v1';
const SERVER_PORT = 3002;

// Instalar Service Worker
self.addEventListener('install', (event) => {
  console.log('📡 Service Worker de colaboración instalado');
  self.skipWaiting();
});

// Activar Service Worker
self.addEventListener('activate', (event) => {
  console.log('🚀 Service Worker de colaboración activado');
  event.waitUntil(self.clients.claim());
});

// Manejar mensajes del cliente
self.addEventListener('message', (event) => {
  const { type, data } = event.data;
  
  switch (type) {
    case 'START_SERVER':
      handleStartServer(event);
      break;
    case 'STOP_SERVER':
      handleStopServer(event);
      break;
    case 'CHECK_STATUS':
      handleCheckStatus(event);
      break;
    default:
      console.log('⚠️ Tipo de mensaje no reconocido:', type);
  }
});

// Iniciar servidor
async function handleStartServer(event) {
  try {
    console.log('🚀 Iniciando servidor de colaboración...');
    
    // Simular inicio del servidor
    const serverInfo = {
      port: SERVER_PORT,
      url: `ws://localhost:${SERVER_PORT}/collaboration`,
      status: 'running'
    };
    
    // Responder al cliente
    event.ports[0].postMessage({
      type: 'SERVER_STARTED',
      data: serverInfo
    });
    
    console.log('✅ Servidor iniciado:', serverInfo);
  } catch (error) {
    console.error('❌ Error iniciando servidor:', error);
    event.ports[0].postMessage({
      type: 'SERVER_ERROR',
      error: error.message
    });
  }
}

// Detener servidor
async function handleStopServer(event) {
  try {
    console.log('🛑 Deteniendo servidor de colaboración...');
    
    // Simular detención del servidor
    event.ports[0].postMessage({
      type: 'SERVER_STOPPED',
      data: { status: 'stopped' }
    });
    
    console.log('✅ Servidor detenido');
  } catch (error) {
    console.error('❌ Error deteniendo servidor:', error);
    event.ports[0].postMessage({
      type: 'SERVER_ERROR',
      error: error.message
    });
  }
}

// Verificar estado del servidor
async function handleCheckStatus(event) {
  try {
    // Simular verificación del estado
    const status = {
      isRunning: true,
      port: SERVER_PORT,
      url: `ws://localhost:${SERVER_PORT}/collaboration`
    };
    
    event.ports[0].postMessage({
      type: 'SERVER_STATUS',
      data: status
    });
  } catch (error) {
    console.error('❌ Error verificando estado:', error);
    event.ports[0].postMessage({
      type: 'SERVER_ERROR',
      error: error.message
    });
  }
}

// Manejar conexiones WebSocket (simulado)
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  
  // Interceptar requests al servidor de colaboración
  if (url.pathname === '/collaboration' && url.protocol === 'ws:') {
    event.respondWith(
      new Response('WebSocket Server Active', {
        status: 200,
        headers: {
          'Content-Type': 'text/plain'
        }
      })
    );
  }
});

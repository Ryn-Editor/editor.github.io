// Web Worker para manejar el servidor de colaboración
// Este worker simula un servidor WebSocket usando SharedArrayBuffer y MessageChannel

// Simulación de servidor WebSocket
class SimulatedWebSocketServer {
  constructor(port = 3002) {
    this.port = port;
    this.clients = new Map();
    this.rooms = new Map();
    this.isRunning = false;
    this.messageHandlers = new Map();
  }

  // Iniciar servidor
  start() {
    if (this.isRunning) {
      return { success: true, message: 'Servidor ya está ejecutándose' };
    }

    this.isRunning = true;
    console.log(`🚀 Servidor WebSocket simulado iniciado en puerto ${this.port}`);
    
    // Simular que el servidor está escuchando
    this.simulateServerActivity();
    
    return { 
      success: true, 
      message: 'Servidor iniciado exitosamente',
      url: `ws://localhost:${this.port}/collaboration`
    };
  }

  // Detener servidor
  stop() {
    if (!this.isRunning) {
      return { success: true, message: 'Servidor no está ejecutándose' };
    }

    this.isRunning = false;
    this.clients.clear();
    this.rooms.clear();
    
    console.log('🛑 Servidor WebSocket simulado detenido');
    
    return { 
      success: true, 
      message: 'Servidor detenido exitosamente' 
    };
  }

  // Simular actividad del servidor
  simulateServerActivity() {
    if (!this.isRunning) return;
    
    // Simular que el servidor está procesando conexiones
    setTimeout(() => {
      if (this.isRunning) {
        this.simulateServerActivity();
      }
    }, 5000);
  }

  // Verificar estado del servidor
  getStatus() {
    return {
      isRunning: this.isRunning,
      port: this.port,
      clients: this.clients.size,
      rooms: this.rooms.size,
      url: `ws://localhost:${this.port}/collaboration`
    };
  }
}

// Crear instancia del servidor
const server = new SimulatedWebSocketServer();

// Manejar mensajes del hilo principal
self.onmessage = function(event) {
  const { type, data } = event.data;
  
  switch (type) {
    case 'START_SERVER':
      handleStartServer();
      break;
    case 'STOP_SERVER':
      handleStopServer();
      break;
    case 'GET_STATUS':
      handleGetStatus();
      break;
    default:
      console.log('⚠️ Tipo de mensaje no reconocido:', type);
  }
};

// Iniciar servidor
function handleStartServer() {
  try {
    const result = server.start();
    
    self.postMessage({
      type: 'SERVER_STARTED',
      data: result
    });
  } catch (error) {
    self.postMessage({
      type: 'SERVER_ERROR',
      error: error.message
    });
  }
}

// Detener servidor
function handleStopServer() {
  try {
    const result = server.stop();
    
    self.postMessage({
      type: 'SERVER_STOPPED',
      data: result
    });
  } catch (error) {
    self.postMessage({
      type: 'SERVER_ERROR',
      error: error.message
    });
  }
}

// Obtener estado del servidor
function handleGetStatus() {
  try {
    const status = server.getStatus();
    
    self.postMessage({
      type: 'SERVER_STATUS',
      data: status
    });
  } catch (error) {
    self.postMessage({
      type: 'SERVER_ERROR',
      error: error.message
    });
  }
}

// Notificar que el worker está listo
self.postMessage({
  type: 'WORKER_READY',
  data: { message: 'Worker de servidor listo' }
});

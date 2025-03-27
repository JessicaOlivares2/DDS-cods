const EventSource = require('eventsource');

// URL del servidor SSE (ajusta según sea necesario)
const sseURL = 'http://127.0.0.1:8090/api/realtime';

// Crear una nueva conexión SSE
const source = new EventSource(sseURL);

source.onopen = () => {
  console.log('Conexión SSE abierta');
};

source.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Mensaje recibido:', data);

  // Si el evento corresponde a un pedido pendiente, lo mostramos
  if (data && data.action === 'create' && data.record.estado === 'Pendiente') {
    console.log(`Nuevo pedido pendiente recibido: ${JSON.stringify(data.record)}`);
  }
};

source.onerror = (error) => {
  console.error('Error en la conexión SSE:', error);
};

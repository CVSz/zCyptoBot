export function connectWS(tenant: string, onData: (d: any) => void) {
  const ws = new WebSocket(`ws://localhost:8000/ws/${tenant}`);
  ws.onmessage = (e) => {
    onData(JSON.parse(e.data));
  };
  return ws;
}

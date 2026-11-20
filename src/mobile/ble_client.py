"""Real BLE NUS client; UI callbacks must marshal onto their own thread."""
import asyncio
from threading import Thread, Event
from src.core.device_protocol import MAX_MESSAGE_BYTES, decode_message, encode_message, ProtocolError
from src.core.touch import touch_reply

SERVICE = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
RX = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
TX = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'


class LineReceiver:
    def __init__(self):
        self.pending = bytearray()

    def feed(self, data):
        messages = []
        for byte in data:
            if byte == 10:
                if self.pending:
                    try:
                        messages.append(decode_message(bytes(self.pending)))
                    except (ProtocolError, ValueError):
                        pass
                self.pending = bytearray()
            elif self.pending is not None:
                if len(self.pending) < MAX_MESSAGE_BYTES:
                    self.pending.append(byte)
                else:
                    self.pending = None
        return messages


class DeviceLink:
    def __init__(self, on_status, on_message):
        self.on_status, self.on_message = on_status, on_message
        self.thread = None
        self.stop_event = Event()

    def connect(self, address):
        if self.thread and self.thread.is_alive():
            return
        if not address.strip():
            self.on_status('Introduce la dirección BLE de tu placa')
            return
        self.stop_event.clear()
        self.thread = Thread(target=self._run, args=(address.strip(),), daemon=True)
        self.thread.start()

    def close(self):
        self.stop_event.set()

    def _run(self, address):
        try:
            asyncio.run(self._session(address))
        except Exception as exc:
            self.on_status('Error BLE: {}'.format(exc))
        else:
            self.on_status('Desconectado')

    async def _session(self, address, client_factory=None, scanner=None):
        if client_factory is None:
            from bleak import BleakClient, BleakScanner
            client_factory, scanner = BleakClient, BleakScanner
        self.on_status('Buscando placa…')
        device = await scanner.find_device_by_address(address, timeout=10)
        if device is None:
            raise RuntimeError('Placa no encontrada; comprueba dirección y Bluetooth')
        if self.stop_event.is_set():
            return
        receiver = LineReceiver()
        inbox = asyncio.Queue(maxsize=32)
        loop = asyncio.get_running_loop()

        def enqueue(data):
            for message in receiver.feed(data):
                if inbox.full():
                    self.on_status('Cola BLE llena; desconecta y vuelve a conectar')
                    self.stop_event.set()
                    return
                inbox.put_nowait(message)

        def notify(_, data):
            loop.call_soon_threadsafe(enqueue, bytes(data))

        async with client_factory(device) as client:
            service = client.services.get_service(SERVICE)
            if service is None or service.get_characteristic(RX) is None or service.get_characteristic(TX) is None:
                raise RuntimeError('La placa no ofrece el servicio BLE de Félix')
            await client.start_notify(TX, notify)

            async def write(raw):
                # 20 bytes works even with the default ATT MTU of 23.
                for offset in range(0, len(raw), 20):
                    await client.write_gatt_char(RX, raw[offset:offset+20], response=True)

            await write(encode_message('hello', {}, 'hello-1'))
            # Connected means a real protocol handshake, not merely a GATT link.
            deadline = loop.time() + 5
            while True:
                message = await asyncio.wait_for(inbox.get(), max(0.01, deadline-loop.time()))
                if message['type'] == 'hello_ack' and message.get('request_id') == 'hello-1':
                    break
                if loop.time() >= deadline:
                    raise TimeoutError('La placa no confirmó el protocolo')
            self.on_status('Conectado a Félix')
            while client.is_connected and not self.stop_event.is_set():
                try:
                    message = await asyncio.wait_for(inbox.get(), 0.2)
                except asyncio.TimeoutError:
                    continue
                if message['type'] == 'touch_event':
                    try:
                        reply = touch_reply(encode_message(message['type'], message.get('payload'), message.get('request_id')))
                    except ProtocolError:
                        continue
                    await write(reply)
                self.on_message(message)

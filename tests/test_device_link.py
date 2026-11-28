import asyncio
import unittest
from src.mobile.ble_client import DeviceLink, LineReceiver, SERVICE, RX, TX
from src.core.device_protocol import encode_message, decode_message, MAX_MESSAGE_BYTES
from src.firmware.device_session import DeviceSession
from src.firmware.bluetooth_bridge import BluetoothBridge


class Bridge:
    def __init__(self):
        self.sent = []
        self.inbox = []
        self.connected = True
    def send(self, message):
        self.sent.append(message)
        return self.connected
    def receive(self):
        return self.inbox.pop(0) if self.inbox else None
    def is_connected(self):
        return self.connected


class Display:
    def __init__(self): self.faces = []
    def show_felix_face(self, face): self.faces.append(face)


class LinkTests(unittest.TestCase):
    def test_fragmentation_invalid_and_overflow_recovery(self):
        receiver = LineReceiver()
        data = encode_message('touch_event', {'gesture': 'pet'}, '1')
        messages = []
        for byte in data:
            messages += receiver.feed(bytes([byte]))
        self.assertEqual(messages[0]['request_id'], '1')
        self.assertEqual(receiver.feed(b'x'*(MAX_MESSAGE_BYTES+10)), [])
        self.assertEqual(receiver.feed(b'\ninvalid\n'+data), messages)

    def test_session_only_accepts_correlated_emotion(self):
        bridge, display = Bridge(), Display()
        session = DeviceSession(bridge, display)
        session.touch('pet')
        request_id = bridge.sent[-1]['request_id']
        bridge.inbox = [dict(type='emotion', payload={'name':'angry'}, request_id='wrong'),
                        dict(type='emotion', payload={'name':'angry'}, request_id=request_id)]
        session.poll()
        self.assertEqual(display.faces, ['happy', 'surprised'])
        self.assertEqual(session.pending, [])
        bridge.inbox = [dict(type='hello', request_id='hello-1')]
        session.poll()
        self.assertEqual(bridge.sent[-1]['type'], 'hello_ack')

    def test_firmware_notifications_respect_default_mtu(self):
        chunks = []
        class Radio:
            def gatts_notify(self, connection, handle, data): chunks.append(data)
        bridge = BluetoothBridge()
        bridge.ble, bridge.connected, bridge._tx_handle = Radio(), True, 1
        bridge._connections = {7}
        self.assertTrue(bridge.send(dict(type='touch_event', payload={'gesture':'pet'}, request_id='1')))
        self.assertTrue(all(len(chunk)<=20 for chunk in chunks))
        self.assertEqual(decode_message(b''.join(chunks))['type'], 'touch_event')

    def test_real_client_path_handshake_touch_reply_and_cleanup(self):
        statuses, messages, writes = [], [], []
        link = DeviceLink(statuses.append, messages.append)
        bridge, display = Bridge(), Display()
        session = DeviceSession(bridge, display)
        receiver = LineReceiver()
        class Scanner:
            @staticmethod
            async def find_device_by_address(address, timeout): return address
        class Service:
            def get_characteristic(self, uuid): return uuid if uuid in (RX, TX) else None
        class Services:
            def get_service(self, uuid): return Service() if uuid == SERVICE else None
        class Client:
            services = Services()
            is_connected = True
            closed = False
            def __init__(self, device): pass
            async def __aenter__(self): return self
            async def __aexit__(self, *args): Client.closed = True
            async def start_notify(self, uuid, callback): self.callback = callback
            async def write_gatt_char(self, uuid, data, response):
                writes.append(data)
                bridge.inbox.extend(receiver.feed(data))
                session.poll()
                while bridge.sent:
                    msg = bridge.sent.pop(0)
                    raw = encode_message(msg['type'], msg['payload'], msg.get('request_id'))
                    for offset in range(0,len(raw),20): self.callback(None, raw[offset:offset+20])
                    if msg['type'] == 'hello_ack': session.touch('pet')
                if display.faces == ['happy', 'happy']: link.close()
        asyncio.run(link._session('AA:BB:CC:DD:EE:FF', Client, Scanner))
        self.assertIn('Conectado a Félix', statuses)
        self.assertEqual(messages[0]['type'], 'touch_event')
        self.assertEqual(display.faces, ['happy', 'happy'])
        self.assertTrue(Client.closed)
        self.assertTrue(all(len(chunk)<=20 for chunk in writes))

    def test_touch_before_handshake_is_delivered_and_answered(self):
        statuses, messages, replies = [], [], []
        link = DeviceLink(statuses.append, messages.append)
        receiver = LineReceiver()
        class Scanner:
            @staticmethod
            async def find_device_by_address(address, timeout): return address
        class Service:
            def get_characteristic(self, uuid): return uuid
        class Services:
            def get_service(self, uuid): return Service()
        class Client:
            services = Services()
            is_connected = True
            closed = False
            def __init__(self, device): pass
            async def __aenter__(self): return self
            async def __aexit__(self, *args): Client.closed = True
            async def start_notify(self, uuid, callback): self.callback = callback
            async def write_gatt_char(self, uuid, data, response):
                for message in receiver.feed(data):
                    if message['type'] == 'hello':
                        self.callback(None, encode_message('touch_event', {'gesture': 'pet'}, 'early'))
                        self.callback(None, encode_message('hello_ack', {}, 'hello-1'))
                    elif message['type'] == 'emotion':
                        replies.append(message)
                        link.close()
        async def run():
            await asyncio.wait_for(link._session('test', Client, Scanner), 1)
        asyncio.run(run())
        self.assertEqual([m['request_id'] for m in messages], ['early'])
        self.assertEqual(replies[0]['request_id'], 'early')
        self.assertEqual(replies[0]['payload']['name'], 'happy')
        self.assertIn('Conectado a Félix', statuses)
        self.assertTrue(Client.closed)

    def test_unknown_device_never_reports_connected(self):
        statuses = []
        link = DeviceLink(statuses.append, lambda _: None)
        class Scanner:
            @staticmethod
            async def find_device_by_address(address, timeout): return None
        with self.assertRaises(RuntimeError):
            asyncio.run(link._session('missing', object, Scanner))
        self.assertNotIn('Conectado a Félix', statuses)

if __name__ == '__main__': unittest.main()


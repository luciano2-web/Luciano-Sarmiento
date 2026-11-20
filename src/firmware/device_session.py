"""Nonblocking application routing for the BLE bridge (MicroPython compatible)."""


class DeviceSession:
    def __init__(self, bridge, display):
        self.bridge = bridge
        self.display = display
        self.counter = 0
        self.pending = []

    def touch(self, gesture):
        if gesture not in ('pet', 'annoyed'):
            return
        self.counter += 1
        request_id = str(self.counter)
        # Local feedback remains available when no phone is connected.
        self.display.show_felix_face('happy' if gesture == 'pet' else 'surprised')
        if self.bridge.send({'type': 'touch_event', 'payload': {'gesture': gesture}, 'request_id': request_id}):
            self.pending.append(request_id)
            self.pending = self.pending[-16:]

    def poll(self):
        if not self.bridge.is_connected():
            self.pending = []
        # Bound work per iteration so a busy phone cannot starve the touch sensor.
        for _ in range(8):
            message = self.bridge.receive()
            if message is None:
                break
            kind = message['type']
            request_id = message.get('request_id')
            if kind in ('hello', 'ping'):
                self.bridge.send({'type': 'hello_ack' if kind == 'hello' else 'pong',
                                  'payload': {}, 'request_id': request_id})
            elif kind == 'emotion' and request_id in self.pending:
                name = message.get('payload', {}).get('name')
                if name in ('happy', 'angry'):
                    self.pending.remove(request_id)
                    # OLED currently has no angry drawing; use surprised explicitly.
                    self.display.show_felix_face('surprised' if name == 'angry' else name)

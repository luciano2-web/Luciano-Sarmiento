"""Kivy controls for a real board connection, separate from simulated gestures."""
from functools import partial
from src.mobile.ble_client import DeviceLink


def install_ble_panel(app, root):
    from kivy.clock import Clock
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    panel = BoxLayout(orientation='vertical', size_hint_y=0.18)
    address = TextInput(hint_text='Dirección BLE de tu ESP32', multiline=False)
    status = Label(text='Placa desconectada')
    buttons = BoxLayout()
    connect = Button(text='Conectar placa')
    disconnect = Button(text='Desconectar')

    def update_status(text, dt):
        if not app._stopped:
            status.text = text

    def update_message(message, dt):
        if app._stopped:
            return
        if message['type'] == 'touch_event':
            gesture = message.get('payload', {}).get('gesture')
            if gesture in ('pet', 'annoyed'):
                app.touch_face.text = 'Placa: ' + ('^_^ Feliz' if gesture == 'pet' else '>_< Enojado')

    link = DeviceLink(lambda text: Clock.schedule_once(partial(update_status, text)),
                      lambda msg: Clock.schedule_once(partial(update_message, msg)))

    def start(*args):
        if app._stopped:
            return
        # Android permissions are requested on the UI thread before BLE work.
        from kivy.utils import platform
        if platform == 'android':
            from android.permissions import request_permissions
            from jnius import autoclass
            sdk = autoclass('android.os.Build$VERSION').SDK_INT
            permissions = (['android.permission.BLUETOOTH_SCAN', 'android.permission.BLUETOOTH_CONNECT']
                           if sdk >= 31 else ['android.permission.ACCESS_FINE_LOCATION'])

            def granted(names, results):
                if results and all(results):
                    Clock.schedule_once(lambda dt: None if app._stopped else link.connect(address.text))
                else:
                    Clock.schedule_once(partial(update_status, 'Permiso Bluetooth denegado'))
            request_permissions(permissions, granted)
        else:
            link.connect(address.text)

    connect.bind(on_release=start)
    disconnect.bind(on_release=lambda *_: link.close())
    buttons.add_widget(connect)
    buttons.add_widget(disconnect)
    panel.add_widget(address)
    panel.add_widget(buttons)
    panel.add_widget(status)
    root.add_widget(panel)
    return link

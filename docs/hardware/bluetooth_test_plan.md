# Simulación del enlace de Félix

## Qué comprueba
- La app envía un mensaje `hello` y el robot simulado lo recibe.
- El robot simulado responde `hello_ack` y la app lo recibe.
- El formato conserva texto español y un identificador de petición.
- Se rechazan tipos desconocidos y versiones incompatibles.
- Un enlace desconectado no acepta nuevos mensajes.

## Cómo ejecutarla
Desde la raíz del repositorio:

```bash
python -m unittest tests.test_device_protocol -v
```

## Qué NO demuestra
Esta prueba usa colas en memoria. **No enciende el ESP32 ni usa la radio Bluetooth**.
No prueba emparejamiento, BLE/GATT, alcance, interferencias, micrófono, parlante,
ni compatibilidad con Android/Windows. Es una prueba del protocolo y del flujo
lógico, no una certificación del hardware.

## Estado Bluetooth veraz
El puente anterior configuraba UART por GPIO 19/18 y marcaba `connected=True`
sin detectar un dispositivo remoto. UART por sí solo no es Bluetooth. Por eso
no se puede afirmar que la conexión Bluetooth estuviera funcionando. El siguiente
paso es implementar y probar BLE GATT en el ESP32 y un cliente BLE en Android/
Windows; ambos extremos deben intercambiar `hello` y `hello_ack` físicamente.

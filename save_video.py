import obswebsocket
from obswebsocket import obsws, requests


try:
    ws = obsws('localhost', 4444, 'your_password')
    ws.connect()
    print("Conectado ao OBS WebSocket")

    ws.call(requests.StartRecording())
    print("Gravação iniciada")

    ws.disconnect()
    print("Desconectado do OBS WebSocket")

except obswebsocket.exceptions.ConnectionFailure as e:
    print(f"Falha na conexão: {e}")
except Exception as e:
    print(f"Ocorreu um erro: {e}")

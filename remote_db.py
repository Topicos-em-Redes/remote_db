import paho.mqtt.client as mqtt
import requests
import json
from datetime import datetime

# Configurações
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "seu/topico/aqui"  # Altere para o tópico desejado

FIREBASE_URL = "https://ttredes-iot-database-default-rtdb.firebaseio.com/mensagens.json"

def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker com código:", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    ts = datetime.now().isoformat()
    print(f"Recebido em {ts}: {payload}")

    # Dados a serem enviados ao Firebase
    data = {
        "timestamp": ts,
        "payload": payload
    }
    try:
        response = requests.post(FIREBASE_URL, data=json.dumps(data))
        if response.status_code == 200:
            print("Enviado ao Firebase com sucesso!")
        else:
            print("Falha ao enviar ao Firebase:", response.text)
    except Exception as e:
        print("Erro ao enviar ao Firebase:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
print(f"Escutando tópico '{MQTT_TOPIC}' no broker {MQTT_BROKER}:{MQTT_PORT}...")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Encerrando...")
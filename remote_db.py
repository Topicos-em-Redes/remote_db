import paho.mqtt.client as mqtt
import requests
import json
from datetime import datetime


# Configurações para conexão segura
MQTT_BROKER = "localhost"
MQTT_PORT = 8883  # Porta segura
MQTT_TOPIC = "esp32/rain_sensor"  # Altere para o tópico desejado

# Caminhos dos certificados gerados pelo script config_mosquitto.py
CLIENT_CERT = "/certs/firebase_db/firebase_db.crt"
CLIENT_KEY = "/certs/firebase_db/firebase_db.key"
CA_CERT = "/certs/firebase_db/ca.crt"

# Credenciais
MQTT_USERNAME = "firebase_db"
MQTT_PASSWORD = "1234"

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

# Configura autenticação
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Configura TLS/mTLS
client.tls_set(ca_certs=CA_CERT, certfile=CLIENT_CERT, keyfile=CLIENT_KEY)

client.connect(MQTT_BROKER, MQTT_PORT, 60)
print(f"Escutando tópico '{MQTT_TOPIC}' no broker {MQTT_BROKER}:{MQTT_PORT} (TLS)...")

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Encerrando...")
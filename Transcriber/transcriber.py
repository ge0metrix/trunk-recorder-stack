import random
import time
import json
from paho.mqtt import client as mqtt_client
import speech_recognition as sr
import os
from datetime import datetime


AZUREKEY = os.getenv("AZUREKEY")
broker = 'mosquitto'
port = 1883
#topic = "trunkrecorder/status/call_end"
subtopic = "transcribe/todo/#"
pubtopic = "transcribe/done"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

r = sr.Recognizer()


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def transcribe_file(filepath:str):
    filepath = filepath.replace("m4a","wav")
    x = ("",0)
    with sr.AudioFile(filepath) as source:
        audio = r.record(source)  # read the entire audio file
    print(f"transcribing {filepath}")
    try:
        x = r.recognize_azure(audio, key=AZUREKEY, location='eastus')
    except Exception as e:
        print(datetime.now(), e, x)
        raise e
    #print(x)
    return x


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        data = json.loads(msg.payload.decode())
        filepath = data.get("call_filename")
        #filepath = "1-1704418526_483125000.0-call_0.wav"
        #print(data.get("call").get("call_filename"))
        try:
            transcript = transcribe_file(filepath=filepath)
            data["transcript"] = transcript
            print(data.get("sys_name"), ":", data.get("transcript"))
            publish(client, topic=pubtopic, msg = data)
        except Exception as e:
            print(data, e)

    client.subscribe(subtopic, qos=2)
    client.on_message = on_message

def publish(client, topic, msg):
    result = client.publish(topic, json.dumps(msg))
    # result: [0, 1]
    status = result[0]
    if status == 0:
        pass
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")




def run():
    print("starting transcription")
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

print("Starting Transcription Watcher", AZUREKEY)
run()
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 17:05:30 2022
@author: luise
"""
import paho.mqtt.client as mqtt
import threading as th
import sounddevice as sd
from scipy.io.wavfile import write
import librosa as lib

fs = 44100
second = 4

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 17:05:30 2022
@author: luise
"""
import paho.mqtt.client as mqtt
import threading as th
import sounddevice as sd
from scipy.io.wavfile import write
import librosa as lib

fs = 44100
second = 4

#MQTT Thread Function

def MQTT_TH(client):    
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("luisaraujo/pedido")
 
    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        #print('Message received: ' + str(msg.payload))
        record_voice = sd.rec( int( second * fs ) , samplerate = fs , channels = 2 )
        sd.wait()
        write("som.wav", fs , record_voice )
        x, sr = lib.load("som.wav") 
        pm = lib.feature.rms(y=x,  frame_length=44100)
        #bytearray ver esta parte do envio de daos -> receber uma string aqui
        #<- enviar bytearray par ao outro lado
        pm = str(pm.tolist())
        client.publish("luisaraujo/dados", pm)

    print('Incializing MQTT')
    #client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
  
    client.connect("mqtt.eclipseprojects.io", 1883, 60)
   
    client.loop_forever()

t = th.Thread(target=MQTT_TH, args=[mqtt.Client()])
t.start()

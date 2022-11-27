# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 20:51:34 2022

@author: luise
"""
import streamlit as st
import paho.mqtt.client as mqtt
import threading

client = mqtt.Client()
client.connect("mqtt.eclipseprojects.io", 1883, 60)

def on_connect(client, userdata, flags, rc):
    print("streamlit subscribed ")
    client.subscribe("luisaraujo.dados")
 
def on_message(client, userdata, msg):
    print(msg.topic)
    
class subscrever:
    def subscribe(self):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        print("subscribing")
        client.loop_forever()
    
    def __init__(self):
        t = threading.Thread(target=self.subscribe())
        t.start()
class publicar:
    def publish(self):        
        client.publish("luisaraujo", 'pedido')
    def __init__(self):
        t = threading.Thread(target=self.publish())
        t.start()
        

#botão
if st.button('iniciar gravação'):
    subscrever()
    publicar()

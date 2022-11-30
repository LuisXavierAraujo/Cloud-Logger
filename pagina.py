# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 20:51:34 2022

@author: luise
"""
import streamlit as st
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import paho.mqtt.client as mqtt
import threading as th
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
from streamlit_autorefresh import st_autorefresh

df = pd.DataFrame(columns = ['pm','times'])
st_autorefresh(interval=5000)
st.dataframe(df)


    

#MQTT Thread Function
def MQTT_TH(client):   

    def on_connect(client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.        
        client.subscribe("luisaraujo/dados")
 
    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(json.loads(msg.payload))
        #data = json.loads(msg.payload)
        #print(data)
        #...df.append({"pm": data[0][0], "times": data[0][1]}, ignore_index = True)
        #df1 = {"pm": json.loads(msg.payload)[0], "times": json.loads(msg.payload)[1]}
        #pd.concat([df, df1])
        

    #client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.loop_forever()

if 'mqttThread' not in st.session_state:
    st.session_state.mqttClient = mqtt.Client()
    st.session_state.mqttThread = th.Thread(target=MQTT_TH, args=[st.session_state.mqttClient])
    add_script_run_ctx(st.session_state.mqttThread)
    st.session_state.mqttThread.start()

#botão
if st.checkbox('iniciar gravação'):
    st.session_state.mqttClient.publish("luisaraujo/pedido", payload="start")
    print("Pedido Enviado")

#df = pd.DataFrame(columns = ['Teste1', 'Teste2', 'Teste3'])
#df = df.append({'Teste1' : "olá", 'Teste2' : 77, 'Teste3': 56}, ignore_index = True)

#def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    #return df.to_csv().encode('utf-8')

#csv = convert_df(df)

#st.download_button(
#    label="Download data as CSV",
#    data=csv,
#    file_name='data.csv',
#    mime='text/csv',
#)


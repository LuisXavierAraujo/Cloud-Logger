# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 20:51:34 2022

@author: luise
"""
import csv
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
from csv import writer
entrei = False
st_autorefresh(interval=5000)
#st.dataframe(df)  

#MQTT Thread Function
def MQTT_TH(client):   

    def on_connect(client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.        
        client.subscribe("luisaraujo/dados")
 
    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        entrei = True
        df = pd.DataFrame(columns = ['PM', 'Times'])
        data = json.loads(msg.payload)
        df = df.append({'PM' : data[0], 'Times' : data[1]}, ignore_index = True)
        df.to_csv('current_data.csv', index=False)
        #list1 = np.random.randn(1,20)[0].tolist()
        #list2 = np.random.randn(1,20)[0].tolist()
        #df = df.append({'PM' : list1, 'Times' : list2}, ignore_index = True)
        print("Recebi")
        #df = pd.DataFrame(columns = ['lista1', 'lista2', 'lista3'])
        #list1 = np.random.randn(1,2)[0].tolist()
        #list2 = np.random.randn(1,2)[0].tolist()
        #list3 = np.random.randn(1,2)[0].tolist()
        #df = df.append({'lista1' : list1, 'lista2' : list2, 'lista3': list3}, ignore_index = True)
        #df.to_csv('current_data.csv', index=False)

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



#with open("/workspace/Cloud-Logger/current_data.csv", 'r') as file:
#    print("Entrei")
#    csvreader = csv.reader(file)
#    print("Entrei 2")
#    count = 0
#    for row in csvreader:
#        print("Entrei 3")
#        if(count==1):        
#            print("Entrei4")       
#            a = json.loads(row[0])
#            b = json.loads(row[1])
#            c = json.loads(row[2])
#            print(a)
#            print(b)
#        count = count + 1
if not entrei:
    print("Falso")
if entrei:
    print("Entrei")
    df = pd.read_csv('/workspace/Cloud-Logger/current_data.csv')
    print(df)
    print(type(df))
    st.line_chart(data = df, x="PM", y="Times")
    #st.line_chart(b)
    #st.line_chart(c)

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


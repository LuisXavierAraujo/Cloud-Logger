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
import plotly.express as px


st.graphviz_chart('''
    digraph {
        subgraph {
            microfone -> computador
        computador -> mqtt_dados [color=blue, style=dotted, shape=box]
        mqtt_dados -> gitpod [color=blue, style=dotted]
        mqtt_pedido -> computador [color=blue, style=dotted]
        gitpod -> mqtt_pedido [color=blue, style=dotted]        
        mqtt_pedido  [shape=box]
        mqtt_dados  [shape=box]
        rank = same; mqtt_pedido; mqtt_dados;
        }
    }
''')
st_autorefresh(interval=5000)  

#MQTT Thread Function
def MQTT_TH(client):   
    def on_connect(client, userdata, flags, rc):
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.        
        client.subscribe("luisaraujo/dados")
 
    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        st.session_state['plot'] = True
        data = json.loads(msg.payload)
        data = {'PM': data[0],'Times': data[1], 'STFT': data[2]}
        dataframe = pd.DataFrame(data)
        st.session_state['current_data'] = dataframe        
        print(dataframe)
    
    dataframe_final = pd.DataFrame(columns = ['PM', 'Times', 'STFT'])
    st.session_state['dataframe_final'] = dataframe_final
    st.session_state['plot'] = True
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

# Botão
if st.checkbox('iniciar gravação'):
    st.session_state.mqttClient.publish("luisaraujo/pedido", payload="start")
    if(st.session_state['plot']):
        df = st.session_state['current_data']
        print(df)
        #rms energy
        st.line_chart(data = df, x="Times", y="PM")
        pm = df['PM'].tolist()
        times = df['Times'].tolist()

        st.markdown("### First Chart")
        fig = px.density_heatmap(
            data_frame=df, y="STFT", x="Times"
        )
        st.write(fig)
        stft = df['STFT'].tolist()

        dataframe_final = st.session_state['dataframe_final']
        dataframe_final = dataframe_final.append({'PM' : pm, 'Times' : times, 'STFT': stft}, ignore_index = True)
        st.session_state['dataframe_final'] = dataframe_final

        

else:
     st.session_state['plot'] = False



## Guardar os dados
dataframe_final = st.session_state['dataframe_final']
csv = dataframe_final.to_csv().encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='data.csv',
    mime='text/csv',
)


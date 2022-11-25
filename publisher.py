# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 16:56:58 2022

@author: luise
"""

import paho.mqtt.client as mqtt



client = mqtt.Client()
#client.on_connect = on_connect
client.connect("test.mosquito.org", 1883, 60)
client.publish("luisaraujo", "on")

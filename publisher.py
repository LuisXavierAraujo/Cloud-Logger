import paho.mqtt.client as mqtt

client = mqtt.Client()
#client.on_connect = on_connect
client.connect("mqtt.eclipseprojects.io", 1883, 60)
a = [[0.005,0.003,0.002],[2,3,1]]
a_bytearray = str(a)
client.publish("luisaraujo", a_bytearray)
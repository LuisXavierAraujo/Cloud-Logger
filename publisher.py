import paho.mqtt.client as mqtt

client = mqtt.Client()
#client.on_connect = on_connect
client.connect("mqtt.eclipseprojects.io", 1883, 60)
a = [5,3,2]
a_bytearray = bytearray(a)
client.publish("luisaraujo", a_bytearray)
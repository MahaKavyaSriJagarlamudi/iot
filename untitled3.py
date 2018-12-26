import sys
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import time 
sleep = 15 

channelID = "607718"
apiKey = "4UHMFVDK2A6B06J9" 
sensor=Adafruit_DHT.DHT11

gpio=17
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  
count = 1

def on_log(client, userdata, level, buf):
	print "log : ", buf
	
def on_connect(client, userdata, flags, rc):
	if rc==0:
		print "connection OK "
	else:
		print " not connected "
#def on_disconnect(client, userdata, rc):
#	print " disconnected "
def on_publish(client, userdata, mid):
	print " publish call back ", mid
	#print " Time after acknkowledment   :  ", time.ctime()

#def on_message(client, userdata, message):
    #time.sleep(10)
 #   print("received message =",str(message.payload.decode("utf-8")))
	#topic = msg.topic
	#m_decode = str(msg.payload.decode("utf-8") 
	#print " message received : ", m_decode
    #if msg.retrain==1:
		#print " this is a retrained message "
		
client = mqtt.Client("MQTT APPLICATION")
client.on_log=on_log
client.on_connect=on_connect
#client.on_disconnect=on_disconnect
client.on_publish=on_publish
#client.on_message=on_message

client.connect("mqtt.thingspeak.com", 1883, 60)

print " connecting to broker "
client.loop_start()
#print "                     "
client.subscribe("channels/%s/publish/%s" % (channelID,apiKey))

#topic = "channels/" + channelID + "/publish/" + apiKey
def thermometer():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f} C  Humidity={1:0.1f} %'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        
        #client.connect("mqtt.thingspeak.com", 1883, 60)
        #print " connecting to broker "
        #print " Time before data send :  ", time.ctime()
        #start = time.time()
        #client.loop_start()
        
        #client.subscribe("channels/%s/publish/%s" % (channelID,apiKey))
        print " Time befor publishing  :  ", time.ctime()
        #client.loop_start()
        start = time.time()
        client.publish("channels/%s/publish/%s" % (channelID,apiKey), "field1=" + str(temperature) + "&field2=" + str(humidity))
        end = time.time()
        client.loop_stop()
        print " Time after publishing  :  ", time.ctime()
        t = end - start
        print " Time taken for publishing data to broker:  ", t
        #client.loop_stop()
        #print " Time after acknowledgment   :  ", time.ctime() 
        #t = end - start
        #print " Time required to send data  :  ", t
        
        break
if __name__ == "__main__":
        while True:
			    thermometer()
			    time.sleep(sleep)
			    count += 1
			    print "-------------------------------------------------"
			    print count, "time"
                
                

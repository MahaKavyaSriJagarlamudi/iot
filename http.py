import sys
import httplib, urllib
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
#from random import randint 
sleep = 15 # how many seconds to sleep between posts to the channel
key = '7HHNXWAB0M33KNC9' 
sensor=Adafruit_DHT.DHT11
gpio=17
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)  
count = 1
def readings():
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f} C  Humidity={1:0.1f} %'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
        params = urllib.urlencode({'field1': temperature , 'field2': humidity , 'key':key}) 
        #params2 = urllib.urlencode({'field3' : t , 'key' : key})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        #headers2 = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        print " Time after connection establishment :  ", time.ctime()
        start = time.time()
        #print " start ", start
        try:
			conn.request("POST", "/update", params, headers)
			response = conn.getresponse()
			end = time.time()
			print " Time after response  :  ", time.ctime()
			print " Response  :    ", response.status, response.reason
			t = end - start
			print " Time taken for sending data and to get response  :" , t
			#data = response.read()
        except:
            print "connection failed"
        break
if __name__ == "__main__":
	while True:
		readings()
		time.sleep(sleep)
		count += 1
		print "-------------------------------------------------"
		print count, "time" 
                

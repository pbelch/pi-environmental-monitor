
#Load system defined functions
import sys
import time
import datetime
import Adafruit_DHT
import os
import RPi.GPIO as io
import smbus
import decimal

#Set pi numbering convention
io.setmode(io.BCM)

####### Define sensors we are using #############
#Digital humidity and thermometer sensor
DHT_TYPE = Adafruit_DHT.DHT11
DHT_PIN  = 4

#Motion detector
pir_pin = 18
io.setup(pir_pin, io.IN)   

#LUX sensor
addr = 0x23
bus = smbus.SMBus(1)

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 05

#Everything within this loop re-runs every FREQUENCY_SECONDS
while True:

	####### Get data from each device #######
	
	#Clear the console screen before refresh
	os.system('cls' if os.name == 'nt' else 'clear')
	
	#LUX sensor
	data = bus.read_i2c_block_data(addr,0x11)
	lux2 = str((data[1] + (256 * data[0])) / 1.2)
	lux = decimal.Decimal(lux2).quantize(decimal.Decimal('.01'), rounding=decimal.ROUND_UP)
	#Store LUX reading in variable (String for display and INT for numerical comparison)
	outluxeval = int(lux)
	outlux = str(lux)	
	

	# Humid and temp sensor reading.
	humidity, temp = Adafruit_DHT.read(DHT_TYPE, DHT_PIN)
	#Pause if unable to connect to sensor - Prevents app crashing
	if humidity is None or temp is None:
		print 'Loading data.. please wait'
		time.sleep(2)
		continue
	
	####### Build screen and gather inputs from sensors #######
	

	#Get Current DateTime
	now = datetime.datetime.now()
	
	#Start outputting to screen
	print '############## Raspberry Jam App ##############'
	print '#      Last Updated: {:%d-%b-%Y %H:%M:%S}     #'.format(now)
	
	#Additional loop to check if there is movement and store result
	if io.input(pir_pin):
		motionout = 'DETECTED!!!'
	else:
		motionout = 'None Detected'
	
	#Additional loop to group LUX reading and store result	
	
	if outluxeval <= 30 :
		luxout = 'Very Dark'
	if outluxeval > 30 and outluxeval <= 700:
		luxout = 'Dim'
	if outluxeval > 700 and outluxeval <= 7500:
		luxout = 'Normal'
	if outluxeval > 7500 :
		luxout = 'OUTSIDE!!!!'

		
	#Output of calculated and actual values and variables to screen
	
	print '#              Temperature: {0:0.1f} C            #'.format(temp)
	print '#              Humidity:    {0:0.1f} %            #'.format(humidity)
	print '#              Motion:  ' + str(motionout) + '        #'
	print '#              Light:  ' + str(luxout) + '(' + str(outlux) + ')        #'
	print '#                                             #'
	print '###############################################'
	print '             Press CTRL + C to Exit '             
	
	#Time before refresh. Set in variable at the top of the page
	time.sleep(FREQUENCY_SECONDS)

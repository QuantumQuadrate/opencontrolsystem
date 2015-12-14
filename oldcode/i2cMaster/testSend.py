import smbus
import time
import sys
import RPi.GPIO as GPIO
from routingTable import routing_table
#create routing table
rt = routing_table()

bus = smbus.SMBus(1)

default_address = 5
address_table = []

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)


		
def init_i2c():
	bus = smbus.SMBus(1)

def get_table():
	for x in range(0,127):
		try:
			bus.write_byte_data(x, 0x00, 111)
			time.sleep(0.05)
			address_table.append(x)
		except:
			pass
	print("Address table: ["),
	for number in address_table:
		print(str(number) + ', '),
	print("]")

def initialize():
	#Set IACK pin high and carry signal to nearest slave card
	GPIO.output(4, True);
	time.sleep(0.01);

	keep_going = True;
	while(keep_going):
		try:
			#Set IACK out high
			#read the current device hardware ID
			hardware_id = bus.read_byte(default_address)
			time.sleep(0.001)

			#Give this device a routing address
			assigned_address = rt.add_device(hardware_id)
			bus.write_byte(default_address, assigned_address)

			time.sleep(0.001)
			print("[mac:" + str(hardware_id) + ",address:" + str(assigned_address) + "]")

		except IOError:
			time.sleep(0.001)
			GPIO.output(4, False)
			keep_going = False
		except Exception, e:
			print(e)
			keep_going = False

	print("Finished building routing table")
	GPIO.cleanup()
	rt.print_routing_table()


initialize()

#get_table()
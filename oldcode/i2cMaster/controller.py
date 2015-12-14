import smbus
import time
import sys
import RPi.GPIO as GPIO
from routingTable import routing_table
import utils
util = utils.utils()

class vme_controller:
	def __init__(self):

		#Pinout can be found at: http://www.element14.com/community/servlet/JiveServlet/previewBody/73950-102-4-309126/GPIO_Pi2.png
		#Pin numbers refers to GPIO pin numbers

		print("Controller object initialized!")
		#Print status messages or not
		self.verbose = True
		
		#define max command retries
		self.max_tries = 5

		#default slave address
		self.default_address = 5

		#IACK gpio pin number
		self.iack_pin_number = 4
		
		#Reset gpio pin number
		self.reset_pin_number = 17
		
		#interupt 0 pin, maps to interupt 0 on arduino
		self.interupt_0_pin   = 5

		#interupt 1 pin, maps to interupt 1 on arduino
		self.interupt_1_pin   = 6

		#create I2C bus object on i2c port 1
		self.bus = smbus.SMBus(1)

		#create routing table object
		self.rt = routing_table()
		
		#initialize gpio
		self.init_gpio()
	
		#initialize IACK gpio line
		self.init_gpio_iack()

		#initialize reset gpio line
		self.init_gpio_reset()
		
		#initialize interupt lines
		self.init_gpio_interupts()

		#initialize routing table
		#init_routing_table()

	#initialize gpio
	def init_gpio(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)

	#initialize IACK line, must happen before address table build
	def init_gpio_iack(self):
		GPIO.setup(self.iack_pin_number, GPIO.OUT)

	#initialize interupt lines
	def init_gpio_interupts(self):
		GPIO.setup(self.interupt_0_pin, GPIO.OUT)
		GPIO.setup(self.interupt_1_pin, GPIO.OUT)

	#initialize reset line, must happen before address table build
	def init_gpio_reset(self):
		GPIO.setup(self.reset_pin_number, GPIO.OUT)

	#Go through whole address space to find devices (hot swap in future iteration?)
	def poll_table(self):
		arr = []
		for x in range(0,127):
			try:
				start = time.time()
				self.bus.write_byte_data(x, 0x00, 111)
				end   = time.time()
				print("I2C time: " + str(end-start))
				time.sleep(0.05)
				arr.append(x)
				if self.verbose:
					print("Found device at address " + str(x))
			except:
				pass
		return(arr)
	
	
	#Write block to card (wrapper)
	def write_block(self, address, block):
		#sbus library expects first byte of block then rest of the block
		self.bus.write_i2c_block_data(address,block[0],block[1:])

	#Request block from card (wrapper)
	def read_block(self, address, cmd, tries=0):
		#First byte is address, second byte is the command byte which is sent with the request
		try:
			return self.bus.read_i2c_block_data(address, cmd)
		except IOError:
			if(tries<=self.max_tries):
				time.sleep(0.001)
				print("Error reading block from card, retrying")
				self.read_block(address, cmd,(tries+1))
			else:
				print("Resent read_command " + str(self.max_tries) + " times without success")
	
	#fire interupt pin that maps to arduino 0 interupt
	def interupt_0_fire(self):
		GPIO.output(self.interupt_0_pin, True)
		time.sleep(0.001)
		GPIO.output(self.interupt_0_pin, False)

	#fire interupt pin that maps to arduino 1 interupt
	def interupt_1_fire(self):
		GPIO.output(self.interupt_1_pin, True)
		time.sleep(0.001)
		GPIO.output(self.interupt_1_pin, False)

	#Pull reset line low to reset all slave devices
	def reset_slaves(self):
		GPIO.output(self.reset_pin_number, False)
		time.sleep(0.001)
		GPIO.output(self.reset_pin_number, True)
		#given some time for reboot
		time.sleep(2)
			
	#Find and assign addresses to devices
	def init_routing_table(self):
		#reset all card on bus
		self.reset_slaves()

		#Set IACK pin high to indicate setup has started, this is carried down the line of cards
		GPIO.output(self.iack_pin_number, True);
		time.sleep(0.01);

		#boolean to track loop
		keep_going = True;

		while(keep_going):
			try:
				#read the current device hardware ID
				hardware_id = self.bus.read_byte(self.default_address)
				time.sleep(0.005)

				#Add device id to routing table and get back an assigned address
				assigned_address = self.rt.add_device(hardware_id)

				#inform device what address it was assigned
				self.bus.write_byte(self.default_address, assigned_address)

				time.sleep(0.005)
				#if self.verbose:
					#print("[mac:" + str(hardware_id) + ",address:" + str(assigned_address) + "]")
			
			#Go until no default address devices are found and error is thrown
			except IOError:
				time.sleep(0.001)
				#pull IACK low to indicate setup is done, this is carried down the line of cards
				GPIO.output(self.iack_pin_number, False)
				keep_going = False

			#If unknown error happens print it and stop
			except Exception, e:
				print(e)
				#pull IACK low to indicate setup is done
				GPIO.output(self.iack_pin_number, False)
				keep_going = False

		#Check if there are no devices found
		if(self.rt.number_devices() == 0):
			raise Exception("No devices connected to controller")

		#setup finished
		if self.verbose:
			print("Finished building routing table")
		#GPIO.cleanup()
		self.rt.print_routing_table()
	def num_devices(self):
		return self.rt.number_devices()
		
# test code               
if __name__ == "__main__":
	c = vme_controller()
	c.init_routing_table()
	block = ([0] + util.int_to_bytes(50) + util.int_to_bytes(200))
	print block
	c.write_block(118, block)


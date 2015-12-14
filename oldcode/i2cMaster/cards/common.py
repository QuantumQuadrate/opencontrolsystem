#This file stores things common to / required by
#all cards.


#This class stores operating level commands common to all cards.
#These commands are on demand and do not contain timing information
#like experiment level commands.
#
#Commands 0-63 (0x00-0x3F) are reserved for this purpose.
#Organization: (0-15) (0x0~) -> diagnose board (blink led, get amount of free ram, get uuid etc.)
#              (16-31)(0x1~) -> experiment stack operations (load ops, clear ops, start experiment etc.)
#              (32-47)(0x2~) -> TBD
#              (48-63)(0x3~) -> TBD  


#Current format is:
#|(operation byte)|(parameter byte 1)|(parameter byte 2)| ... (max 30 parameter bytes)
#TODO:block transfer if needed

import time
import utils
util = utils.utils()

class common_card:
	#################Define command constants######################################
	#                                                                             #
	#                                                                             #

	def __init__(self, controller, id, address):
		
		self.id      = id
		self.address = address
		self.controller = controller

		#diagnostics##############################################################################
		#Blink indicator LED (useful for finding card in rack)
		#{input:4 bytes; output:0 bytes}
		#Input : |{2 bytes}(number of blinks)|{2 bytes}(duration of blink in ms)|
		#Output: nothing
		self.instr_util_blink_led = 0x00
               	
		#Return the card's uuid
		#{input:0 bytes; output:8 bytes}
		#Input : nothing
		#Output: |{2 bytes}(card type)|{6 bytes}(Serial number)|
		self.instr_util_get_uuid  = 0x01

		#Return the amount of free ram
		#{input:0 bytes; output:2 bytes}
		#Input : nothing
		#Output: |{2 bytes}(Amount of free ram in bytes)|
		self.instr_util_free_ram  = 0x02
		
		#Benchmark communication
		#{input: (0-30) bytes; output:(0-31) bytes}
		#Input : |{1 byte}(number of bytes to send back (0-30))|{0-30}(variable length of bytes to recieve)|
		#Output: |{0-30 bytes}(variable amount of bytes to send back)|
		self.instr_util_bench_com  = 0x03

		#Digital pulse for checking timing
		#{input: (0-30) bytes; output:(0) bytes}
		#Input : |{2 bytes}(digital output pin number)|{2 bytes}(number of pulses to send)|{2 bytes}(delay between pulses)|
		#Output: nothing
		self.instr_util_check_pulses = 0x04
		
		#Experiment stack operations#############################################################

		#Run experiment stack
		#{input:1 bytes; output:0 bytes}
		#Input : |{1 byte}(Which interupt to fire on)|
		#Output: nothing
		self.instr_exp_run = 0x10

		#Run experiment stack at slower speed for debugging
		#TODO: prevent overflow, verify division is correct
		#{input:1 bytes; output:0 bytes}
		#Input : |{1 byte}(time divider)|
		#Output: nothing
		self.instr_exp_run_slow = 0x11
		
		#Load operation into experiment stack (2 byte ms time counter = 65 seconds max time)
		#
		#On the card these operations are performed and deleted to save memory.
		#These experiment operations could be loaded while the experiment is running if the 
		#card is setup to block communication during operations. If the exp_op stack can be supplied faster
		#than it is consumed and the data stack is consummed fast enough, this allows continous operation.
		#
		#{input:(10-30) bytes; output:1 byte}
		#Input : |{1 byte}(exp operation code)|{2 bytes}(start time in ms)|{2 bytes}(number of repetitions)|{2 bytes}(delay between repetitions in ms)|{0-9 bytes}(exp op args)|
		#Output: |{3 bytes}(bytes of free ram left {minus 64 to protect stack})|
		self.instr_exp_load_op = 0x12
		
		#Run exp operation on demand (2 byte ms time counter = 65 seconds max time)
		#{input:(10-30) bytes; output:(0-31) bytes}
		#Input : |{1 byte}(exp operation code)|{0-23 bytes}(exp op args)|
		#Output: |{0-31 bytes}(exp operation return values)|
		self.instr_exp_run_op = 0x13

		#Benchmark exp operation on demand, measure execution time in microseconds, excluding communication time
		#operations taking longer than 1 millisecond could cause issues with timing
		#{input:(10-30) bytes; output:2 bytes}
		#Input : |{1 byte}(exp operation code)|{0-23 bytes}(exp op args)|
		#Output: |{4 bytes}(exp operation runtime in microseconds)|
		self.instr_exp_bench_op = 0x14
		
		#Calculate checksum of experiment stack
		#{input: 0 bytes, output : 1 byte}
		#Input : nothing
		#Output: |{1 byte}(modulus checksum of all bytes in stack)|
		self.instr_exp_check = 0x15

		#Clear experiment stack
		#{input: 0 bytes, output : 0 bytes}
		#Input : nothing
		#Output: nothing
		self.instr_exp_clear = 0x16

		#Get row of experiment data off data stack
		#
		#On the card, the data block is deleted after being sent to conserve memory.
		#This data can be retrieved while the experiment is running if the 
		#card is setup to block communication during operations. If the exp_op stack can be supplied faster
		#than it is consumed and the data stack is consumed faster then the card produces data, this allows continous experiment operation.
		#
		#{input: 0 bytes, output : 0 bytes}
		#Input : nothing
		#Output: |{1 byte}(stack empty indicator: 0x01->data, 0x00-> empty)|{1 byte}(exp level function code that this data came from)|{0-2 bytes}(time stamp of data)|{0-16 bytes}(data)|
		self.instr_exp_get = 0x17
	
	#                                                                             #
	#                                                                             #
	#################Define command constants######################################
	



	#################Define utility functions based on definitions above###########
	#                                                                             #
	#                                                                             #
	
	#Blink led variable number of times to 
	def util_blink_led(self,number_of_blinks,duration_of_blink):
		block = ([self.instr_util_blink_led] + util.int_to_bytes(number_of_blinks) + util.int_to_bytes(duration_of_blink))
		self.controller.write_block(self.address,block);

	#Get the uuid of the card
	def util_get_uuid(self):
		return self.controller.read_block(self.address, self.instr_util_get_uuid)[0:8]
	
	#Get the amount of free ram in the card in bytes
	def util_free_ram(self):
		message_block = self.controller.read_block(self.address, self.instr_util_free_ram)
		bytes = message_block[0:2]
		return util.bytes_to_unsigned_int(bytes)
		
	#Send timed pulses to specific pin to test clock drift etc.
	def util_check_pulses(self,pin_number, number_of_pulses,duration_of_pulse):
		block = ([self.instr_util_check_pulses] + util.int_to_bytes(pin_number) + util.int_to_bytes(number_of_pulses) + util.int_to_bytes(duration_of_pulse))
		self.controller.write_block(self.address,block);
	
	
	#                                                                             #
	#                                                                             #		
	#################Define utility functions based on definition above############
	



	#######Define standard experiment functions based on definitions above#########
	#                                                                             #
	#                                                                             #

	#Load experiment operation into card memory
	def exp_load_op(self, operation):
		block = ([self.instr_exp_load_op] + operation)
		self.controller.write_block(self.address,block)

	#Place card into experiment mode
	#Once in this mode, the card will wait for an interupt to start executing intructions
	def exp_run(self):
		block = [self.instr_exp_run]
		self.controller.write_block(self.address,block)

	#Requests one datapoint off the card data stack
	def exp_get(self):
		message_block = self.controller.read_block(self.address, self.instr_exp_get)
		return message_block[0:9]

	#Get all data from card
	def exp_get_all_data(self):
		got_all_data = False
		all_data     = []
		#poll data array until empty
		while(not got_all_data):
			time.sleep(0.01)
			block = self.exp_get()
			#0x00 indicates data array is empty
			if(block[0] == 0x00):
				got_all_data = True
			else:
				all_data.append(block)
		return all_data		
	#                                                                             #
	#                                                                             #
	#######Define standard experiment functions based on definitions above#########


	
				

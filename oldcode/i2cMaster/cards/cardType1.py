import smbus
import time
import sys
from commons import commands


#This class is the controller side software model 
#of a unique type of card containing methods to
#setup and run experiments on the card.

#Common functions and methods among different
#card classes might be moved to a default card class that
#gets extended by unique card classes to better organize
#the code.


class card_type_1:
	#instantiate card object
	def __init__(self, i2c_bus, uuid, i2c_address):
		#Pass bus object in by reference
		#TODO is the pythonic way to do this?
		self.i2c_bus = i2c_bus
		#Set card's uuid
		self.uuid = uuid
		#Set card's i2c address
		self.i2c_address
		#get list of common commands
		self.cmds = commands
	
	#get the amount of free ram
	def free_ram(self):
		block = [commands.]


	#Write block to card
	def write_block(self, block):
		self.i2c_bus.write_i2c_block_data(self.i2c_address, 0x00, block)
	
	#Request block from card (wrapper)
	def read_block(self):
		return self.i2c_bus.read_i2c_block_data(self.i2c_address, 111)
		
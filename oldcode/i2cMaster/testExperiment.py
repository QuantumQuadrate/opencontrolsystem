import cards.common
import controller
import time
import utils


import matplotlib.pyplot as plt


util = utils.utils()

#Initialize controller object
control = controller.vme_controller()
control.init_routing_table()

#initialize cards
my_card1 = cards.common.common_card(control, 55, 118)
#my_card2 = cards.common.common_card(control, 55, 117)

#print my_card1.util_free_ram()
time.sleep(1)
#Run experiment

op1 = ([0x00] + util.int_to_bytes(0) + util.int_to_bytes(64) + util.int_to_bytes(1) + util.int_to_bytes(1))
op2 = ([0xff])


my_card1.exp_load_op(op1)
time.sleep(0.1)
my_card1.exp_load_op(op2)
time.sleep(0.1)

my_card1.exp_run()
time.sleep(0.1)
control.interupt_0_fire()

time.sleep(2)

#poll data off card
time_array = []
voltage_array = []
got_all_data = False

while(not got_all_data):
	block = my_card1.exp_get()
	if(block[0] == 0x00):
		got_all_data = True
	else:
		#time.sleep(0.1)
		#print block
		int_time  = util.bytes_to_unsigned_int(block, 2)
		int_voltage = util.bytes_to_unsigned_int(block, 4)
		voltage     = (float(int_voltage)/1024)*5
		
		time_array  = time_array + [int_time]
		voltage_array = voltage_array + [voltage]	
		#print("Time: " + str(int_time) + "ms after exp start interupt, Voltage: " + str(voltage))




plt.plot(time_array, voltage_array)
plt.xlabel('Time in ms')
plt.ylabel('Voltage')
plt.show()





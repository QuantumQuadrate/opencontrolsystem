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
my_card1 = cards.common.common_card(control, 33, 118)
my_card2 = cards.common.common_card(control, 55, 117)

#print my_card1.util_free_ram()
time.sleep(1)
#Run experiment


for x in range(0,4):
	op = ([0x00] + util.int_to_bytes(x*32*4) + util.int_to_bytes(32) + util.int_to_bytes(4) + util.int_to_bytes(x))
	my_card1.exp_load_op(op)

op_end = ([0xff])
my_card1.exp_load_op(op_end)



for x in range(0,4):
	op = ([0x00] + util.int_to_bytes(x*32*4 + 2) + util.int_to_bytes(32) + util.int_to_bytes(4) + util.int_to_bytes(x))
	my_card2.exp_load_op(op)

op_end = ([0xff])
my_card2.exp_load_op(op_end)



my_card1.exp_run()
my_card2.exp_run()
time.sleep(0.1)
control.interupt_0_fire()

time.sleep(2)

#poll data off card


all_data1 = my_card1.exp_get_all_data()
all_data2 = my_card2.exp_get_all_data()

time_array = []
voltage_array = []

for block in all_data1:
	int_time  = util.bytes_to_unsigned_int(block, 2)
	int_voltage = util.bytes_to_unsigned_int(block, 4)
	voltage     = (float(int_voltage)/1024)*5
		
	time_array  = time_array + [int_time]
	voltage_array = voltage_array + [voltage]	
	#print("Time: " + str(int_time) + "ms after exp start interupt, Voltage: " + str(voltage))


for block in all_data2:
	int_time  = util.bytes_to_unsigned_int(block, 2)
	int_voltage = util.bytes_to_unsigned_int(block, 4)
	voltage     = (float(int_voltage)/1024)*5
		
	time_array  = time_array + [int_time]
	voltage_array = voltage_array + [voltage]	
	#print("Time: " + str(int_time) + "ms after exp start interupt, Voltage: " + str(voltage))


time2 = []
volt2 = []

for x in range(0, 128):
	time2 = time2 + [time_array[x]]
	volt2 = volt2 + [voltage_array[x]]
	
	time2 = time2 + [time_array[x+128]]
	volt2 = volt2 + [voltage_array[x+128]]	

plt.plot(time2, volt2)
plt.xlabel('Time in ms')
plt.ylabel('Voltage')
plt.show()





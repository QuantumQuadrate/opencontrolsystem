#reads the header file
def read_file(file_name):
	f =  open(file_name, 'r')
	defs = f.read()
	f.close()
	return defs

#parses the header file
#returns a dictionary of opcode -> hex value 
def parse(file_name):
	defs_string = read_file(file_name)
	lines = defs_string.split('\n')
	dictionary = dict()
	for line in lines:
		if(line):
			parsed = line.split(' ')
			if(parsed):
				if(len(parsed)>=3):
					if(parsed[0] == '#define'):
						opcode = parsed[1]
						value  = parsed[2]
						dictionary[opcode] = value
					else:
						print('Opcode definition header file had a line that was not a "#define", skipping over')
				else:
					print("Opcode definition header file had a line that had less than 2 space chars, skipping over")
			else:
				print("Opcode definition header file had a line that was blank, skipping over")
	print('found ' + str(len(dictionary)) + ' instructions in the header file')
	return dictionary

#test
print(parse('op_defs.h')['OP_3'])


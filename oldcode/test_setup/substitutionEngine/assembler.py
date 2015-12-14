import string

def get_main():
	f =  open('partials/main.part', 'r')
	main = f.read()
	f.close()
	return main

def get_card_methods():
	f =  open('partials/cardmethods.part', 'r')
	methods = f.read()
	f.close()
	return methods

def write_complete(main):
	f = open('complete/main.ino', 'w+')
	f.write(main)
	f.close()


def assemble():
	main = get_main()
	cardmethods = get_card_methods()
	main = main.replace('//<cardmethods>', cardmethods )
	write_complete(main)

assemble()
import os

def get_ip():
	conf = ''
	os.system("hostname -I > hostconfig.txt")
	with open("hostconfig.txt","r") as f:
		 conf += f.read()
	conf = conf.split()
	
	return conf[0]

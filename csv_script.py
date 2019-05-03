#Author: Ata Aygen - 29/04/2019
#Refer to CSV template for device type variables


from netmiko import Netmiko
from getpass import getpass
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException, AuthenticationException, NoValidConnectionsError
import csv
import logging
import time
import datetime
import progressbar

def operation(command, device):
	if command == "config":
			if device["device_type"] == "cisco_ios" or device["device_type"] == "cisco_asa":
				return "sh run"
			if device["device_type"] == "juniper":
				return "show configuration | display set"
	if command == "version":
			return "show version"


bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)   


# logging.basicConfig(filename='test.log', level=logging.DEBUG)
# logger = logging.getLogger("netmiko")
	
username = input("Username: ")
password = getpass()

ip_input = input("Enter CSV file name containing IP's (default.csv): ")


runcommand = input("Enter the operation to be done(config, sh ver etc.): ")

ip_list = []


with open(ip_input) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		ip_list.append([row[0],row[1]])
		
bar = progressbar.ProgressBar(max_value=len(ip_list)) 
bar.start()

device_list = []
# print(ip_list)
for device in ip_list:
	device = {"host": device[0],"username": username,"password": password,"device_type": device[1],"secret": password,}
	device_list.append(device)
	

for device in device_list:
	try:
		net_connect = Netmiko(**device)
		net_connect.enable()
		hostname = net_connect.find_prompt()
		hostname = hostname[:-1]
		print(net_connect.find_prompt())
		
		command = operation(runcommand,device)
		
		out = open(hostname + ".txt", "w+")
		
				
		output = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n" + hostname + "\n" + net_connect.send_command(command)
		
		net_connect.disconnect()
		out.write(output)
		out.close()
		print("Config for " + hostname + " saved \n")
		print()
		#net_connect.send_command("exit")
		bar.update(bar.value + 1)
	except (NetMikoTimeoutException, SSHException, ConnectionRefusedError) as err:
		print(err)
		bar.update(bar.value + 1)
		print("\n")
		
	except ValueError as e:
		print(e)
		bar.update(bar.value + 1)
		print("\n")

	except AuthenticationException:
		print("Authentication failed for " + device.host)
		bar.update(bar.value + 1)
		print("\n")
	
bar.finish()
# netscript
A basic Python script to run various commands on network devices


Dependencies:

Netmiko
progressbar2


Working features:

Grabbing running configuration from Cisco IOS, ASA and JunOS devices
Grabbing "show version" output from Cisco IOS, ASA and JunOS devices
Running any "show" command if the input contains only a single device type

CSV format:

IP addresses in the first column, device type in the second.
Device type variables: cisco_ios, cisco_asa, juniper, hp_procurve
Template included in repo

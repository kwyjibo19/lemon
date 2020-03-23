#!/usr/bin/env python3 

import getpass
import telnetlib

import jinja2
import os

template_file = "cfgen.j2"
csv_parameter_file = "cfgen.csv"
config_parameters = []
output_directory = "_output"

print("!!!!!READING CSV!!!!!")
f = open(csv_parameter_file)
csv_content = f.read()
f.close()

print("!!!!!CONVERTING CSV!!!!!")
csv_lines = csv_content.splitlines()
headers = csv_lines[0].split(";")
for i in range(1, len(csv_lines)):
    values = csv_lines[i].split(";")
    parameter_dict = dict()
    for h in range(0, len(headers)):
        parameter_dict[headers[h]] = values[h]
    config_parameters.append(parameter_dict)
    #print(csv_lines)

print("!!!!!CREATING J2 ENV!!!!!")
env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath="."))
template = env.get_template(template_file)

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

print("!!!!CREATING TEMPLATES!!!!!")
for parameter in config_parameters:
    result = template.render(parameter)
    f = open(os.path.join(output_directory, parameter['hostname'] + ".config"), "w")
    f.write(result)
    print("!!!!!CONFIGURATION '%s' CREATED!!!!!" % (parameter['hostname'] + ".config"))

    HOST = "99.99.99.1"
    user = input("Enter your telnet username: ")
    password = getpass.getpass()

    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
         tn.read_until(b"Password: ")
         tn.write(password.encode('ascii') + b"\n")
    tn.write(b"conf t\n")
    tn.write(result)
    print(result)
         tn.write(b"end\n")
    print("!!!!!DEVICE '%s' CONFIGURED!!!!!" % (parameter['hostname']))
    f.close()
print("!!!!!DONE!!!!!")

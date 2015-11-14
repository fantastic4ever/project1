from flask import Flask, request, jsonify
from pymongo import MongoClient
import urllib2, json, requests
import sys, subprocess
import os, signal, time
import student_settings as ss
import student_flask as sf
import json

app = Flask(__name__)
eve_url = ''
global eve_process
global args
mongo_url = 'mongodb://admin:admin@ds039684.mongolab.com:39684/project1'
with open('student_config.txt') as data_file:    
    my_settings = json.load(data_file)

#Just redirect GET request to eve service
@app.route("/private/student/<uni>", methods=['GET'])
def get_student(uni):
	response = requests.get(eve_url + uni)
	return response.content

#Just redirect POST request to eve service 
@app.route("/private/student", methods=['POST'])
def add_student():
	response = requests.post(eve_url, data=request.get_json())
	return response.content

#Get student id and etag first. Then delete student and all registration information
@app.route("/private/student/<uni>", methods=['DELETE'])
def delete_student(uni):
	#Get student information
	response = requests.get(eve_url + uni)
	student_info = response.json()
	if response.status_code > 206:    #Fail to get student information by uni
		return response.content
	#Get registration status from MongoDB instance_info collection. If registration service is not running, return
	client = MongoClient(mongo_url)
	regis_info = client.project1.instance_info.find({'instanceType' : 'registration'})
	if(regis_info.count() == 0):
		return 'Error : Registartion service is not running'
	registration_url = 'http://' + regis_info[0]['host'] + ':' + regis_info[0]['port'] + '/private/registration/uni/'
	client.close()
	#Send DELETE request to eve service to delete student
	response = requests.delete(eve_url + student_info['_id'], headers={"If-Match" : student_info['_etag']})
	if response.status_code > 206:    #Failed to delete student information
		return response.content
	#Send DELETE request to registration service
	response2 = requests.delete(registration_url + uni)
	return response.content + '\n\n' + response2.content

#Get student id and etag first. Then update it. 
@app.route("/private/student/<uni>", methods=['PATCH'])
def update_student(uni):
	#Get student information
	response = requests.get(eve_url + uni)
	student_info = response.json()
	print request.get_json()
	if response.status_code > 206:    #Fail to get student information by uni
		return response.content
	#Send PATCH request to eve service to update student information
	response = requests.patch(eve_url + student_info['_id'], data=request.get_json(), headers={"If-Match" : student_info['_etag']})
	return response.content

#Get student schema
@app.route("/private/student/schema", methods=["GET"])
def get_student_schema():
	return 	jsonify(my_settings['DOMAIN']['student']['schema'])

#Delete an attribute in student schema 
@app.route("/private/student/schema/<attribute>", methods=['DELETE'])
def delete_student_schema(attribute):
	#check if attribute is in student schema
	if attribute in my_settings['DOMAIN']['student']['schema']:
		del my_settings['DOMAIN']['student']['schema'][attribute]
		with open('student_config.txt', 'w') as outfile:
			json.dump(my_settings, outfile)
		#restart eve service to load new schema settings
		stop_eve_process()
		time.sleep(0.1)
		start_eve_process()
		return "Successfully delete attribute '" + attribute + "'"
	else:
		return "Failed to delete attribute: '" + attribute + "' is not in student schema" 

#Add an attribute in student schema
@app.route("/private/student/schema/<attribute>", methods=['POST'])
def add_student_schema(attribute):
	attribute_value=request.get_json()
	#validate attribute_value
	#if attribute_value is valid, then add attribute to schema
	my_settings['DOMAIN']['student']['schema'][attribute] = attribute_value
	with open('student_config.txt', 'w') as outfile:
		json.dump(my_settings, outfile)
	#restart eve service to load new schema settings
	stop_eve_process()
	time.sleep(0.1)
	start_eve_process()
	return "success!"

def stop_eve_process():
	print "stopping student eve process..."
	os.kill(sf.eve_process.pid, signal.SIGTERM)

def start_eve_process():
	print "starting student eve process..."
	sf.eve_process = subprocess.Popen(args)

if __name__ == "__main__":
	if(len(sys.argv) >= 3):
		#sys.argv[1] is host address. sys.argv[2] is port number
		host = sys.argv[1]
		#I set eve service runs on different port. If current flask runs on 5000 port, eve runs on 15000 port
		eve_port = str((int(sys.argv[2]) + 10000))
		eve_url = 'http://' + host + ':' + eve_port + '/student/'
		args = ['python', 'student_eve.py', host, eve_port]
		#run eve service as subprocess in background
		start_eve_process()
		app.run(host=host, port=int(sys.argv[2]))

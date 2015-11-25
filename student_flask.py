from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
import urllib2, json, requests
import sys, subprocess
import os, signal, time
import student_flask as sf
import json
import logging
import util
from util import mongo_url

app = Flask(__name__)
eve_url = ''
global eve_process
global args
student_num = 'student'
student_schema = util.get_eve_schema('student')
logging.basicConfig(filename="student.log",
                    level=logging.INFO, format='%(asctime)s --- %(message)s')


#Get all student information
@app.route("/private/student", methods=['GET'])
def get_all_student():
	response = requests.get(eve_url)
	return Response(response.content, mimetype='application/json', status=response.status_code)

#Get student information by uni. Flask just redirect GET request to eve service
@app.route("/private/student/<uni>", methods=['GET'])
def get_student(uni):
	response = requests.get(eve_url + uni)
	return Response(response.content, mimetype='application/json', status=response.status_code)

#Add student information. Flask just redirect POST request to eve service 
@app.route("/private/student", methods=['POST'])
def add_student():
	logging.info(student_num + " service: receive a creating student request")
	logging.info(request.get_json())
	response = requests.post(eve_url, data=request.get_json())
	return Response(response.content, mimetype='application/json', status=response.status_code)

#Get student id and etag first. Then delete student and all registration information
@app.route("/private/student/<uni>", methods=['DELETE'])
def delete_student(uni):
	#Get student information
	response = requests.get(eve_url + uni)
	student_info = response.json()
	if response.status_code > 206:    #Fail to get student information by uni
		return Response(response.content, mimetype='application/json', status=response.status_code)
	#Get registration status from MongoDB instance_info collection. If registration service is not running, return
	client = MongoClient(mongo_url)
	regis_info = client.project1.instance_info.find({'instanceType' : 'registration'})
	if regis_info.count() == 0:
		return Response(status=500)
	registration_url = 'http://' + str(regis_info[0]['host']) + ':' + str(regis_info[0]['port']) + '/private/registration/uni/'
	client.close()
	#Send DELETE request to registration service
	response2 = requests.delete(registration_url + uni)
	if response2.status_code != 404 and response2.status_code > 206:
		return Response(response2.content, mimetype='application/json', status=response2.status_code)
	#Send DELETE request to eve service to delete student
	response = requests.delete(eve_url + student_info['_id'], headers={"If-Match" : student_info['_etag']})
	return Response(response.content, mimetype='application/json', status=response.status_code)

#Get student id and etag first. Then update it. 
@app.route("/private/student/<uni>", methods=['PUT'])
def update_student(uni):
	#Get student information
	response = requests.get(eve_url + uni)
	student_info = response.json()
	print request.get_json()
	if response.status_code > 204:    #Fail to get student information by uni
		return Response(response.content, mimetype='application/json', status=response.status_code)
	#Send PATCH request to eve service to update student information
	response = requests.put(eve_url + student_info['_id'], data=request.get_json(), headers={"If-Match" : student_info['_etag']})
	return Response(response.content, mimetype='application/json', status=response.status_code)

#Get student schema
@app.route("/private/student/schema", methods=["GET"])
def get_student_schema():
	return jsonify(student_schema)

#Delete attribute(one or more) in student schema
@app.route("/private/student/schema", methods=['DELETE'])
def delete_student_schema():
	#check if attribute is in student schema
	content = request.get_json()
	count = 0
	for k in content:
		if k in student_schema.keys():
			del student_schema[k]
			count = count + 1
		else:
			print k + ' does not exists in student schema, can not delete it'
	result = util.update_eve_setting("student", student_schema)
	#restart eve service to load new schema settings
	stop_eve_process()
	time.sleep(0.1)
	start_eve_process()
	return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count)+' column(s) deleted", "code": 200}}', mimetype = 'application/json', status = 200)


#Add attributes(one or more) in student schema. If attribute is already in schema, ignore it
@app.route("/private/student/schema", methods=['POST'])
def add_student_schema():
	content = request.get_json()
	count = 0
	for k, v in content.items():
		if k in student_schema.keys():
			print k + ' already exists in student schema, can not add it'
		else:
			student_schema[k] = v
			count += 1
	# update the schema in mongodb
	result = util.update_eve_setting('student', student_schema)
	stop_eve_process()
	time.sleep(0.1)
	start_eve_process()
	return Response('{"_status": "SUCCESS", "_success": {"message": "' + str(count) + ' column(s) added", "code": 200}}', mimetype='application/json', status=200)

#Update attributes(one or more) in student schema. If attribute is not in schema, ignore it
@app.route("/private/student/schema", methods=['PUT'])
def update_student_schema():
	content = request.get_json()
	count = 0
	for k, v in content.items():
		if k in student_schema.keys():
			student_schema[k] = v
			count += 1
		else:
			print k + ' does not exists in student schema, can not update it'
	# update the schema in mongodb
	result = util.update_eve_setting('student', student_schema)
	stop_eve_process()
	time.sleep(0.1)
	start_eve_process()
	return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count)+' column(s) updated", "code": 200}}', mimetype='application/json', status=200)

#Shutdown eve service
@app.route("private/instance/student", methods=['DELETE'])
def shutdown_eve_service():
	stop_eve_process()
	return Response(status=200)

def stop_eve_process():
	print "stopping student eve process..."
	os.kill(sf.eve_process.pid, signal.SIGTERM)

def start_eve_process():
	print "starting student eve process..."
	sf.eve_process = subprocess.Popen(args)

if __name__ == "__main__":
	if(len(sys.argv) >= 4):
		#sys.argv[1] is host address. sys.argv[2] is port number. sys.argv[4] is shard number
		host = sys.argv[1]
		#I set eve service runs on different port. If current flask runs on 5000 port, eve runs on 15000 port
		eve_port = str((int(sys.argv[2]) + 10000))
		student_num = student_num + str(int(sys.argv[3]))
		eve_url = 'http://' + host + ':' + eve_port + '/' + student_num + '/'
		args = ['python', 'student_eve.py', host, eve_port, sys.argv[3]]
		#run eve service as subprocess in background
		start_eve_process()
		app.run(host=host, port=int(sys.argv[2]))

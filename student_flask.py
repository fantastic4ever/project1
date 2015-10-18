from flask import Flask, request
import urllib2, json, requests
import sys, subprocess
import os

app = Flask(__name__)
eve_url = ''

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

#Get student id and etag first. Then delete it.
@app.route("/private/student/<uni>", methods=['DELETE'])
def delete_student(uni):
	#Get student information
	response = requests.get(eve_url + uni)
	student_info = response.json()
	if response.status_code != 200:
		return response.content
	#Send DELETE request to eve service to delete student
	response = requests.delete(eve_url + student_info['_id'], headers={"If-Match" : student_info['_etag']})
	#Send DELETE request to registration service
	return response.content

#Get student id and etag first. Then update it. 
@app.route("/private/student/<uni>", methods=['PATCH'])
def update_student(uni):
	#Get student information
	response = requests.get(eve_url + uni)
	student_info = response.json()
	print request.get_json()
	if response.status_code != 200:
		return response.content
	#Send PATCH request to eve service to update student information
	response = requests.patch(eve_url + student_info['_id'], data=request.get_json(), headers={"If-Match" : student_info['_etag']})
	return response.content

if __name__ == "__main__":
	if(len(sys.argv) >= 3):
		host = sys.argv[1]
		#I set eve service runs on different port. If current flask runs on 5000 port, eve runs on 15000 port
		eve_port = str((int(sys.argv[2]) + 10000))
		eve_url = 'http://' + host + ':' + eve_port + '/student/'
		args = ['python', 'student_eve.py', host, eve_port]
		#run eve service as subprocess in background
		subprocess.Popen(args)
		app.run(host=host, port=int(sys.argv[2]))

from flask import Flask, request
import urllib2, json, requests
import sys, subprocess
import os, signal, time
from flask import jsonify
from pymongo import MongoClient
import registration_flask as rf 

global eve_process
global args

uri = 'mongodb://admin:admin@ds039684.mongolab.com:39684/project1'
client = MongoClient(uri)
db = client.get_default_database()
settings = db.settings
my_settings = settings.find_one({'name': 'registration'})
print my_settings['name']
print my_settings
app = Flask(__name__)
eve_url = ''

@app.route("/private/registration/schema", methods = ['GET'])
def search_for_registration_shema():
    return 	jsonify(my_settings['value']['DOMAIN']['registration']['schema'])

@app.route("/private/registration/schema/<attribute>", methods = ['POST'])
def add_for_registration_shema(attribute):
	attribute_value = request.get_json()
	my_settings['value']['DOMAIN']['registration']['schema'][attribute] = attribute_value
	# update the schema in mongodb
	result = db.settings.update_one({'name': 'registration'}, {'$set': {'value': my_settings['value']}})
	print result.matched_count
	#restart eve service to load new schema settings
	stop_eve_process()
	time.sleep(0.1)
	start_eve_process()
	return ("Successfully add the attribute '" + attribute + "'", 200)

@app.route("/private/registration/schema/<attribute>", methods = ['DELETE'])
def delete_for_registration_shema(attribute):
    #check if attribute is in the registration schema
	if attribute in my_settings['value']['DOMAIN']['registration']['schema']:
		del my_settings['value']['DOMAIN']['registration']['schema'][attribute]
		# update the schema in mongodb
		result = db.settings.update_one({'name': 'registration'}, {'$set': {'value': my_settings['value']}})
		print result.matched_count
		#restart eve service to load new schema settings
		stop_eve_process()
		time.sleep(0.1)
		start_eve_process()
		return ("Successfully delete the attribute '" + attribute + "'", 200)
	else:
		return ("Failed to delete the attribute: '" + attribute + "' is not in registration schema", 300) 


@app.route("/private/registration", methods = ['GET'])
def search_for_registration():
		response = requests.get(eve_url)
		registration_info = response.json()
		return response.content

@app.route("/private/registration/uni/<uni>", methods = ['GET'])
def search_registration_for_uni(uni):
		payload = {'where': 'UNI==' + uni}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		return response.content

@app.route("/private/registration/courseid/<cid>", methods = ['GET'])
def search_registration_for_cid(cid):
		payload = {'where': 'Course_ID==' + cid}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		return response.content

@app.route("/private/registration/uni/<uni>/courseid/<cid>", methods = ['GET'])
def search_registration_for_uni_cid(uni, cid):
		payload = {'where': '{"UNI":' + '"' + uni + '", "Course_ID":' + '"' + cid + '"}'}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		return response.content

@app.route("/private/registration", methods = ['POST'])
def post_registration():
		content = request.get_json(force = True)
		headers = {'content-type': 'application/json'}
		response = requests.post(eve_url, data=json.dumps(content), headers = headers)
		return response.content

@app.route("/private/registration", methods = ['DELETE'])
def delete_registration():
		response = requests.delete(eve_url)
		return response.content

@app.route("/private/registration/uni/<uni>", methods = ['DELETE'])
def delete_registration_for_uni(uni):
		payload = {'where': 'UNI==' + uni}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		print registration_info
		items = registration_info['_items']
		if items == []:
			return ('', 404)
		else:
			for item in items:
				response = requests.delete(eve_url + '/' + item['_id'], params = payload, headers = {"If-Match": item['_etag']})
			return response.content

@app.route("/private/registration/courseid/<cid>", methods = ['DELETE'])
def delete_registration_for_cid(cid):
		payload = {'where': 'Course_ID==' + cid}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		print registration_info
		items = registration_info['_items']
		if items == []:
			return ('', 404)
		else:
			for item in items:
				response = requests.delete(eve_url + '/' + item['_id'], params = payload, headers = {"If-Match": item['_etag']})
			return response.content

@app.route("/private/registration/uni/<uni>/courseid/<cid>", methods = ['GET'])
def delete_registration_for_uni_cid(uni, cid):
		payload = {'where': '{"UNI":' + '"' + uni + '", "Course_ID":' + '"' + cid + '"}'}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		print registration_info
		items = registration_info['_items']
		if items == []:
			return ('', 404)
		else:
			firstItem = items[0]
			response = requests.delete(eve_url + '/' + firstItem['_id'], params = payload, headers = {"If-Match": firstItem['_etag']})
			return response.content

@app.route("/private/registration/uni/<uni>/courseid/<cid>", methods = ['PUT'])
def update_registration_for_uni_cid(uni, cid):
		payload = {'where': '{"UNI":' + '"' + uni + '", "Course_ID":' + '"' + cid + '"}'}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		print registration_info
		items = registration_info['_items']
		if items == []:
			return ('', 404)
		else:
			firstItem = items[0]
			content = request.get_json(force=True)
			headers = {'content-type': 'application/json', 'If-Match': firstItem['_etag']}
			response = requests.put(eve_url + '/' + firstItem['_id'],  data = json.dumps(content), headers = headers)
			return response.content

def stop_eve_process():
	print "stopping registration eve process..."
	print rf.eve_process.pid
	os.kill(rf.eve_process.pid, signal.SIGTERM)

def start_eve_process():
	print "starting registration eve process..."
	rf.eve_process = subprocess.Popen(args)
	print rf.eve_process.pid

if __name__ == "__main__":
		if(len(sys.argv) >= 3):
			host = sys.argv[1]
			#I set eve service runs on different port. If current flask runs on 5000 port, eve runs on 15000 port
			eve_port = str((int(sys.argv[2]) + 10000))
			eve_url = 'http://' + host + ':' + eve_port + '/registration'
			args = ['python', 'registration_eve.py', host, eve_port]
			#run eve service as subprocess in background
			start_eve_process()
			app.run(host=host, port=int(sys.argv[2]))


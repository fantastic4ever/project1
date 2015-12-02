from flask import Flask, request
import urllib2, json, requests
import sys, subprocess
import os, signal, time
from flask import jsonify
from flask import Response
from pymongo import MongoClient
import registration_flask as rf 
import config
import logging

global eve_process
global args

logging.basicConfig(filename=config.REGISTRATION_LOG_FILENAME, 
                    level=logging.INFO, format='%(asctime)s --- %(message)s')

uri = 'mongodb://admin:admin@ds039684.mongolab.com:39684/project1'
client = MongoClient(uri)
db = client.get_default_database()
schema = db.schema
my_schema = schema.find_one({'name': 'registration'})
logging.info('flask...')
logging.info(my_schema['value'])

app = Flask(__name__)
eve_url = ''

@app.route("/private/registration/schema", methods = ['GET'])
def search_for_registration_shema():
    return 	jsonify(my_schema['value'])

@app.route("/private/registration/schema", methods = ['POST'])
def add_for_registration_shema():
	content = request.get_json()
	logging.info(content)
	count = 0
	for k, v in content.items():
		if k in my_schema['value'].keys():
			logging.info(k + ' already exists in registration schema, can not add it')
		else:
			my_schema['value'][k] = v
			count = count + 1
	# update the schema in mongodb
	result = db.schema.update_one({'name': 'registration'}, {'$set': {'value': my_schema['value']}})
	logging.info(result.matched_count)
	# restart eve service to load new schema settings
	stop_eve_process()
	time.sleep(0.1)
	start_eve_process()
	# return Response('{"_status": "SUCCESS", "_success": {"message": "Successfully add an attribute ", "code": 200}}', mimetype = 'application/json', status = 200)
	return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count)+' column(s) added", "code": 200}}', mimetype='application/json', status=200)

@app.route("/private/registration/schema", methods = ['PUT'])
def update_for_registration_shema():
	content = request.get_json()
	logging.info(content)
	count = 0
	for k, v in content.items():
		if k in my_schema['value'].keys():
			my_schema['value'][k] = v
			count = count + 1
		else:
			logging.info(k + ' does not exists in registration schema, can not update it')
	# update the schema in mongodb
	result = db.schema.update_one({'name': 'registration'}, {'$set': {'value': my_schema['value']}})
	logging.info(result.matched_count)
	# restart eve service to load new schema settings
	stop_eve_process()
	time.sleep(0.1)
	start_eve_process()
	# return Response('{"_status": "SUCCESS", "_success": {"message": "Successfully add an attribute ", "code": 200}}', mimetype = 'application/json', status = 200)
	return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count)+' column(s) updated", "code": 200}}', mimetype='application/json', status=200)

# @app.route("/private/registration/schema/<attribute>", methods = ['POST'])
# def add_for_registration_shema(attribute):
# 	attribute_value = request.get_json()
# 	my_schema['value'][attribute] = attribute_value
# 	# update the schema in mongodb
# 	result = db.settings.update_one({'name': 'registration'}, {'$set': {'value': my_schema['value']}})
# 	logging.info(result.matched_count)
# 	#restart eve service to load new schema settings
# 	stop_eve_process()
# 	time.sleep(0.1)
# 	start_eve_process()
# 	return Response('{"_status": "SUCCESS", "_success": {"message": "Successfully add an attribute ", "code": 200}}', mimetype = 'application/json', status = 200)

@app.route("/private/registration/schema", methods = ['DELETE'])
def delete_for_registration_shema():
	content = request.get_json()
	logging.info(type(content))
	logging.info(content)
	count = 0
	for k in content:
		logging.info(k)
		if k in my_schema['value'].keys():
			del my_schema['value'][k]
			# update the schema in mongodb
			count = count + 1
		else:
			logging.info(k + ' does not exists in registration schema, can not delete it')
	result = db.schema.update_one({'name': 'registration'}, {'$set': {'value': my_schema['value']}})
	logging.info(result.matched_count)
	# restart eve service to load new schema settings
	stop_eve_process()
	time.sleep(0.1)
	start_eve_process()
	return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count)+' column(s) deleted", "code": 200}}', mimetype = 'application/json', status = 200)

# @app.route("/private/registration/schema/<attribute>", methods = ['DELETE'])
# def delete_for_registration_shema(attribute):
#     #check if attribute is in the registration schema
# 	if attribute in my_schema['value']:
# 		del my_schema['value'][attribute]
# 		# update the schema in mongodb
# 		result = db.settings.update_one({'name': 'registration'}, {'$set': {'value': my_schema['value']}})
# 		logging.info(result.matched_count)
# 		#restart eve service to load new schema settings
# 		stop_eve_process()
# 		time.sleep(0.1)
# 		start_eve_process()
# 		return Response('{"_status": "SUCCESS", "_success": {"message": "Successfully delete an attribute ", "code": 200}}', mimetype = 'application/json', status = 200)
# 	else:
# 		return Response('{"_status": "ERR", "_error": {"message": "Failed to delete the attribute. The attribute is not in the schema.", "code": 500}}', mimetype = 'application/json', status = 300)

@app.route("/private/registration", methods = ['GET'])
def search_for_registration():
		response = requests.get(eve_url)
		registration_info = response.json()
		return Response(response.content, mimetype='application/json', status=200)

@app.route("/private/registration/uni/<uni>", methods = ['GET'])
def search_registration_for_uni(uni):
		payload = {'where': 'UNI==' + uni}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		logging.info(registration_info)
		items = registration_info['_items']
		if items == []:
			return Response('{"_status": "ERR", "_error": {"message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.", "code": 404}}', mimetype='application/json', status=404)
		return Response(response.content, mimetype='application/json', status=200)

@app.route("/private/registration/courseid/<cid>", methods = ['GET'])
def search_registration_for_cid(cid):
		payload = {'where': 'Course_ID==' + cid}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		items = registration_info['_items']
		if items == []:
			return Response('{"_status": "ERR", "_error": {"message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.", "code": 404}}', mimetype='application/json', status=404)
		return Response(response.content, mimetype='application/json', status=200)

@app.route("/private/registration/uni/<uni>/courseid/<cid>", methods = ['GET'])
def search_registration_for_uni_cid(uni, cid):
		payload = {'where': '{"UNI":' + '"' + uni + '", "Course_ID":' + '"' + cid + '"}'}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		return Response(response.content, mimetype='application/json', status=200)

@app.route("/private/registration", methods = ['POST'])
def post_registration():
		content = request.get_json(force = True)
		headers = {'content-type': 'application/json'}
		response = requests.post(eve_url, data=json.dumps(content), headers = headers)
		return Response(response.content, mimetype='application/json', status=200)

@app.route("/private/registration", methods = ['DELETE'])
def delete_registration():
		response = requests.delete(eve_url)
		#return Response(response.content, mimetype='application/json', status=200)
		return Response('{"_status": "SUCCESS", "_success": {"message": "delete succesfully", "code": 200}}', mimetype = 'application/json', status = 200)


@app.route("/private/registration/uni/<uni>", methods = ['DELETE'])
def delete_registration_for_uni(uni):
		payload = {'where': 'UNI==' + uni}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		logging.info(registration_info)
		items = registration_info['_items']
		if items == []:
			return Response('{"_status": "ERR", "_error": {"message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.", "code": 404}}', mimetype='application/json', status=404)
		else:
			for item in items:
				response = requests.delete(eve_url + '/' + item['_id'], params = payload, headers = {"If-Match": item['_etag']})
			#return Response(response.content, mimetype='application/json', status=200)
			return Response('{"_status": "SUCCESS", "_success": {"message": "delete succesfully", "code": 200}}', mimetype = 'application/json', status = 200)


@app.route("/private/registration/courseid/<cid>", methods = ['DELETE'])
def delete_registration_for_cid(cid):
		payload = {'where': 'Course_ID==' + cid}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		logging.info(registration_info)
		items = registration_info['_items']
		if items == []:
			return Response('{"_status": "ERR", "_error": {"message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.", "code": 404}}', mimetype='application/json', status=404)
		else:
			for item in items:
				response = requests.delete(eve_url + '/' + item['_id'], params = payload, headers = {"If-Match": item['_etag']})
			#return Response(response.content, mimetype='application/json', status=200)
			return Response('{"_status": "SUCCESS", "_success": {"message": "delete succesfully", "code": 200}}', mimetype = 'application/json', status = 200)


@app.route("/private/registration/uni/<uni>/courseid/<cid>", methods = ['DELETE'])
def delete_registration_for_uni_cid(uni, cid):
		payload = {'where': '{"UNI":' + '"' + uni + '", "Course_ID":' + '"' + cid + '"}'}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		logging.info(registration_info)
		items = registration_info['_items']
		if items == []:
			return Response('{"_status": "ERR", "_error": {"message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.", "code": 404}}', mimetype='application/json', status=404)
		else:
			firstItem = items[0]
			response = requests.delete(eve_url + '/' + firstItem['_id'], params = payload, headers = {"If-Match": firstItem['_etag']})
			#return Response(response.content, mimetype='application/json', status=200)
			return Response('{"_status": "SUCCESS", "_success": {"message": "delete succesfully", "code": 200}}', mimetype = 'application/json', status = 200)


@app.route("/private/registration/uni/<uni>/courseid/<cid>", methods = ['PUT'])
def update_registration_for_uni_cid(uni, cid):
		payload = {'where': '{"UNI":' + '"' + uni + '", "Course_ID":' + '"' + cid + '"}'}
		response = requests.get(eve_url, params = payload)
		registration_info = response.json()
		logging.info(registration_info)
		items = registration_info['_items']
		if items == []:
			return Response('{"_status": "ERR", "_error": {"message": "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.", "code": 404}}', mimetype='application/json', status=404)
		else:
			firstItem = items[0]
			content = request.get_json(force=True)
			headers = {'content-type': 'application/json', 'If-Match': firstItem['_etag']}
			response = requests.put(eve_url + '/' + firstItem['_id'],  data = json.dumps(content), headers = headers)
			return Response(response.content, mimetype='application/json', status=200)

def stop_eve_process():
	logging.info("stopping registration eve process...")
	logging.info(rf.eve_process.pid)
	os.kill(rf.eve_process.pid, signal.SIGTERM)

def start_eve_process():
	logging.info("starting registration eve process...")
	rf.eve_process = subprocess.Popen(args)
	logging.info(rf.eve_process.pid)

if __name__ == "__main__":
		if(len(sys.argv) >= 3):
			host = sys.argv[1]
			# I set eve service runs on different port. If current flask runs on 5000 port, eve runs on 15000 port
			eve_port = str((int(sys.argv[2]) + 10000))
			eve_url = 'http://' + host + ':' + eve_port + '/registration'
			args = ['python', 'registration_eve.py', host, eve_port]
			# run eve service as subprocess in background
			start_eve_process()
			app.run(host=host, port=int(sys.argv[2]))


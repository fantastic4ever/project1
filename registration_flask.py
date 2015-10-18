from flask import Flask, request
import urllib2, json, requests
import sys, subprocess
import os

app = Flask(__name__)
eve_url = ''

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

if __name__ == "__main__":
		if(len(sys.argv) >= 3):
			host = sys.argv[1]
			#I set eve service runs on different port. If current flask runs on 5000 port, eve runs on 15000 port
			eve_port = str((int(sys.argv[2]) + 10000))
			eve_url = 'http://' + host + ':' + eve_port + '/registration'
			args = ['python', 'registration_eve.py', host, eve_port]
			#run eve service as subprocess in background
			subprocess.Popen(args)
			app.run(host=host, port=int(sys.argv[2]))


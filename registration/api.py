from flask import Flask, request
import urllib2, json, requests

app = Flask(__name__)

@app.route("/private/registration", methods = ['GET'])
def search_for_registration():
		response = requests.get('http://127.0.0.1:5000/registration')
		registration_info = response.json()
		return response.content

@app.route("/private/registration/uni/<uni>", methods = ['GET'])
def search_registration_for_uni(uni):
		payload = {'where': 'UNI==' + uni}
		response = requests.get('http://127.0.0.1:5000/registration', params = payload)
		registration_info = response.json()
		return response.content

@app.route("/private/registration/courseid/<cid>", methods = ['GET'])
def search_registration_for_cid(cid):
		payload = {'where': 'Course_ID==' + cid}
		response = requests.get('http://127.0.0.1:5000/registration', params = payload)
		registration_info = response.json()
		return response.content

@app.route("/private/registration/uni/<uni>/courseid/<cid>", methods = ['GET'])
def search_registration_for_uni_cid(uni, cid):
		payload = {'where': '{"UNI":' + '"' + uni + '", "Course_ID":' + '"' + cid + '"}'}
		response = requests.get('http://127.0.0.1:5000/registration', params = payload)
		registration_info = response.json()
		return response.content

@app.route("/private/registration", methods = ['POST'])
def post_registration():
		content = request.get_json(force = True)
		headers = {'content-type': 'application/json'}
		response = requests.post('http://127.0.0.1:5000/registration', data=json.dumps(content), headers = headers)
		return response.content

@app.route("/private/registration", methods = ['DELETE'])
def delete_registration():
		response = requests.delete('http://127.0.0.1:5000/registration')
		return response.content

@app.route("/private/registration/uni/<uni>", methods = ['DELETE'])
def delete_registration_for_uni(uni):
		payload = {'where': 'UNI==' + uni}
		response = requests.get('http://127.0.0.1:5000/registration', params = payload)
		registration_info = response.json()
		print registration_info
		items = registration_info['_items']
		if items == []:
			return ('', 404)
		else:
			for item in items:
				response = requests.delete('http://127.0.0.1:5000/registration/'+ item['_id'], params = payload, headers = {"If-Match": item['_etag']})
			return response.content

@app.route("/private/registration/courseid/<cid>", methods = ['DELETE'])
def delete_registration_for_cid(cid):
		payload = {'where': 'Course_ID==' + cid}
		response = requests.get('http://127.0.0.1:5000/registration', params = payload)
		registration_info = response.json()
		print registration_info
		items = registration_info['_items']
		if items == []:
			return ('', 404)
		else:
			for item in items:
				response = requests.delete('http://127.0.0.1:5000/registration/'+ item['_id'], params = payload, headers = {"If-Match": item['_etag']})
			return response.content

@app.route("/private/registration/uni/<uni>/courseid/<cid>", methods = ['GET'])
def delete_registration_for_uni_cid(uni, cid):
		payload = {'where': '{"UNI":' + '"' + uni + '", "Course_ID":' + '"' + cid + '"}'}
		response = requests.get('http://127.0.0.1:5000/registration', params = payload)
		registration_info = response.json()
		print registration_info
		items = registration_info['_items']
		if items == []:
			return ('', 404)
		else:
			firstItem = items[0]
			response = requests.delete('http://127.0.0.1:5000/registration/'+ firstItem['_id'], params = payload, headers = {"If-Match": firstItem['_etag']})
			return response.content

@app.route("/private/registration/uni/<uni>/courseid/<cid>", methods = ['PUT'])
def update_registration_for_uni_cid(uni, cid):
		payload = {'where': '{"UNI":' + '"' + uni + '", "Course_ID":' + '"' + cid + '"}'}
		response = requests.get('http://127.0.0.1:5000/registration', params = payload)
		registration_info = response.json()
		print registration_info
		items = registration_info['_items']
		if items == []:
			return ('', 404)
		else:
			firstItem = items[0]
			content = request.get_json(force=True)
			headers = {'content-type': 'application/json', 'If-Match': firstItem['_etag']}
			response = requests.put('http://127.0.0.1:5000/registration/'+ firstItem['_id'],  data = json.dumps(content), headers = headers)
			return response.content

if __name__ == "__main__":
	app.run(host = '127.0.0.1', port = 5001, debug = True)


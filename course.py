from eve import Eve
from eve.auth import BasicAuth
from flask import Response
from pymongo import MongoClient
import requests, json, sys

# Custom error handler
class Custom500Registration(Exception):
	pass

#################################################################################
app = Eve(settings='course_settings.py')
mongo_url = 'mongodb://admin:admin@ds039684.mongolab.com:39684/project1'

@app.errorhandler(Custom500Registration)
def failed_to_delete_registration(error):
	return Response('{"_status": "ERR", "_error": {"message": "Failed to delete related registration information", "code": 500}}', mimetype='application/json')

def pre_DELETE_callback(resource, request, lookup):
	print 'Received DELETE request, resource = %s, lookup = %s' % (resource, lookup)
	
	# TODO Get registration host and port from instance_info db
	registration_service_url = "http://127.0.0.1:3000/private/registration/courseid/"
	client = MongoClient(mongo_url)
	db = client.project1
	cursor = db.instance_info.find({"instanceType": "registration"})
	client.close()
	if cursor.count() < 1:
		return 'Error : Registartion service is not running'
	for document in cursor:
		print document
		print document['host']
		print document['port']
		registration_service_url = 'http://' + document['host'] + ':' + str(document['port']) + '/private/registration/uni/'
	#print '%s"%s"' % (registration_service_url, lookup['call_number'])
	
	# Try delete from registration before delete locally
	response = requests.delete(registration_service_url + '"' + lookup['call_number'] + '"')
	#print response.__dict__['status_code']
	#print response.json # Response body
	status_code = response.__dict__['status_code']
	
	if status_code != 200 and status_code != 404:
		# Failed to delete related registration information
		print "Exception: Failed to delete related registration information"
		raise Custom500Registration

if __name__ == '__main__':
	app.on_pre_DELETE += pre_DELETE_callback
	
	if len(sys.argv) == 3:
		app.run(host = sys.argv[1], port = int(sys.argv[2]))
	else:
		app.run()
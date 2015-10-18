from eve import Eve
from eve.auth import BasicAuth
from flask import Response
import requests, json, sys

# Custom error handler
class Custom500Registration(Exception):
	pass

#################################################################################
app = Eve(settings='course_settings.py')

@app.errorhandler(Custom500Registration)
def failed_to_delete_registration(error):
	return Response('{"_status": "ERR", "_error": {"message": "Failed to delete related registration information", "code": 500}}', mimetype='application/json')

def pre_DELETE_callback(resource, request, lookup):
	print 'Received DELETE request, resource = %s, lookup = %s' % (resource, lookup)
	
	# Try delete from registration before delete locally
	registration_service_url = "http://127.0.0.1:3000/private/registration/courseid/"
	print '%s"%s"' % (registration_service_url, lookup['call_number'])
	response = requests.get(registration_service_url + '"' + lookup['call_number'] + '"')
	#response = requests.delete(registration_service_url + '"' + lookup['call_number'] + '"')
	print response.json()
	
	if response.status_code > 206:
		# Failed to delete related registration information
		print "Failed to delete related registration information"
		raise Custom500Registration

if __name__ == '__main__':
	app.on_pre_DELETE += pre_DELETE_callback
	
	if len(sys.argv) == 3:
		app.run(host = sys.argv[1], port = int(sys.argv[2]))
	else:
		app.run()
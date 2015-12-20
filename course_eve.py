from eve import Eve
from flask import Response, request
from pymongo import MongoClient
import requests, json, sys
import logging
import credentials

import config

mongo_url = 'mongodb://%s:%s@ds039684.mongolab.com:39684/project1' % (credentials.DB_USERNAME, credentials.DB_PASSWORD)

logging.basicConfig(filename=config.COURSE_LOG_FILENAME, 
                    level=logging.INFO, format='%(asctime)s --- %(message)s')


#####################
# Eve Configuration #
#####################
# Get course schema from instance_info db
try:
	client = MongoClient(mongo_url)
	db = client.project1
	cursor = db.schema.find({"name": "course"})
	client.close()
	if cursor.count() < 1:
		raise ConfigurationUnavailable
	# logging.info(cursor[0])
	#logging.info('========= SCHEMA =========\n%s\n==========================' % (cursor[0]['value']))
	schema = cursor[0]['value']
except Exception as e:
	if type(e).__name__ == 'ConnectionError':
		logging.error('Error: Cannot connect to mongodb')
		raise MongoDbUnavailable
	else:
		logging.error('Error: %s when getting schema from mongodb' % (type(e).__name__))
		raise e

# Settings
settings = {
	# Use db hosted on MongoLab
	'MONGO_HOST': 'ds039684.mongolab.com',
	'MONGO_PORT': 39684,
	'MONGO_USERNAME': credentials.DB_USERNAME,
	'MONGO_PASSWORD': credentials.DB_PASSWORD,
	'MONGO_DBNAME': 'project1',
	# URL prefix
	'URL_PREFIX': 'private',

	# Supports ../course/<call_number> where <call_number> consists of 5 digits
	'ID_FIELD': 'call_number',
	'ITEM_LOOKUP_FIELD': 'call_number',
	'ITEM_URL': 'regex("[0-9]{5}")',
	
	# Data schema
	'DOMAIN': {
		'course': {
			'additional_lookup': {
				 'url': 'regex("[0-9]{5}")', #("[\w]+")',
				 'field': 'call_number',
			 },
			 
			'schema': schema
		}
	},
	
	'RESOURCE_METHODS': ['GET', 'POST'],
	'ITEM_METHODS': ['GET', 'PUT', 'DELETE']
}

# App Initialization
app = Eve(settings=settings)



########################
# Custom Error Handler #
########################
class MongoDbUnavailable(Exception):
	pass

class ConfigurationUnavailable(Exception):
	pass

class RegistrationServiceUnavailable(Exception):
	pass

class RegistrationServiceError(Exception):
	pass

@app.errorhandler(MongoDbUnavailable)
def mongodb_failed_to_connect(error):
	return Response('{"_status": "ERR", "_error": {"message": "Failed to connect to mongodb", "code": 500}}', mimetype='application/json', status=500)

@app.errorhandler(ConfigurationUnavailable)
def mongodb_configuration_unavailable(error):
	return Response('{"_status": "ERR", "_error": {"message": "Failed to read configuration of course service from mongodb", "code": 500}}', mimetype='application/json', status=500)

@app.errorhandler(RegistrationServiceUnavailable)
def registration_failed_to_connect(error):
	return Response('{"_status": "ERR", "_error": {"message": "Failed to connect to registration service", "code": 504}}', mimetype='application/json', status=504)

@app.errorhandler(RegistrationServiceError)
def registration_failed_to_delete(error):
	return Response('{"_status": "ERR", "_error": {"message": "Failed to delete related registration information", "code": 502}}', mimetype='application/json', status=502)

@app.errorhandler(Exception)
def unexpected_failure(error):
    template = "An exception of type {0} occured. Arguments:\n{1!r}"
    message = template.format(type(error).__name__, error.args)
    logging.info(message)
    return Response('{"_status": "ERR", "_error": {"message": "Unexpected failure", "code": 500}}', mimetype='application/json', status=500)



##################
# Event handlers #
##################
def pre_DELETE_callback(resource, request, lookup):
	logging.info('Received DELETE request, resource = %s, lookup = %s' % (resource, lookup))
	if resource != 'course':
		return

	# Get registration host and port from instance_info db
	try:
		client = MongoClient(mongo_url)
		db = client.project1
		cursor = db.instance_info.find({"instanceType": "registration"})
		client.close()
		if cursor.count() < 1:
			raise RegistrationServiceUnavailable
		else:
			# logging.info(cursor[0])
			registration_service_url = 'http://' + cursor[0]['host'] + ':' + str(cursor[0]['port']) + '/private/registration/uni/'
		logging.info('requesting %s"%s"' % (registration_service_url, lookup['call_number']))
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			logging.error('Error: Cannot connect to mongodb')
			raise MongoDbUnavailable
		else:
			logging.error('Error: %s when getting registration_service_url from mongodb' % (type(e).__name__))
			raise e

	# Try delete from registration before delete locally
	try:
		response = requests.delete(registration_service_url + '"' + lookup['call_number'] + '"')
		# logging.info(response.__dict__['status_code'])
		# logging.info(response.json # Response body)
		status_code = response.__dict__['status_code']
		if status_code != 200 and status_code != 404:
			logging.error("Exception: Failed to delete related registration information")
			raise RegistrationServiceError
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			logging.error('Error: Registartion service is not running')
			raise RegistrationServiceUnavailable
		else:
			logging.error('Error: %s when deleting %s from registration' % (type(e).__name__, lookup['call_number']))
			raise e





# Main
if __name__ == '__main__':
	app.on_pre_DELETE += pre_DELETE_callback
	
	if len(sys.argv) == 3:
		app.run(host = sys.argv[1], port = int(sys.argv[2]))
	else:
		app.run()
from flask import Flask, request, Response
from pymongo import MongoClient
import course_flask as cf
import urllib2, json, requests
import sys, subprocess, signal, time
import os
import re

mongo_url = 'mongodb://admin:admin@ds039684.mongolab.com:39684/project1'



#############
# Variables #
#############
global eve_process
global args
app = Flask(__name__)
eve_base_url = ''
call_number_pattern = re.compile("[0-9]{5}")
# Get course schema from instance_info db
try:
	client = MongoClient(mongo_url)
	db = client.project1
	cursor = db.schema.find({"name": "course"})
	client.close()
	if cursor.count() < 1:
		raise ConfigurationUnavailable
	# print cursor[0]
	print '========= SCHEMA =========\n%s\n==========================' % (cursor[0]['value'])
	schema = cursor[0]['value']
except Exception as e:
	if type(e).__name__ == 'ConnectionError':
		print 'Error: Cannot connect to mongodb'
		raise MongoDbUnavailable
	else:
		print 'Error: %s when getting schema from mongodb' % (type(e).__name__)
		raise e

########################
# Custom Error Handler #
########################
class MongoDbUnavailable(Exception):
	pass

class ConfigurationUnavailable(Exception):
	pass

class EveUnavailable(Exception):
	pass

@app.errorhandler(MongoDbUnavailable)
def mongodb_failed_to_connect(error):
	return Response('{"_status": "ERR", "_error": {"message": "Failed to connect to mongodb", "code": 500}}', mimetype='application/json', status=500)

@app.errorhandler(ConfigurationUnavailable)
def mongodb_configuration_unavailable(error):
	return Response('{"_status": "ERR", "_error": {"message": "Failed to read configuration of course service from mongodb", "code": 500}}', mimetype='application/json', status=500)

@app.errorhandler(EveUnavailable)
def mongodb_failed_to_connect(error):
	return Response('{"_status": "ERR", "_error": {"message": "Failed to connect to eve service", "code": 500}}', mimetype='application/json', status=500)

@app.errorhandler(Exception)
def unexpected_failure(error):
    template = "An exception of type {0} occured. Arguments:\n{1!r}"
    message = template.format(type(error).__name__, error.args)
    print message
    return Response('{"_status": "ERR", "_error": {"message": "Unexpected failure", "code": 500}}', mimetype='application/json', status=500)



###############
# API Mapping #
###############
@app.route("/private/course", methods = ['GET'])
@app.route("/private/course/", methods = ['GET'])
def course_read_all():
	print 'Recieved GET course request'
	try:
		response = requests.get(eve_base_url)
		return Response(response.content, mimetype='application/json', status=response.status_code)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when add course to eve' % (type(e).__name__)
			raise e

@app.route("/private/course/<call_number>", methods = ['GET'])
@app.route("/private/course/<call_number>/", methods = ['GET'])
def course_read_specific(call_number):
	print 'Recieved GET specific course request'
	try:
		response = requests.get(eve_base_url + '/' + str(call_number))
		return Response(response.content, mimetype='application/json', status=response.status_code)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when add course to eve' % (type(e).__name__)
			raise e

@app.route("/private/course", methods = ['POST'])
@app.route("/private/course/", methods = ['POST'])
def course_create():
	print 'Recieved POST course request'
	try:
		content = request.get_json(force = True)
		print 'content(type=%s) = %s' % (type(content).__name__, content)
		count_invalid = 0
		if (type(content).__name__ == 'list'):
			# Multiple courses, validate each course's call_number format
			for course in content:
				print 'course = %s' % (course)
				for key in course:
					if key == 'call_number' and not call_number_pattern.match(course[key]):
						print '\tinvalid call_number'
						content.remove(course)
						count_invalid += 1
		else:
			# Single course, validate call_number format
			print type(content).__name__
			for key in content:
				# Loop in case of invalid input; invalid input will be handled by eve, here only validate format
				print 'key = %s' % (key)
				if key == 'call_number' and not call_number_pattern.match(content[key]):
					print '\tinvalid call_number'
					content = []
					count_invalid += 1
					break
		print 'A content(type=%s) = %s' % (type(content).__name__, content)
		if len(content) == 0:
			# No valid data left, return error
			return Response('{"_status": "ERR", "_issues": {"call_number": "value format must be of five digits"},"_error": {"message": "Insertion failure: ' + str(count_invalid) + ' document(s) contain(s) error(s)", "code": 422}}', mimetype='application/json', status=422)
		else:
			# Otherwise, ignore invalid data and process valid data
			headers = {'content-type': 'application/json'}
			response = requests.post(eve_base_url, data=json.dumps(content), headers = headers)
			return Response(response.content, mimetype='application/json', status=response.status_code)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when add course to eve' % (type(e).__name__)
			raise e

@app.route("/private/course/<call_number>", methods = ['PUT'])
@app.route("/private/course/<call_number>/", methods = ['PUT'])
def course_update(call_number):
	print 'Recieved PUT course request'
	try:
		# Get course information
		response = requests.get(eve_base_url + '/' + str(call_number))
		course_info = response.json()
		if response.status_code > 204:
			# Fail to get course information by call_number
			return Response(response.content, mimetype='application/json', status=response.status_code)

		# Update data of specified call_number
		attributes_to_update = request.get_json(force = True)
		print 'attributes_to_update(type=%s) = %s' % (type(attributes_to_update).__name__, attributes_to_update)
		client = MongoClient(mongo_url)
		db = client.project1
		for attribute in attributes_to_update:
			print "attribute = %s" % (attribute)
			if attribute == 'call_number':
				return Response('{"_status": "ERR", "_error": {"message": "Modification of lookup field is not allowed", "code": 405}}', mimetype='application/json', status=405)
			else:
				result = db.course.update_one(
					{"call_number": str(call_number)},
				    {
				        "$set": {
				            attribute: attributes_to_update[attribute]
				        },
				        "$currentDate": {"lastModified": True}
				    }
				)
		client.close()
		if result.matched_count < 1:
			raise MongoDbUnavailable

		# Get course information and generate response
		response = requests.get(eve_base_url + '/' + str(call_number))
		course_info = response.json()
		print course_info
		if response.status_code > 204:
			# Fail to get course information by call_number
			return Response(response.content, mimetype='application/json', status=response.status_code)

		print '{"_updated": "'+course_info['_updated']+'", "_links": {"self": {"href": "'+course_info['_links']['self']['href']+'", "title": "'+course_info['_links']['self']['title']+'"}}, "_created": "'+course_info['_created']+'", "_status": "OK", "_id": "'+course_info['_id']+'", "_etag": "'+course_info['_etag']+'"}'
		return Response('{"_updated": "'+course_info['_updated']+'", "_links": {"self": {"href": "'+course_info['_links']['self']['href']+'", "title": "'+course_info['_links']['self']['title']+'"}}, "_created": "'+course_info['_created']+'", "_status": "OK", "_id": "'+course_info['_id']+'", "_etag": "'+course_info['_etag']+'"}', mimetype='application/json', status=200)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when update course in eve' % (type(e).__name__)
			raise e

@app.route("/private/course/<call_number>", methods = ['DELETE'])
@app.route("/private/course/<call_number>/", methods = ['DELETE'])
def delete_registration_for_uni(call_number):
	print 'Recieved DELETE specific schema request'
	try:
		response = requests.delete(eve_base_url + '/' + str(call_number), headers = request.headers)
		return Response(response.content, mimetype='application/json', status=response.status_code)
	except Exception as e:
		if type(e).__name__ == 'ConnectionError':
			print 'Error: Cannot connect to eve'
			raise EveUnavailable
		else:
			print 'Error: %s when add course to eve' % (type(e).__name__)
			raise e



##################
# Schema Related #
##################
@app.route("/private/course/schema", methods = ['GET'])
def schema_view():
		print 'Recieved GET schema request'
		return Response(json.dumps(schema, ensure_ascii=False), mimetype='application/json', status=200)

@app.route("/private/course/schema", methods = ['POST'])
def schema_add_column():
		print 'Recieved POST schema request'
		try:
			columns_to_add = request.get_json(force = True)
			print 'columns_to_add(type=%s) = %s' % (type(columns_to_add).__name__, columns_to_add)
			# Process only new attributes according to local copy of schema
			client = MongoClient(mongo_url)
			db = client.project1
			count = 0
			for column in columns_to_add:
				print "column = %s" % (column)
				if column not in schema:
					print "\tadd"
					# Update db copy
					result = db.schema.update_one(
						{"name": "course"},
					    {
					        "$set": {
					            "value."+column: columns_to_add[column]
					        },
					        "$currentDate": {"lastModified": True}
					    }
					)
					# Update local copy
					schema.update({column: columns_to_add[column]})
					count += 1			
			client.close()
			if count > 0:
				print 'result.matched_count = %s' % (result.matched_count)
				if result.matched_count < 1:
					raise ConfigurationUnavailable
				else:
					# Schema modified, restart eve
					stop_eve_process()
					time.sleep(0.1)
					start_eve_process()
			return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count)+' column(s) added", "code": 200}}', mimetype='application/json', status=200)
		except Exception as e:
			if type(e).__name__ == 'ConnectionError':
				print 'Error: Cannot connect to mongodb'
				raise MongoDbUnavailable
			else:
				print 'Error: %s when adding column to schema' % (type(e).__name__)
				raise e

@app.route("/private/course/schema", methods = ['PUT'])
def schema_update_column():
		print 'Recieved PUT schema request'
		try:
			columns_to_update = request.get_json(force = True)
			print 'columns_to_update(type=%s) = %s' % (type(columns_to_update).__name__, columns_to_update)
			# Process only existing attributes according to local copy of schema
			client = MongoClient(mongo_url)
			db = client.project1
			count = 0
			for column in columns_to_update:
				print "column = %s" % (column)
				if column in schema:
					print "\tupdate"
					# Forbid modification of lookup field
					if column == 'call_number':
						return Response('{"_status": "ERR", "_error": {"message": "Modification of lookup field is not allowed", "code": 405}}', mimetype='application/json', status=405)
					# Update db copy
					result = db.schema.update_one(
						{"name": "course"},
					    {
					        "$set": {
					            "value."+column: columns_to_update[column]
					        },
					        "$currentDate": {"lastModified": True}
					    }
					)
					# Update local copy
					schema.update({column: columns_to_update[column]})
					count += 1
			client.close()
			if count > 0:
				print 'result.matched_count = %s' % (result.matched_count)
				if result.matched_count < 1:
					raise ConfigurationUnavailable
				else:
					# Schema modified, restart eve
					stop_eve_process()
					time.sleep(0.1)
					start_eve_process()
			return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count)+' column(s) updated", "code": 200}}', mimetype='application/json', status=200)
		except Exception as e:
			if type(e).__name__ == 'ConnectionError':
				print 'Error: Cannot connect to mongodb'
				raise MongoDbUnavailable
			else:
				print 'Error: %s when updating column of schema' % (type(e).__name__)
				raise e

@app.route("/private/course/schema", methods = ['DELETE'])
def schema_delete_column():
		print 'Recieved DELETE schema request'
		try:
			columns_to_remove = request.get_json(force = True)
			print 'columns_to_remove(type=%s) = %s' % (type(columns_to_remove).__name__, columns_to_remove)
			# Process only existing attributes according to local copy of schema
			client = MongoClient(mongo_url)
			db = client.project1
			count = 0
			for column in columns_to_remove:
				print "column = %s" % (column)
				if column in schema:
					print "\tremove"
					# Forbid removal of lookup field
					if column == 'call_number':
						return Response('{"_status": "ERR", "_error": {"message": "Removal of lookup field is not allowed", "code": 405}}', mimetype='application/json', status=405)
					# Update db copy
					result = db.schema.update_one(
						{"name": "course"},
					    {
					        "$unset": {
					            "value."+column: ""
					        },
					        "$currentDate": {"lastModified": True}
					    }
					)
					# Update local copy
					del schema[column]
					count += 1
			client.close()
			if count > 0:
				print 'result.matched_count = %s' % (result.matched_count)
				if result.matched_count < 1:
					raise ConfigurationUnavailable
				else:
					# Schema modified, restart eve
					stop_eve_process()
					time.sleep(0.1)
					start_eve_process()
			return Response('{"_status": "SUCCESS", "_success": {"message": "'+str(count)+' column(s) deleted", "code": 200}}', mimetype='application/json', status=200)
		except Exception as e:
			if type(e).__name__ == 'ConnectionError':
				print 'Error: Cannot connect to mongodb'
				raise MongoDbUnavailable
			else:
				print 'Error: %s when deleting column from schema' % (type(e).__name__)
				raise e



def start_eve_process():
	print "starting course eve process..."
	cf.eve_process = subprocess.Popen(args)

def stop_eve_process():
	print "stopping course eve process..."
	os.kill(cf.eve_process.pid, signal.SIGTERM)

if __name__ == "__main__":
		if(len(sys.argv) >= 3):
			host = sys.argv[1]
			#I set eve service runs on different port. If current flask runs on 5000 port, eve runs on 15000 port
			eve_port = str((int(sys.argv[2]) + 10000))
			eve_base_url = 'http://' + host + ':' + eve_port + '/private/course'
			args = ['python', 'course_eve.py', host, eve_port]
			#run eve service as subprocess in background
			start_eve_process()
			app.run(host=host, port=int(sys.argv[2]))


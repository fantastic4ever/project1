from eve import Eve
from flask import Response, request
from pymongo import MongoClient
import requests, json, sys

mongo_url = 'mongodb://admin:admin@ds039684.mongolab.com:39684/project1'



#####################
# Eve Configuration #
#####################
# Get course schema from instance_info db
try:
    client = MongoClient(mongo_url)
    db = client.project1
    cursor = db.instance_info.find({"instanceType": "course"})
    client.close()
    if cursor.count() < 1:
        print 'Error : Configuration info of course service not available'
        raise ConfigurationUnavailable
    # for document in cursor[0]:
        # print cursor[0]
        # print cursor[0]['host']
        # print cursor[0]['port']
    registration_service_url = 'http://' + cursor[0]['host'] + ':' + str(cursor[0]['port']) + '/private/registration/uni/'
    print 'schema(type=%s) = %s' % (type(cursor[0]['schema']).__name__, cursor[0]['schema'])
    schema = cursor[0]['schema']
except Exception as e:
    if type(e).__name__ == 'ConnectionError':
        print 'Error : Cannot connect to mongodb'
        raise MongoDbUnavailable
    else:
        print 'Error : Unexpected 1'
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(e).__name__, e.args)
        print message
        raise e

# Settings
settings = {
    # Use db hosted on MongoLab
    'MONGO_HOST': 'ds039684.mongolab.com',
    'MONGO_PORT': 39684,
    'MONGO_USERNAME': 'admin',
    'MONGO_PASSWORD': 'admin',
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
    print message
    return Response('{"_status": "ERR", "_error": {"message": "Unexpected failure", "code": 500}}', mimetype='application/json')



##################
# Event handlers #
##################
def pre_DELETE_callback(resource, request, lookup):
    print 'Received DELETE request, resource = %s, lookup = %s' % (resource, lookup)
    if resource != 'course':
        return

    # Get registration host and port from instance_info db
    try:
        client = MongoClient(mongo_url)
        db = client.project1
        cursor = db.instance_info.find({"instanceType": "registration"})
        client.close()
        if cursor.count() < 1:
            print 'Error : Registartion service is not running'
            raise RegistrationServiceUnavailable
        for document in cursor:
            # print document
            # print document['host']
            # print document['port']
            registration_service_url = 'http://' + document['host'] + ':' + str(document['port']) + '/private/registration/uni/'
        print 'requesting %s"%s"' % (registration_service_url, lookup['call_number'])
    except Exception as e:
        if type(e).__name__ == 'ConnectionError':
            print 'Error : Cannot connect to mongodb'
            raise MongoDbUnavailable
        else:
            print 'Error : Unexpected 1'
            raise e

    # Try delete from registration before delete locally
    try:
        response = requests.delete(registration_service_url + '"' + lookup['call_number'] + '"')
        # print response.__dict__['status_code']
        # print response.json # Response body
        status_code = response.__dict__['status_code']
        if status_code != 200 and status_code != 404:
            print "Exception: Failed to delete related registration information"
            raise RegistrationServiceError
    except Exception as e:
        if type(e).__name__ == 'ConnectionError':
            print 'Error : Registartion service is not running'
            raise RegistrationServiceUnavailable
        else:
            print 'Error : Unexpected 2'
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
        new_columns = request.get_json(force = True)
        print 'new_columns(type=%s) = %s' % (type(new_columns).__name__, new_columns)
        count = 0
        for column in new_columns:
            print "column = %s" % (column)
            if column not in schema:
                print "\tadd"
                count += 1
        schema.update(new_columns)
        try:
            client = MongoClient(mongo_url)
            db = client.project1
            result = db.instance_info.update_one(
                {"instanceType": "course"},
                {
                    "$set": {
                        "schema": schema
                    },
                    "$currentDate": {"lastModified": True}
                }
            )
            client.close()
            if result.matched_count < 1:
                print 'Error : Configuration info of course service not available'
                raise ConfigurationUnavailable
            return Response('{"_status": "SUCCESS", "_error": {"message": "'+str(count)+' column(s) added", "code": 200}}', mimetype='application/json', status=200)
        except Exception as e:
            if type(e).__name__ == 'ConnectionError':
                print 'Error : Cannot connect to mongodb'
                raise MongoDbUnavailable
            else:
                print 'Error : Unexpected'
                raise e

@app.route("/private/course/schema", methods = ['PUT'])
def schema_update_column():
        print 'Recieved PUT schema request'
        columns_to_update = request.get_json(force = True)
        print 'columns_to_update(type=%s) = %s' % (type(columns_to_update).__name__, columns_to_update)
        try:
            client = MongoClient(mongo_url)
            db = client.project1
            count = 0
            for column in columns_to_update:
                print "column = %s" % (column)
                if column in schema:
                    print "\tupdate"
                    count += 1
                    schema.update({column: columns_to_update[column]})
                    result = db.instance_info.update_one(
                        {"instanceType": "course"},
                        {
                            "$set": {
                                "schema": schema
                            },
                            "$currentDate": {"lastModified": True}
                        }
                    )
            client.close()
            return Response('{"_status": "SUCCESS", "_error": {"message": "'+str(count)+' column(s) updated", "code": 200}}', mimetype='application/json', status=200)
        except Exception as e:
            if type(e).__name__ == 'ConnectionError':
                print 'Error : Cannot connect to mongodb'
                raise MongoDbUnavailable
            else:
                print 'Error : Unexpected'
                raise e

@app.route("/private/course/schema", methods = ['DELETE'])
def schema_delete_column():
        print 'Recieved DELETE schema request'
        columns_to_remove = request.get_json(force = True)
        print 'columns_to_remove(type=%s) = %s' % (type(columns_to_remove).__name__, columns_to_remove)
        try:
            client = MongoClient(mongo_url)
            db = client.project1
            count = 0
            for column in columns_to_remove:
                print "column = %s" % (column)
                if column in schema:
                    print "\tremove"
                    count += 1
                    # Remove locally
                    del schema[column]
                    # Remove from mongodb
                    result = db.instance_info.update_one(
                        {"instanceType": "course"},
                        {
                            "$unset": {
                                "schema."+column: ""
                            },
                            "$currentDate": {"lastModified": True}
                        }
                    )
            client.close()
            return Response('{"_status": "SUCCESS", "_error": {"message": "'+str(count)+' column(s) deleted", "code": 200}}', mimetype='application/json', status=200)
        except Exception as e:
            if type(e).__name__ == 'ConnectionError':
                print 'Error : Cannot connect to mongodb'
                raise MongoDbUnavailable
            else:
                print 'Error : Unexpected'
                raise e

# Main
if __name__ == '__main__':
    app.on_pre_DELETE += pre_DELETE_callback
    
    if len(sys.argv) == 3:
        app.run(host = sys.argv[1], port = int(sys.argv[2]))
    else:
        app.run()
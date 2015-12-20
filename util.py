from pymongo import MongoClient
import credentials

mongo_url = 'mongodb://%s:%s@ds039684.mongolab.com:39684/project1' % (credentials.DB_USERNAME, credentials.DB_PASSWORD)

def update_eve_setting(name, my_schema):
	client = MongoClient(mongo_url)
	schema_col = client.project1.schema
	result = schema_col.update_one({"name": name}, {"$set":{"value":my_schema}})
	client.close()
	return result

def get_student_setting_template():
	return {
		'MONGO_HOST': 'ds039684.mongolab.com',
	    'MONGO_PORT': 39684,
	    'MONGO_DBNAME': 'project1',
	    'MONGO_USERNAME': credentials.DB_USERNAME,
	    'MONGO_PASSWORD': credentials.DB_PASSWORD,
	    'DOMAIN': {
	    },
	    'RESOURCE_METHODS': ['GET', 'DELETE', 'POST'],
	    'ITEM_METHODS': ['GET', 'DELETE', 'PUT']
	}

def get_eve_schema(name):
	client = MongoClient(mongo_url)
	schema_col = client.project1.schema
	my_schema = schema_col.find_one({"name":name})["value"]
	client.close()
	return my_schema

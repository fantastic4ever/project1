from eve import Eve
import sys
import registration_global
from pymongo import MongoClient

"""my_settings = {
    'MONGO_HOST': 'ds039684.mongolab.com',
    'MONGO_PORT': 39684,
	'MONGO_USERNAME': 'admin',
	'MONGO_PASSWORD': 'admin',
	'MONGO_DBNAME': 'project1',
    'DOMAIN': {
    	'registration': {
        	'schema': {
            	'UNI': {
                	'type': 'string'
            	},
            	'Course_ID': {
                	'type': 'string'
            	}
        	},
        	'additional_lookup': {
            	'url': 'regex("[\w]+")',
            	'field': 'UNI',
        	}
    	}
	},
	'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
	'ITEM_METHODS': ['GET', 'PUT', 'DELETE', 'PATCH']
}"""


uri = 'mongodb://admin:admin@ds039684.mongolab.com:39684/project1'
client = MongoClient(uri)
db = client.get_default_database()
settings = db.settings
my_settings = settings.find_one({'name': 'registration'})
print 'eve.......'
print my_settings['value']
app = Eve(settings=my_settings['value']) 
 
if __name__ == '__main__':
    if (len(sys.argv) == 3):
    	app.run(host = sys.argv[1], port = int(sys.argv[2]))
    else:
    	app.run()
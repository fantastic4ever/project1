from eve import Eve
import sys
from pymongo import MongoClient
import logging
import config
import credentials


logging.basicConfig(filename=config.REGISTRATION_LOG_FILENAME, 
                    level=logging.INFO, format='%(asctime)s --- %(message)s')

uri = 'mongodb://%s:%s@ds039684.mongolab.com:39684/project1' % (credentials.DB_USERNAME, credentials.DB_PASSWORD)
client = MongoClient(uri)
db = client.get_default_database()
schema = db.schema
my_schema = schema.find_one({'name': 'registration'})
logging.info('eve.......')
logging.info(my_schema['value'])

my_settings = {
    'MONGO_HOST': 'ds039684.mongolab.com',
    'MONGO_PORT': 39684,
	'MONGO_USERNAME': credentials.DB_USERNAME,
	'MONGO_PASSWORD': credentials.DB_PASSWORD,
	'MONGO_DBNAME': 'project1',
    'DOMAIN': {
    	'registration': {
        	'schema': my_schema['value'],
        	'additional_lookup': {
            	'url': 'regex("[\w]+")',
            	'field': 'UNI',
        	}
    	}
	},
	'RESOURCE_METHODS': ['GET', 'POST', 'DELETE'],
	'ITEM_METHODS': ['GET', 'PUT', 'DELETE', 'PATCH']
}

app = Eve(settings=my_settings) 
 
if __name__ == '__main__':
    if (len(sys.argv) == 3):
    	app.run(host = sys.argv[1], port = int(sys.argv[2]))
    else:
    	app.run()
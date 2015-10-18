# Use db hosted on MongoLab
MONGO_HOST = 'ds039684.mongolab.com'
MONGO_PORT = 39684
MONGO_USERNAME = 'admin'
MONGO_PASSWORD = 'admin'
MONGO_DBNAME = 'project1'

# URL prefix
URL_PREFIX = 'private'

# Supports ../course/<call_number> where <call_number> consists of 5 digits
ID_FIELD = 'call_number'
ITEM_LOOKUP_FIELD = ID_FIELD
ITEM_URL = 'regex("[0-9]{5}")'

DOMAIN = {
    'course': {
		'additional_lookup': {
			 'url': 'regex("[0-9]{5}")', #("[\w]+")',
			 'field': 'call_number',
		 },
		 
		'schema': {
            'call_number': {
                'type': 'string',
				'unique': True,
				'required': True
            },
            'subject': {
                'type': 'string'
            },
            'department': {
                'type': 'string',
            },
            'course_number': {
                'type': 'string'
            },
			'section_number': {
                'type': 'string'
            },
            'title': {
                'type': 'string'
            },
			'credit': {
                'type': 'integer'
            },
			'instructor': {
                'type': 'string'
            },
			'semester': {
                'type': 'string'
            },
			'day_time': {
                'type': 'string'
            },
			'location': {
                'type': 'string'
            },
			'enrollment_cap': {
                'type': 'integer'
            },
			'enrollment_current': {
                'type': 'integer'
            },
			'texbook': {
				'type': 'string'
			}
        }
    }
}

RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PUT', 'DELETE']
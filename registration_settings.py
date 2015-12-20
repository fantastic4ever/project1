import credentials

MONGO_HOST = 'ds039684.mongolab.com'
MONGO_PORT = 39684
MONGO_USERNAME = credentials.DB_USERNAME
MONGO_PASSWORD = credentials.DB_PASSWORD
MONGO_DBNAME = 'project1'

DOMAIN = {
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
}

#ALLOWED_FILTERS = ['UNI', 'Course_ID']
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PUT', 'DELETE', 'PATCH']
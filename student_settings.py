# RESOURCE_METHODS = ['GET','POST','DELETE']
# ITEM_METHODS = ['GET','PATCH','DELETE']

# MONGO_HOST = 'ds039684.mongolab.com'
# MONGO_PORT = 39684
# MONGO_USERNAME = 'admin'
# MONGO_PASSWORD = 'admin'
# MONGO_DBNAME = 'project1'

# DOMAIN = {
# 	'student': {
# 		'schema' : {
# 			'uni' : {
# 				'type' : 'string',
# 				'empty' : False,
# 				'unique' : True
# 			},
# 			'firstname' : {
# 				'type' : 'string',
# 				'empty' : False
# 			},
# 			'lastname' : {
# 				'type' : 'string',
# 				'empty' : False
# 			},
# 			'middlename' : {
# 				'type' : 'string'
# 			},
# 			'major' : {
# 				'type' : 'string'
# 			}
# 		},
# 		'additional_lookup': {
#             'url': 'regex("[\w]+")',
#             'field': 'uni',
#             }
# 		}}

global my_settings
my_settings = {
	'RESOURCE_METHODS': ['GET','POST','DELETE'],
	'ITEM_METHODS': ['GET','PATCH','DELETE'],
    'MONGO_HOST': 'ds039684.mongolab.com',
    'MONGO_PORT': 39684,
    'MONGO_DBNAME': 'project1',
    'MONGO_USERNAME': 'admin',
	'MONGO_PASSWORD': 'admin',
    'DOMAIN': {
	'student': {
		'schema' : {
			'uni' : {
				'type' : 'string',
				'empty' : False,
				'unique' : True
			},
			'firstname' : {
				'type' : 'string',
				'empty' : False
			},
			'lastname' : {
				'type' : 'string',
				'empty' : False
			},
			'middlename' : {
				'type' : 'string'
			},
			'major' : {
				'type' : 'string'
			}
		},
		'additional_lookup': {
            'url': 'regex("[\w]+")',
            'field': 'uni',
            }
		}
	}
}
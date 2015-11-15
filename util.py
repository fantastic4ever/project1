from pymongo import MongoClient

mongo_url = 'mongodb://admin:admin@ds039684.mongolab.com:39684/project1'

def get_eve_setting(name, version):
	client = MongoClient(mongo_url)
	setting_col = client.project1.settings
	my_setting = setting_col.find_one({"name":"student", "version":"current"})["value"] # read eve settings from db
	client.close()
	return my_setting

def update_eve_setting(name, version, my_setting):
	client = MongoClient(mongo_url)
	setting_col = client.project1.settings
	result = setting_col.update_one({"version": version, "name": name}, {"$set":{"value":my_setting}})
	client.close()
	return result
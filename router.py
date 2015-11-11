# -*- coding: utf-8 -*-
"""
data API
"""
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import requests
import logging
import urllib
import subprocess
import os
from flask.ext.pymongo import PyMongo
from collections import OrderedDict

import credentials
import router_config

app = Flask(__name__)
app.config['MONGOLAB_HOST'] = 'ds039684.mongolab.com'
app.config['MONGOLAB_PORT'] = 39684
app.config['MONGOLAB_DBNAME'] = 'project1'
app.config['MONGO_USERNAME'] = credentials.DB_USERNAME
app.config['MONGO_PASSWORD'] = credentials.DB_PASSWORD
mongo = PyMongo(app)
logging.basicConfig(filename=router_config.LOG_FILENAME,level=logging.INFO,format='%(asctime)s --- %(message)s')
DEVNULL = open(os.devnull, 'wb')
instance_info_table = {}  # map iid/port to (instanceType,subp)
student_shard_table = {}  # map shar to (host,port)
course_iid = None
registration_iid = None


### get a list of all available public api ###
@app.route('/public', methods=['GET'])
def list_api():
    output = []
    html = "<!DOCTYPE html><html><head><title>Page Title</title></head><body><p>%s</p></body></html>"
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("<b>%s</b><br>%s<br>%s<br>"%(rule.endpoint, methods, url))
        output.append(line)

    return html%"</p><p>".join(sorted(output))

### data manipulation api for student ###
@app.route('/public/student', methods=['POST'])
def create_student():
    logging.info("receive a create_student request")
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    shard_index = uni_hash(uni)
    host,port = student_shard_table[shard_index]
    return requests.post('http://%s:%d/private/student'%(host,port), json=sanitized_data).status_code

@app.route('/public/student/<uni>', methods=['GET'])
def retrive_student(uni):
    logging.info("receive a retrive_student request")
    shard_index = uni_hash(uni)
    return requests.get('http://%s:%d/private/student/%s'%(host,port,uni)).content

@app.route('/public/student/<uni>', methods=['PUT'])
def update_student(uni):
    logging.info("receive a update_student request")
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    shard_index = uni_hash(uni)
    return requests.put('http://%s:%d/private/student/%s'%(host,port,uni), json=sanitized_data).status_code

@app.route('/public/student/<uni>', methods=['DELETE'])
def delete_student(uni):
    logging.info("receive a delete_student request")
    shard_index = uni_hash(uni)
    return requests.delete('http://%s:%d/private/student/%s'%(host,port,uni)).status_code

# ### data definition api for student ###
# @app.route('/public/student/scheme', methods=['POST'])
# def create_new_column_for_student_scheme():
#     logging.info("receive a create_new_column_for_student_scheme request")
#     return requests.post("/private/student/scheme",params=request.args).status_code

# @app.route('/public/student/scheme', methods=['GET'])
# def retrive_student_scheme():
#     logging.info("receive a retrive_student_scheme request")
#     return requests.get('/private/student/scheme').content

# @app.route('/public/student/scheme', methods=['PUT'])
# def update_column_of_student_scheme():
#     logging.info("receive a update_column_of_student_scheme request")
#     return requests.put("/private/student/scheme",params=request.args).status_code

# @app.route('/public/student/scheme', methods=['DELETE'])
# def delete_column_of_student_scheme():
#     logging.info("receive a delete_column_of_student_scheme request")
#     return requests.delete("/private/student/scheme",params=request.args).status_code


### data manipulation api for course ###
@app.route('/public/course', methods=['POST'])
def create_course():
    logging.info("receive a create_course request")
    if not course_iid:  # iid is port
        return "500: course instance is not started"
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    return requests.post('http://%s:%d/private/course'%(router_config.HOST,course_iid), json=sanitized_data).status_code

@app.route('/public/course/<cid>', methods=['GET'])
def retrive_course(cid):
    logging.info("receive a retrive_course request")
    if not course_iid:
        return "500: course instance is not started"
    return requests.get('http://%s:%d/private/course/%s'%(router_config.HOST,course_iid,cid)).content

@app.route('/public/course/<cid>', methods=['PUT'])
def update_course(cid):
    logging.info("receive a update_course request")
    if not course_iid:
        return "500: course instance is not started"
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    return requests.put('http://%s:%d/private/course/%s'%(router_config.HOST,course_iid,cid)).status_code

@app.route('/public/course/<cid>', methods=['DELETE'])
def delete_course(cid):
    logging.info("receive a delete_course request")
    if not course_iid:
        return "500: course instance is not started"
    return requests.delete('http://%s:%d/private/course/%s'%(router_config.HOST,course_iid,cid)).status_code


### data manipulation api for registration ###
@app.route('/public/registration/<rid>', methods=['POST'])
def create_registration(rid):
    logging.info("receive a create_registration request")
    if not registration_iid:  # iid is port
        return "500: registration instance is not started"
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    return requests.post('http://%s:%d/private/registration'%(router_config.HOST,registration_iid), json=sanitized_data).status_code

@app.route('/public/registration/<rid>', methods=['GET'])
def retrive_registration(rid):
    logging.info("receive a retrive_registration request")
    if not registration_iid:  # iid is port
        return "500: registration instance is not started"
    return requests.get('http://%s:%d/private/registration/%s'%(router_config.HOST,registration_iid,rid)).content

@app.route('/public/registration/<rid>', methods=['PUT'])
def update_registration(rid):
    logging.info("receive a update_registration request")
    if not registration_iid:  # iid is port
        return "500: registration instance is not started"
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    return requests.put('http://%s:%d/private/registration/%s'%(router_config.HOST,registration_iid,rid)).status_code

@app.route('/public/registration/<rid>', methods=['DELETE'])
def delete_registration(rid):
    logging.info("receive a delete_registration request")
    if not registration_iid:  # iid is port
        return "500: registration instance is not started"
    return requests.delete('http://%s:%d/private/course/%s'%(router_config.HOST,registration_iid,rid)).status_code

### api for creating new microservice instance
### TODO: store the instance pid into db in case of failure of router process
@app.route('/public/instance/<instanceType>', methods=['POST'])
def create_instance(instanceType):
    try:
        port = router_config.PORT_POOL.pop()  ## port is also the instance id
        code_path = None
        if instanceType=="student":
            code_path = router_config.STUDENT_CODE_PATH
        if instanceType=="course":
            code_path = router_config.COURSE_CODE_PATH
            global course_iid
            course_iid = port
        if instanceType=="registration":
            code_path = router_config.REGISTRATION_CODE_PATH
            global registration_iid
            registration_iid = port
        subp = subprocess.Popen(['python',
                                  code_path,
                                  '%s:%d'%(router_config.HOST,port)],
                                  stdout=DEVNULL, stderr=DEVNULL)
        instance_info_table[port] = (instanceType,subp)
        this_instance = {"instanceId":port,"instanceType":"course","host":router_config.HOST,"port":port}
        mongo.db.instance_info.insert_one(this_instance)

        if instanceType=="student":  # map shard number with host:port
            this_shard_number = router_config.NUMBER_OF_SHARD
            student_shard_table[this_shard_number] = (host,port)
            router_config.NUMBER_OF_SHARD+=1
    except Exception, e:
        return 500
    # succeed
    return 201

### delete any microservice instance
@app.route('/public/instance/<iid>', methods=['DELETE'])
def delete_instance(iid):  ## port is also the instance id
    try:
        instanceType,subp = instance_info_table[iid]
        subp.kill()
        del instance_info_table[iid]
        mongo.db.instance_info.delete_one("instanceId":iid)
        if instanceType=="student":  # unmap shard number
            for shard,(host,port) in student_shard_table:  # find the corresponding shard and delete
                if str(port)==str(iid):
                    del student_shard_table[shard]
                    router_config.NUMBER_OF_SHARD-=1
        if instanceType=="course":
            global course_iid
            course_iid = None
        if instanceType=="registration":
            global registration_iid
            registration_iid = None
    except Exception, e:
        return 500
    # succeed
    return 201

### util functions
def uni_hash(uni):
    return uni.__hash__()%router_config.NUMBER_OF_SHARD

def getSanitizedJson(original_json):
    """
    used for security check (incomplete)
    """
    return original_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
# -*- coding: utf-8 -*-
"""
data API
"""
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, Response
import requests
import logging
import urllib
import subprocess
import os
import signal
import json
from pymongo import MongoClient
from collections import OrderedDict

import credentials
import router_config

app = Flask(__name__)
mongo_url = 'mongodb://%s:%s@ds039684.mongolab.com:39684/project1' % (credentials.DB_USERNAME, credentials.DB_PASSWORD)
mongo = MongoClient(mongo_url)
logging.basicConfig(filename=router_config.LOG_FILENAME,
                    level=logging.INFO, format='%(asctime)s --- %(message)s')
DEVNULL = open(os.devnull, 'wb')
instance_info_table = {}  # map iid/port to (instanceType,subp)
student_shard_table = {}  # map shard to (host,port)
course_iid = None
registration_iid = None
current_number_of_shards = 0
json_headers = {'content-type': 'application/json'}


@app.route('/public', methods=['GET'])
def list_api():
    """get a list of all available public api"""
    output = []
    html = "<!DOCTYPE html><html><head><title>Page Title</title></head><body><p>%s</p></body></html>"
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("<b>%s</b><br>%s<br>%s<br>" %
                              (rule.endpoint, methods, url))
        output.append(line)

    return html % "</p><p>".join(sorted(output))


@app.route('/public/student', methods=['POST'])
def create_student():
    """api for student CREATE"""
    logging.info("receive a create_student request")
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return "invalid request"
    if "uni" not in sanitized_data:
        return "uni is not found"
    uni = sanitized_data["uni"]
    shard_index = uni_hash(uni)
    logging.info(student_shard_table)
    if str(shard_index) not in student_shard_table:
        return "500: student instance %s is not started" % shard_index
    host, port = student_shard_table[str(shard_index)]
    # print sanitized_data
    # print 'http://%s:%s/private/student' % (host, port)
    return str(requests.post('http://%s:%s/private/student' % (host, port), headers=json_headers, data=json.dumps(sanitized_data)).status_code)
"""data manipulation api for student"""


@app.route('/public/student/<uni>', methods=['GET'])
def retrive_student(uni):
    """api for student RETRIVE"""
    logging.info("receive a retrive_student request")
    shard_index = uni_hash(uni)
    if shard_index not in student_shard_table:
        logging.info(student_shard_table)
        return "500: student instance %s is not started" % shard_index
    host, port = student_shard_table[str(shard_index)]
    response = requests.get('http://%s:%s/private/student/%s' % (host, port, uni))
    return Response(response.content, mimetype='application/json', status=200)


# @app.route('/public/student', methods=['GET'])
# def retrive_all_student(uni):
#     """api for student RETRIVE ALL"""
#     logging.info("receive a retrive_all_student request")
#     result = 
#     for shard_number, (host, port) in student_shard_table:

#     return requests.get('http://%s:%s/private/student/%s' % (host, port, uni)).content


@app.route('/public/student/<uni>', methods=['PUT'])
def update_student(uni):
    """api for student UPDATE"""
    logging.info("receive a update_student request")
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return "invalid request"
    shard_index = uni_hash(uni)
    if str(shard_index) not in student_shard_table:
        return "500: student instance %s is not started" % shard_index
    host, port = student_shard_table[str(shard_index)]
    return str(requests.put('http://%s:%s/private/student/%s' % (host, port, uni), headers=json_headers, data=json.dumps(sanitized_data)).status_code)


@app.route('/public/student/<uni>', methods=['DELETE'])
def delete_student(uni):
    """api for student DELETE"""
    logging.info("receive a delete_student request")
    shard_index = uni_hash(uni)
    if str(shard_index) not in student_shard_table:
        return "500: student instance %s is not started" % shard_index
    host, port = student_shard_table[str(shard_index)]
    return str(requests.delete('http://%s:%s/private/student/%s' % (host, port, uni)).status_code)

"""data definition api for student"""


@app.route('/public/student/scheme', methods=['POST'])
def create_new_column_for_student_scheme():
    logging.info("receive a create_new_column_for_student_scheme request")
    host, port = student_shard_table[0]
    return str(requests.post("http://%s:%s/private/student/scheme" % (host, port), params=request.args).status_code)


@app.route('/public/student/scheme', methods=['GET'])
def retrive_student_scheme():
    logging.info("receive a retrive_student_scheme request")
    host, port = student_shard_table[0]
    response = requests.get("http://%s:%s/private/student/scheme" % (host, port))
    return Response(response.content, mimetype='application/json', status=200)


@app.route('/public/student/scheme', methods=['PUT'])
def update_column_of_student_scheme():
    logging.info("receive a update_column_of_student_scheme request")
    host, port = student_shard_table[0]
    return str(requests.put("http://%s:%s/private/student/scheme" % (host, port), params=request.args).status_code)


@app.route('/public/student/scheme', methods=['DELETE'])
def delete_column_of_student_scheme():
    logging.info("receive a delete_column_of_student_scheme request")
    host, port = student_shard_table[0]
    return str(requests.delete("http://%s:%s/private/student/scheme" % (host, port), params=request.args).status_code)


"""data manipulation api for course"""


@app.route('/public/course', methods=['POST'])
def create_course():
    logging.info("receive a create_course request")
    if not course_iid:  # iid is port
        return "500: course instance is not started"
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return "invalid request"
    return str(requests.post('http://%s:%s/private/course' % (router_config.HOST, course_iid), headers=json_headers, data=json.dumps(sanitized_data)).status_code)


@app.route('/public/course/<cid>', methods=['GET'])
def retrive_course(cid):
    logging.info("receive a retrive_course request")
    if not course_iid:
        return "500: course instance is not started"
    response = requests.get('http://%s:%s/private/course/%s' % (router_config.HOST, course_iid, cid))
    return Response(response.content, mimetype='application/json', status=200)


@app.route('/public/course/', methods=['GET'])
def retrive_all_course():
    logging.info("receive a retrive_all_course request")
    if not course_iid:
        return "500: course instance is not started"
    response = requests.get('http://%s:%s/private/course' % (router_config.HOST, course_iid))
    return Response(response.content, mimetype='application/json', status=200)


@app.route('/public/course/<cid>', methods=['PUT'])
def update_course(cid):
    logging.info("receive a update_course request")
    if not course_iid:
        return "500: course instance is not started"
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return "invalid request"
    return str(requests.put('http://%s:%s/private/course/%s' % (router_config.HOST, course_iid, cid)).status_code)


@app.route('/public/course/<cid>', methods=['DELETE'])
def delete_course(cid):
    logging.info("receive a delete_course request")
    if not course_iid:
        return "500: course instance is not started"
    return str(requests.delete('http://%s:%s/private/course/%s' % (router_config.HOST, course_iid, cid)).status_code)


"""data manipulation api for registration"""


@app.route('/public/registration/<rid>', methods=['POST'])
def create_registration(rid):
    logging.info("receive a create_registration request")
    if not registration_iid:  # iid is port
        return "500: registration instance is not started"
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return "invalid request"
    return str(requests.post('http://%s:%s/private/registration' % (router_config.HOST, registration_iid), headers=json_headers, data=json.dumps(sanitized_data)).status_code)


@app.route('/public/registration', methods=['GET'])
def retrive_all_registration():
    logging.info("receive a retrive_all_registration request")
    if not registration_iid:  # iid is port
        return "500: registration instance is not started"
    response = requests.get('http://%s:%s/private/registration' % (router_config.HOST, registration_iid))
    return Response(response.content, mimetype='application/json', status=200)


@app.route('/public/registration/<rid>', methods=['GET'])
def retrive_registration(rid):
    logging.info("receive a retrive_registration request")
    if not registration_iid:  # iid is port
        return "500: registration instance is not started"
    response = requests.get('http://%s:%s/private/registration/%s' % (router_config.HOST, registration_iid, rid))
    return Response(response.content, mimetype='application/json', status=200)


@app.route('/public/registration/<rid>', methods=['PUT'])
def update_registration(rid):
    logging.info("receive a update_registration request")
    if not registration_iid:  # iid is port
        return "500: registration instance is not started"
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return "invalid request"
    return str(requests.put('http://%s:%s/private/registration/%s' % (router_config.HOST, registration_iid, rid)).status_code)


@app.route('/public/registration/<rid>', methods=['DELETE'])
def delete_registration(rid):
    logging.info("receive a delete_registration request")
    if not registration_iid:  # iid is port
        return "500: registration instance is not started"
    return str(requests.delete('http://%s:%s/private/course/%s' % (router_config.HOST, registration_iid, rid)).status_code)

"""api for creating new microservice instance"""
# TODO: store the instance pid into db in case of failure of router process


@app.route('/public/instance/<instanceType>', methods=['POST'])
@app.route('/public/instance/<instanceType>/<shard_number>', methods=['POST'])
def create_instance(instanceType, shard_number = -1):
    try:
        port = str(router_config.PORT_POOL.pop())  # port is also the instance id
        code_path = None
        if instanceType == "student":
            code_path = router_config.STUDENT_CODE_PATH
        if instanceType == "course":
            code_path = router_config.COURSE_CODE_PATH
            global course_iid
            course_iid = port
        if instanceType == "registration":
            code_path = router_config.REGISTRATION_CODE_PATH
            global registration_iid
            registration_iid = port
        if instanceType == "student":  # map shard number with host:port
            if shard_number < 0:
                return "illegal shard_number!"
            if shard_number in student_shard_table:
                return "Shard %s has already been started!" % shard_number
            global current_number_of_shards
            if current_number_of_shards>=router_config.NUMBER_OF_SHARD:
                return "reach the max of shards"
            student_shard_table[str(shard_number)] = (router_config.HOST, port)
            current_number_of_shards += 1
        subp = subprocess.Popen(['python',
                                 code_path,
                                 str(router_config.HOST),
                                 str(port),
                                 str(shard_number)],
                                stdout=DEVNULL, stderr=DEVNULL)
        instance_info_table[port] = (instanceType, subp)
        this_instance = {"instanceId": port, "instanceType": instanceType,
                         "host": router_config.HOST, "port": port}
        mongo.project1.instance_info.insert_one(this_instance)
        
    except Exception, e:
        print e
        return "500"
    # succeed
    return "201"

"""delete any microservice instance"""


@app.route('/public/instance/<iid>', methods=['DELETE'])
def delete_instance(iid):  # port is also the instance id
    # try:
    instanceType, subp = instance_info_table[iid]
    requests.delete('http://%s:%s/private/instance/%s' % (router_config.HOST, iid, instanceType))  # kill eve
    subp.kill()
    del instance_info_table[iid]
    mongo.project1.instance_info.delete_one({"instanceId": iid})
    if instanceType == "student":  # unmap shard number
        # find the corresponding shard and delete
        for shard, (host, port) in student_shard_table.items():
            if str(port) == str(iid):
                del student_shard_table[shard]
                global current_number_of_shards
                current_number_of_shards -= 1
    if instanceType == "course":
        global course_iid
        course_iid = None
    if instanceType == "registration":
        global registration_iid
        registration_iid = None
    # except Exception, e:
    #     logging.error(e)
    #     return "500"
    return "201"  # succeed

"""util functions"""


def uni_hash(uni):
    return str(uni.__hash__() % router_config.NUMBER_OF_SHARD)


def getSanitizedJson(original_json):
    """used for security check (incomplete)"""
    return original_json

def init():
    mongo.project1.drop_collection('instance_info')

if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0', debug=True)

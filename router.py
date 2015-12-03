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
import httplib

import credentials
import config

app = Flask(__name__)
mongo_url = 'mongodb://%s:%s@ds039684.mongolab.com:39684/project1' % (credentials.DB_USERNAME, credentials.DB_PASSWORD)
mongo = MongoClient(mongo_url)
logging.basicConfig(filename=config.ROUTER_LOG_FILENAME,
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
        return Response("request contains illegal data", status=400)
    if "uni" not in sanitized_data:
        return "uni is not found"
    uni = sanitized_data["uni"]
    shard_index = uni_hash(uni)
    logging.info(student_shard_table)
    if str(shard_index) not in student_shard_table:
        return Response("student instance %s is not started" % shard_index, status=500)
    host, port = student_shard_table[str(shard_index)]
    response = requests.post('http://%s:%s/private/student' % (host, port), headers=json_headers, data=json.dumps(sanitized_data))
    return Response(response.content, mimetype='application/json', status=response.status_code)
"""data manipulation api for student"""


@app.route('/public/student/<uni>', methods=['GET'])
def retrive_student(uni):
    """api for student RETRIVE"""
    logging.info("receive a retrive_student request")
    shard_index = uni_hash(uni)
    if shard_index not in student_shard_table:
        logging.info(student_shard_table)
        return Response("student instance %s is not started" % shard_index, status=500)
    host, port = student_shard_table[str(shard_index)]
    response = requests.get('http://%s:%s/private/student/%s' % (host, port, uni))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/student', methods=['GET'])
def retrive_all_student():
    """api for student RETRIVE ALL"""
    logging.info("receive a retrive_all_student request")
    result = []
    for shard_number, (host, port) in student_shard_table.items():
        # logging.info(requests.get('http://%s:%s/private/student' % (host, port)).content)
        response = requests.get('http://%s:%s/private/student' % (host, port))
        result.append(response.content)
    logging.info(type(response.content))
    logging.info(type(json.dumps(result)))
    logging.info(type(result))
    logging.info(Response(result, mimetype='application/json', status=response.status_code))
    logging.info(Response(json.dumps(result), mimetype='application/json', status=response.status_code))
    return Response(json.dumps(result), mimetype='application/json', status=response.status_code)
    return json.dumps(result)


@app.route('/public/student/<uni>', methods=['PUT'])
def update_student(uni):
    """api for student UPDATE"""
    logging.info("receive a update_student request")
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    shard_index = uni_hash(uni)
    if str(shard_index) not in student_shard_table:
        return Response("student instance %s is not started" % shard_index, status=500)
    host, port = student_shard_table[str(shard_index)]
    response = requests.put('http://%s:%s/private/student/%s' % (host, port, uni), headers=json_headers, data=json.dumps(sanitized_data))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/student/<uni>', methods=['DELETE'])
def delete_student(uni):
    """api for student DELETE"""
    logging.info("receive a delete_student request")
    shard_index = uni_hash(uni)
    if str(shard_index) not in student_shard_table:
        return Response("student instance %s is not started" % shard_index, status=500)
    host, port = student_shard_table[str(shard_index)]
    response = requests.delete('http://%s:%s/private/student/%s' % (host, port, uni))
    return Response(response.content, mimetype='application/json', status=response.status_code)

"""data definition api for student"""


@app.route('/public/student/schema', methods=['POST'])
def create_new_column_for_student_schema():
    logging.info("receive a create_new_column_for_student_schema request")
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    if not student_shard_table:
        return Response("Shard table is empty. Please start at least one shard.", status=500)
    host, port = student_shard_table.items()[0]
    response = requests.post("http://%s:%s/private/student/schema" % (host, port), headers=json_headers, data=json.dumps(sanitized_data))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/student/schema', methods=['GET'])
def retrive_student_schema():
    logging.info("receive a retrive_student_schema request")
    if not student_shard_table:
        return Response("Shard table is empty. Please start at least one shard.", status=500)
    host, port = student_shard_table.items()[0]
    response = requests.get("http://%s:%s/private/student/schema" % (host, port))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/student/schema', methods=['PUT'])
def update_column_of_student_schema():
    logging.info("receive a update_column_of_student_schema request")
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    if not student_shard_table:
        return Response("Shard table is empty. Please start at least one shard.", status=500)
    host, port = student_shard_table.items()[0]
    response = requests.put("http://%s:%s/private/student/schema" % (host, port), headers=json_headers, data=json.dumps(sanitized_data))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/student/schema', methods=['DELETE'])
def delete_column_of_student_schema():
    logging.info("receive a delete_column_of_student_schema request")
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    if not student_shard_table:
        return Response("Shard table is empty. Please start at least one shard.", status=500)
    host, port = student_shard_table.items()[0]
    response = requests.delete("http://%s:%s/private/student/schema" % (host, port), headers=json_headers, data=json.dumps(sanitized_data))
    return Response(response.content, mimetype='application/json', status=response.status_code) 


"""data manipulation api for course"""


@app.route('/public/course', methods=['POST'])
def create_course():
    logging.info("receive a create_course request")
    if not course_iid:  # iid is port
        return Response("course instance is not started", status=500)
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    conn = httplib.HTTPConnection('%s:%s' % (config.HOST, course_iid))
    conn.request("POST", "/private/course/", json.dumps(sanitized_data), json_headers)
    return str(conn.getresponse().read())
    # response = requests.post('http://%s:%s/private/course' % (config.HOST, course_iid), headers=json_headers, data=json.dumps(sanitized_data))
    # return Response(response.content, mimetype='application/json', status=response.status_code)
    # return str(requests.post('http://%s:%s/private/course' % (config.HOST, course_iid), headers=json_headers, data=json.dumps(sanitized_data)).status_code)


@app.route('/public/course/<cid>', methods=['GET'])
def retrive_course(cid):
    logging.info("receive a retrive_course request")
    if not course_iid:
        return Response("course instance is not started", status=500)
    response = requests.get('http://%s:%s/private/course/%s' % (config.HOST, course_iid, cid))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/course', methods=['GET'])
def retrive_all_course():
    logging.info("receive a retrive_all_course request")
    if not course_iid:
        return Response("course instance is not started", status=500)
    response = requests.get('http://%s:%s/private/course' % (config.HOST, course_iid))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/course/<cid>', methods=['PUT'])
def update_course(cid):
    logging.info("receive a update_course request")
    if not course_iid:
        return Response("course instance is not started", status=500)
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    conn = httplib.HTTPConnection('%s:%s' % (config.HOST, course_iid))
    conn.request("PUT", "/private/course/%s/" % cid, json.dumps(sanitized_data), json_headers)
    return str(conn.getresponse().read())
    # return str(requests.put('http://%s:%s/private/course/%s' % (config.HOST, course_iid, cid)).status_code)


@app.route('/public/course/<cid>', methods=['DELETE'])
def delete_course(cid):
    logging.info("receive a delete_course request")
    if not course_iid:
        return Response("course instance is not started", status=500)
    conn = httplib.HTTPConnection('%s:%s' % (config.HOST, course_iid))
    # logging.info(type(request.headers))
    header = {'If-Match': request.headers.get('If-Match')}
    conn.request("DELETE", "/private/course/%s/" % cid, "", header)
    return str(conn.getresponse().read())
    # return str(requests.delete('http://%s:%s/private/course/%s' % (config.HOST, course_iid, cid), headers=request.headers).status_code)


"""data definition api for course"""


@app.route('/public/course/schema', methods=['POST'])
def create_new_column_for_course_schema():
    logging.info("receive a create_new_column_for_course_schema request")
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    if not course_iid:
        return Response("course instance is not started", status=500)
    response = requests.post("http://%s:%s/private/course/schema" % (config.HOST, course_iid), headers=json_headers, data=json.dumps(sanitized_data))
    return Response(response.content, mimetype='application/json', status=response.status_code)
    # return str(requests.post("http://%s:%s/private/course/schema" % (config.HOST, course_iid), headers=json_headers, data=json.dumps(sanitized_data)).status_code)


@app.route('/public/course/schema', methods=['GET'])
def retrive_course_schema():
    logging.info("receive a retrive_course_schema request")
    if not course_iid:
        return Response("course instance is not started", status=500)
    response = requests.get("http://%s:%s/private/course/schema" % (config.HOST, course_iid))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/course/schema', methods=['PUT'])
def update_column_of_course_schema():
    logging.info("receive a update_column_of_course_schema request")
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    if not course_iid:
        return Response("course instance is not started", status=500)
    response = requests.put("http://%s:%s/private/course/schema" % (config.HOST, course_iid), headers=json_headers, data=json.dumps(sanitized_data))
    return Response(response.content, mimetype='application/json', status=response.status_code)
    # return str(requests.put("http://%s:%s/private/course/schema" % (config.HOST, course_iid), headers=json_headers, data=json.dumps(sanitized_data)).status_code)


@app.route('/public/course/schema', methods=['DELETE'])
def delete_column_of_course_schema():
    logging.info("receive a delete_column_of_course_schema request")
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    if not course_iid:
        return Response("course instance is not started", status=500)
    response = requests.delete("http://%s:%s/private/course/schema" % (config.HOST, course_iid), headers=json_headers, data=json.dumps(sanitized_data))
    return Response(response.content, mimetype='application/json', status=response.status_code)


"""data manipulation api for registration"""


@app.route('/public/registration', methods=['POST'])
def create_registration():
    logging.info("receive a create_registration request")
    if not registration_iid:  # iid is port
        return Response("registration instance is not started", status=500)
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    response = requests.post('http://%s:%s/private/registration' % (config.HOST, registration_iid), headers=json_headers, data=json.dumps(sanitized_data))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/registration', methods=['GET'])
def retrive_all_registration():
    logging.info("receive a retrive_all_registration request")
    if not registration_iid:  # iid is port
        return Response("registration instance is not started", status=500)
    response = requests.get('http://%s:%s/private/registration' % (config.HOST, registration_iid))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/registration/uni/<uni>', methods=['GET'])
def retrive_registration_from_uni(uni):
    logging.info("receive a retrive_registration_from_uni request")
    if not registration_iid:  # iid is port
        return Response("registration instance is not started", status=500)
    response = requests.get('http://%s:%s/private/registration/uni/%s' % (config.HOST, registration_iid, uni))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/registration/courseid/<courseid>', methods=['GET'])
def retrive_registration_from_courseid(courseid):
    logging.info("receive a retrive_registration_from_courseid request")
    if not registration_iid:  # iid is port
        return Response("registration instance is not started", status=500)
    response = requests.get('http://%s:%s/private/registration/courseid/%s' % (config.HOST, registration_iid, courseid))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/registration/uni/<uni>/courseid/<cid>', methods=['PUT'])
def update_registration(uni, cid):
    logging.info("receive a update_registration request")
    if not registration_iid:  # iid is port
        return Response("registration instance is not started", status=500)
    original_json = request.get_json()
    try:
        # for security reason (optional)
        sanitized_data = getSanitizedJson(original_json)
    except Exception, e:
        return Response("request contains illegal data", status=400)
    conn = httplib.HTTPConnection('%s:%s' % (config.HOST, registration_iid))
    conn.request("PUT", "/private/registration/uni/%s/courseid/%s" % (uni, cid), json.dumps(sanitized_data), json_headers)
    return str(conn.getresponse().read())
    # return str(requests.put('http://%s:%s/private/registration/uni/%s/courseid/%s' % (config.HOST, registration_iid, uni, cid)).status_code)


@app.route('/public/registration/uni/<uni>', methods=['DELETE'])
def delete_registration_from_uni(uni):
    logging.info("receive a delete_registration_from_uni request")
    if not registration_iid:  # iid is port
        return Response("registration instance is not started", status=500)
    response = requests.delete('http://%s:%s/private/registration/uni/%s' % (config.HOST, registration_iid, uni))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/registration/courseid/<courseid>', methods=['DELETE'])
def delete_registration_from_courseid(courseid):
    logging.info("receive a delete_registration_from_courseid request")
    if not registration_iid:  # iid is port
        return Response("registration instance is not started", status=500)
    response = requests.delete('http://%s:%s/private/registration/courseid/%s' % (config.HOST, registration_iid, courseid))
    return Response(response.content, mimetype='application/json', status=response.status_code)


@app.route('/public/registration/uni/<uni>/courseid/<cid>', methods = ['DELETE'])
@app.route('/public/registration/courseid/<cid>/uni/<uni>', methods = ['DELETE'])
def delete_registration_from_courseid_and_uni(uni, cid):
    logging.info("receive a delete_registration_from_courseid_and_uni request")
    if not registration_iid:  # iid is port
        return Response("registration instance is not started", status=500)
    response = requests.delete('http://%s:%s/private/registration/uni/%s/courseid/%s' % (config.HOST, registration_iid, uni, cid))
    return Response(response.content, mimetype='application/json', status=response.status_code)



"""api for creating new microservice instance"""
# TODO: store the instance pid into db in case of failure of router process


@app.route('/public/instance/<instanceType>', methods=['POST'])
@app.route('/public/instance/<instanceType>/<shard_number>', methods=['POST'])
def create_instance(instanceType, shard_number = -1):
    try:
        port = str(config.PORT_POOL.pop())  # port is also the instance id
        code_path = None
        if instanceType == "student":
            code_path = config.STUDENT_CODE_PATH
        if instanceType == "course":
            code_path = config.COURSE_CODE_PATH
            global course_iid
            course_iid = port
        if instanceType == "registration":
            code_path = config.REGISTRATION_CODE_PATH
            global registration_iid
            registration_iid = port
        if instanceType == "student":  # map shard number with host:port
            if shard_number < 0:
                return "illegal shard_number!"
            if shard_number in student_shard_table:
                return "Shard %s has already been started!" % shard_number
            global current_number_of_shards
            if current_number_of_shards>=config.NUMBER_OF_SHARD:
                return "reach the max of shards"
            student_shard_table[str(shard_number)] = (config.HOST, port)
            current_number_of_shards += 1
        subp = subprocess.Popen(['python',
                                 code_path,
                                 str(config.HOST),
                                 str(port),
                                 str(shard_number)],
                                stdout=DEVNULL, stderr=DEVNULL)
        instance_info_table[port] = (instanceType, subp)
        this_instance = {"instanceId": port, "instanceType": instanceType,
                         "host": config.HOST, "port": port}
        mongo.project1.instance_info.insert_one(this_instance)
        
    except Exception, e:
        logging.error(e)
        return Response("error in creating a new %s instance"%instanceType, status=500)
    # succeed
    return Response("succeed creating a new %s instance"%instanceType, status=201)

"""delete any microservice instance"""


@app.route('/public/instance/<iid>', methods=['DELETE'])
def delete_instance(iid):  # port is also the instance id
    try:
        instanceType, subp = instance_info_table[iid]
        requests.delete('http://%s:%s/private/instance/%s' % (config.HOST, iid, instanceType))  # kill eve
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
    except Exception, e:
        logging.error(e)
        return Response("error in stopping %s instance %s" % (instanceType, iid), status=500)
    return Response("succeed stopping %s instance %s" % (instanceType, iid), status=201)  # succeed

"""util functions"""


def uni_hash(uni):
    return str(uni.__hash__() % config.NUMBER_OF_SHARD)


def getSanitizedJson(original_json):
    """used for security check (incomplete)"""
    return original_json

def init():
    mongo.project1.drop_collection('instance_info')

if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0')

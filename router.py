# -*- coding: utf-8 -*-
"""
data API
"""
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import requests
import logging
from settings import NUMBER_OF_SHARD, LOG_FILENAME

app = Flask(__name__)
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,format='%(asctime)s --- %(message)s')

@app.route('/public/student', methods=['POST'])
def create_student():
    logging.info("receive a create_student request")
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    shard_index = uni_hash(uni)
    return requests.post('/private/student/shard/%d'%shard_index, json=sanitized_data).status_code

@app.route('/public/student/<uni>', methods=['GET'])
def retrive_student(uni):
    logging.info("receive a retrive_student request")
    shard_index = uni_hash(uni)
    return requests.get('/private/student/shard/%d/uni/%s'%(shard_index,uni)).content

@app.route('/public/student/<uni>', methods=['PUT'])
def update_student(uni):
    logging.info("receive a update_student request")
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    shard_index = uni_hash(uni)
    return requests.put('/private/student/shard/%d/uni/%s'%(shard_index,uni), json=sanitized_data).status_code

@app.route('/public/student/<uni>', methods=['DELETE'])
def delete_student(uni):
    logging.info("receive a delete_student request")
    shard_index = uni_hash(uni)
    return requests.delete('/private/student/shard/%d/uni/%s'%(shard_index,uni)).status_code


@app.route('/public/course', methods=['POST'])
def create_course():
    logging.info("receive a create_course request")
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    return requests.post('/private/course', json=sanitized_data).status_code

@app.route('/public/course/<cid>', methods=['GET'])
def retrive_course(cid):
    logging.info("receive a retrive_course request")
    return requests.get('/private/course/%s'%cid).content

@app.route('/public/course/<cid>', methods=['PUT'])
def update_course(cid):
    logging.info("receive a update_course request")
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    return requests.put('/private/course/%s'%cid).status_code

@app.route('/public/course/<cid>', methods=['DELETE'])
def delete_course(cid):
    logging.info("receive a delete_course request")
    return requests.delete('/private/course/%s'%cid).status_code


@app.route('/public/registration/<rid>', methods=['POST'])
def create_registration(rid):
    logging.info("receive a create_registration request")
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    return requests.post('/private/registration', json=sanitized_data).status_code

@app.route('/public/registration/<rid>', methods=['GET'])
def retrive_registration(rid):
    logging.info("receive a retrive_registration request")
    return requests.get('/private/registration/%s'%cid).content

@app.route('/public/registration/<rid>', methods=['PUT'])
def update_registration(rid):
    logging.info("receive a update_registration request")
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    return requests.put('/private/registration/%s'%cid).status_code

@app.route('/public/registration/<rid>', methods=['DELETE'])
def delete_registration(rid):
    logging.info("receive a delete_registration request")
    return requests.delete('/private/course/%s'%cid).status_code

def uni_hash(uni):
    return uni.__hash__()%NUMBER_OF_SHARD

def getSanitizedJson(original_json):
    """
    used for security check (incomplete)
    """
    return original_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
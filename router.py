# -*- coding: utf-8 -*-
"""
data API
"""
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import requests
from settings import NUMBER_OF_SHARD

app = Flask(__name__)

@app.route('/public/student', methods=['POST'])
def create_student():
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    shard_index = uni_hash(uni)
    return requests.post('/private/student/shard/%d'%shard_index, json=sanitized_data).status_code

@app.route('/public/student/<uni>', methods=['GET'])
def retrive_student(uni):
    shard_index = uni_hash(uni)
    return requests.get('/private/student/shard/%d/uni/%s'%(shard_index,uni)).content

@app.route('/public/student/<uni>', methods=['PUT'])
def update_student(uni):
    original_json = request.get_json()
    try:
        sanitized_data = getSanitizedJson(original_json)  # for security reason (optional)
    except Exception, e:
        return "invalid request"
    shard_index = uni_hash(uni)
    return requests.put('/private/student/shard/%d/uni/%s'%(shard_index,uni), json=sanitized_data).status_code

@app.route('/public/student/<uni>', methods=['DELETE'])
def delete_student(uni):
    shard_index = uni_hash(uni)
    return requests.delete('/private/student/shard/%d/uni/%s'%(shard_index,uni)).status_code


@app.route('/public/course/<cid>', methods=['POST'])
def create_course(cid):
    return "create_course: "+str(cid)

@app.route('/public/course/<cid>', methods=['GET'])
def retrive_course(cid):
    return "retrive_course: "+str(cid)

@app.route('/public/course/<cid>', methods=['PUT'])
def update_course(cid):
    return "update_course: "+str(cid)

@app.route('/public/course/<cid>', methods=['DELETE'])
def delete_course(cid):
    return "delete_course: "+str(cid)


@app.route('/public/registration/<rid>', methods=['POST'])
def create_registration(rid):
    return "create_registration: "+str(rid)

@app.route('/public/registration/<rid>', methods=['GET'])
def retrive_registration(rid):
    return "retrive_registration: "+str(rid)

@app.route('/public/registration/<rid>', methods=['PUT'])
def update_registration(rid):
    return "update_registration: "+str(rid)

@app.route('/public/registration/<rid>', methods=['DELETE'])
def delete_registration(rid):
    return "delete_registration: "+str(rid)

def uni_hash(uni):
    return uni.__hash__()%NUMBER_OF_SHARD

def getSanitizedJson(original_json):
    """
    used for security check
    """
    return original_json

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
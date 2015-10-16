# -*- coding: utf-8 -*-
"""
data API
"""
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify

app = Flask(__name__)

@app.route('/public/student/<uni>', methods=['POST'])
def create_student(uni):
    return "create_student: "+str(uni)

@app.route('/public/student/<uni>', methods=['GET'])
def retrive_student(uni):
    return "retrive_student: "+str(uni)

@app.route('/public/student/<uni>', methods=['PUT'])
def update_student(uni):
    return "update_student: "+str(uni)

@app.route('/public/student/<uni>', methods=['DELETE'])
def delete_student(uni):
    return "delete_student: "+str(uni)


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
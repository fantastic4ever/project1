# -*- coding: utf-8 -*-
"""
data API
"""
from flask import render_template, request, flash, redirect, url_for, jsonify


@app.route('/public/student/<uni>', methods=['POST'])
def create_student(uni):
    pass

@app.route('/public/student/<uni>', methods=['GET'])
def retrive_student(uni):
    pass

@app.route('/public/student/<uni>', methods=['PUT'])
def update_student(uni):
    pass

@app.route('/public/student/<uni>', methods=['DELETE'])
def delete_student(uni):
    pass


@app.route('/public/course/<cid>', methods=['POST'])
def create_course(cid):
    pass

@app.route('/public/course/<cid>', methods=['GET'])
def retrive_course(cid):
    pass

@app.route('/public/course/<cid>', methods=['PUT'])
def update_course(cid):
    pass

@app.route('/public/course/<cid>', methods=['DELETE'])
def delete_course(cid):
    pass


@app.route('/public/registration/<rid>', methods=['POST'])
def create_registration(rid):
    pass

@app.route('/public/registration/<rid>', methods=['GET'])
def retrive_registration(rid):
    pass

@app.route('/public/registration/<rid>', methods=['PUT'])
def update_registration(rid):
    pass

@app.route('/public/registration/<rid>', methods=['DELETE'])
def delete_registration(rid):
    pass
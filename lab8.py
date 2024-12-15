from flask import Blueprint, render_template, request, session, jsonify, redirect

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def lab8_index():
    return render_template('lab8/index.html')

@lab8.route('/lab8/login/')
def login():
    return render_template('lab8/login.html')

@lab8.route('/lab8/register/')
def register():
    return render_template('lab8/register.html')

@lab8.route('/lab8/articles')
def articles():
    return render_template('lab8/articles')

@lab8.route('/lab8/create')
def create():
    return render_template('lab8/create.html')
from flask import render_template, flash, redirect, url_for, request
from app import app,db

from app.forms import ClassForm
from app.models import Class

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title="Course List")
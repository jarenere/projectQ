# -*- coding: utf-8 -*-
from app import app
from flask import render_template
from config import basedir
    
@app.route('/')
@app.route('/index')
def index():
    f = open(basedir+"/app/static/index.re", "r")
    text =  f.read()
    return render_template('index.html', text = text)

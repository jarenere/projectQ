# -*- coding: utf-8 -*-
# from app import app
from flask import render_template
from config import basedir
from . import blueprint

    
@blueprint.route('/')
@blueprint.route('/index')
def index():
    f = open(basedir+"/app/static/index.re", "r")
    text =  f.read()
    f.close()
    return render_template('index.html', text = text)

@blueprint.route('/pruebas')
def pruebas():
    return render_template('pruebas.html')

#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__create__ = '2015/1/4'

from flask import Blueprint, render_template

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    return render_template('index.html')
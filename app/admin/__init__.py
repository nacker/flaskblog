__author__ = 'nacker'


from flask import Blueprint
admin = Blueprint("admin",__name__)

import app.admin.views
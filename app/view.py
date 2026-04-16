from flask import Blueprint, json, render_template,redirect,session,url_for,request
from .fog import message_callback
routes = Blueprint('routes', __name__)

@routes.route('/',methods=["GET", "POST"])
def dashboard(): 
      message_callback()
      return render_template("dashboard.html")
    
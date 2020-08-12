from flask import ( 
    Flask, url_for, render_template, json, request, redirect, Blueprint, flash, g
)
from werkzeug.exceptions import abort 
from datetime import datetime
# from assetManager.forms import PostForm #flask forms 
# from bs4 import BeautifulSoup as bs #HTML Parsing
from flask_sqlalchemy import SQLAlchemy 
from flask import current_app, g

from assetManager.schema import User
from assetManager.database import get_db 
from flask_user import current_user, login_required, roles_required
from . import file_upload
from .uploadFunctions import upload_image  

bp = Blueprint("assetManager", __name__)

@bp.route("/", methods=["GET"])
def index(name=None): 
    return render_template('index.html')
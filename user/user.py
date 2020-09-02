from flask import ( 
    Flask, url_for, render_template, json, request, redirect, Blueprint, flash, g
)
from werkzeug.exceptions import abort 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask import current_app, g

from assetManager.schema import User
from assetManager.database import get_db 
from flask_user import current_user, login_required, roles_required
from . import file_upload
from .uploadFunctions import upload_image  
import pyqrcode

import os
import time 
from cryptography.hazmat.primitives.twofactor.totp import TOTP
from cryptography.hazmat.primitives.hashes import SHA256

user = Blueprint("user", __name__)

@user.route("/AllUsers", methods=["GET"])
@roles_required(['Editor'])
def index(name=None): 
    return render_template('index.html')

@user.route("/twofactor")
@roles_required(['Editor'])
def setup_two_factor(name=None):
    #Get user secret 
    user = User.query.filter_by(username=current_user.username).first()
    print(user)
    #256 bits
    key = os.urandom(32)
    user.totp_secret = key 
    #use SHA256 encryption method
    totp = TOTP(key, 8, SHA256(), 30)
    time_value = time.time()
    totp_value = totp.generate(time_value)

    #update database 
    db.session.add(user)
    db.session.commit()
    
    #render qrcode 
    url = pyqrcode.create(totp.get_provisioning_uri(current_user.username + "@assetManager", "assetManager"))
    
    return render_template('two-factor-setup.html', url=url.svg('qrcode.svg', scale=8))


from flask import ( 
    Flask, url_for, render_template, json, request, redirect, Blueprint, flash, g
)
from werkzeug.exceptions import abort 
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask import current_app, g

from .schema import User
from assetManager.home.database import get_db 
from flask_user import current_user, login_required, roles_required
import pyqrcode
import io 

user_bp = Blueprint("user_bp", __name__, template_folder='templates')

@user_bp.route("/twofactor")
def setup_two_factor(name=None):
    return render_template(
        'two-factor-setup.html', 
        title='Two Factor Authentication', 
        qrcode='/qrcode')

@user_bp.route("/qrcode")
def qrcode(name=None):
    #render qrcode 
    url = pyqrcode.create(current_user.get_totp_uri())
    buffer = io.BytesIO()
    url.svg(buffer, scale=5)
    return buffer.getvalue(), 200, {
        'Content-Type': 'image/svg+xml', 
        'Cache-Control': 'no-cache, no-store, must-revalidate', 
        'Pragma': 'no-cache', 
        'Expires': '0'
    }


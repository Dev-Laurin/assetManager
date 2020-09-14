from flask_sqlalchemy import SQLAlchemy
import click  
from flask import current_app, g
from flask.cli import with_appcontext
from assetManager import db 

def get_db(): 
	with current_app.app_context(): 
		return db 

def close_db(e=None):
	db = g.pop('db', None)

	if db is not None: 
		db.session.close()

def init_db():
	db = get_db()
	import assetManager.schema 
	db.create_all()
	db.session.commit()

def init_app(app):
	app.teardown_appcontext(close_db)
	init_db()
from werkzeug.security import generate_password_hash, check_password_hash
from assetManager.database import get_db
from datetime import datetime 
from flask_user import UserMixin

db = get_db()
from . import file_upload

class User(UserMixin, db.Model):
	def __str__(self):
		return self.username 

	id = db.Column(db.Integer, primary_key=True)
	active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

	username = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(200), primary_key=False,
		unique=False, nullable=False)

	def set_password(self, password):
		self.password = generate_password_hash(password, 
			method='sha256')

	def check_password(self, password):
		return check_password_hash(self.password, password)

	roles = db.relationship('Role', secondary='user_roles')

class Role(db.Model):
	def __str__(self):
		return self.name 
		
	__tablename__ = 'role'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique=True)

class UserRoles(db.Model):
	__tablename__ = 'user_roles'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
	role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))

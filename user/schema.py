from werkzeug.security import generate_password_hash, check_password_hash
from assetManager.database import get_db
from datetime import datetime 
from flask_user import UserMixin, UserManager

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
	totp_secret = db.Column(db.String(32), nullable=False)

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

#Customize Login Form for Two Factor Auth
from flask_user.forms import LoginForm 
class CustomLoginForm(LoginForm):
	#Add the one time password field 
	code = PasswordField('password', validators=[InputRequired(), Length(min=6, max=8)])

class CustomUserManager(UserManager):

	#Extend the default login view method to include 2FA
	def login_view(self):
		"""Prepare and process the login form."""

        # Authenticate username/email and login authenticated users.

        safe_next_url = self._get_safe_next_url('next', self.USER_AFTER_LOGIN_ENDPOINT)
        safe_reg_next = self._get_safe_next_url('reg_next', self.USER_AFTER_REGISTER_ENDPOINT)

        # Immediately redirect already logged in users
        if self.call_or_get(current_user.is_authenticated) and self.USER_AUTO_LOGIN_AT_LOGIN:
            return redirect(safe_next_url)

        # Initialize form
        login_form = self.LoginFormClass(request.form)  # for login.html
        register_form = self.RegisterFormClass()  # for login_or_register.html
        if request.method != 'POST':
            login_form.next.data = register_form.next.data = safe_next_url
            login_form.reg_next.data = register_form.reg_next.data = safe_reg_next

        # Process valid POST
        if request.method == 'POST' and login_form.validate():
            # Retrieve User
            user = None
            user_email = None
            if self.USER_ENABLE_USERNAME:
                # Find user record by username
                user = self.db_manager.find_user_by_username(login_form.username.data)

                # Find user record by email (with form.username)
                if not user and self.USER_ENABLE_EMAIL:
                    user, user_email = self.db_manager.get_user_and_user_email_by_email(login_form.username.data)
            else:
                # Find user by email (with form.email)
                user, user_email = self.db_manager.get_user_and_user_email_by_email(login_form.email.data)

            if user:
				########################CUSTOM 2FA########################
				#Validate 2FA
				user_input_code = login_form.code 
				#use SHA256 encryption method
				totp = TOTP(key, 8, SHA256(), 30)
				time_value = time.time()

				try: 
					totp.verify(user_input_code, time_value)
					#########################End#########################
					# Log user in
					safe_next_url = self.make_safe_url(login_form.next.data)
					return self._do_login_user(user, safe_next_url, login_form.remember_me.data)
					#########################Custom#######################
				except Exception as e: 
					flash('Invalid code.')

				###########################End############################

                
        # Render form
        self.prepare_domain_translations()
        template_filename = self.USER_LOGIN_AUTH0_TEMPLATE if self.USER_ENABLE_AUTH0 else self.USER_LOGIN_TEMPLATE
        return render_template(template_filename,
                      form=login_form,
                      login_form=login_form,
                      register_form=register_form)
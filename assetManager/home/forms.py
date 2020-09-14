from flask_wtf import FlaskForm
from wtforms import (Form, StringField, BooleanField, 
	TextAreaField, validators, widgets, 
	SelectMultipleField, PasswordField
	)
from wtforms.validators import DataRequired, Length, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
# from flask_uploads import (UploadSet, 
# 	configure_uploads, IMAGES, TEXT, 
# 	DOCUMENTS, patch_request_class
# )
# images = UploadSet('images', IMAGES)

class LoginForm(FlaskForm):
	username = StringField('username', validators=[DataRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
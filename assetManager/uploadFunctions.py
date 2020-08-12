#uploadFunctions.py
import re #substring search
import uuid #Filename random generator
import base64 #base64 image decoding 
import os 
from flask import current_app, g
from werkzeug.utils import secure_filename

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(base64String):
	extension = re.search('/(.*);', base64String)
	filename = str(uuid.uuid4()) + "." + str(extension.group(1))
	src = os.path.join(current_app.config['UPLOAD_FOLDER_MANUAL'], secure_filename(filename))
	base64String = base64String.split(',')[1]
	fh = open(src, "wb")
	fh.write(base64.b64decode(base64String.encode()))
	fh.close()
	src = os.path.join(current_app.config['UPLOADED_IMAGES_DEST'], secure_filename(filename))
	return src 

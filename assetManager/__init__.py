from flask import (
    Flask, url_for, render_template, json, request, 
    redirect
)
from flask_file_upload import FileUpload 
from flask_user import UserManager, roles_required, current_user
import os 
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
file_upload = FileUpload(db=db)
from flask_mail import Mail 
mail = Mail()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .home import database 
    with app.app_context():
        db.init_app(app)
        
        from .user.schema import User
         #uploads
        file_upload.init_app(app, db)   
        user_manager = UserManager(app, db, User)

        #Email
        mail.init_app(app)

        #uploads
        # from flask_uploads import (UploadSet, 
        #     configure_uploads, IMAGES, 
        #     DOCUMENTS, patch_request_class
        # )

        # images = UploadSet('images', IMAGES)
        # documents = UploadSet('documents', DOCUMENTS)
        # configure_uploads(app, (images, documents))
        # patch_request_class(app, 50 * 1024 * 1024) #50 MB max file upload

        # ALLOWED_EXTENSIONS = images
        dev_db(user_manager)

    from .user import user
    from .home import assetManager 
    app.register_blueprint(assetManager.am)
    app.register_blueprint(user.user_bp)

    app.add_url_rule("/", endpoint='index')

    return app 

def dev_db(user_manager):
    db.drop_all()
    db.create_all()

    from .user.schema import Role 
    #create User Roles 
    admin = Role(name='Admin')
    user = Role(name='User')

    db.session.add(admin)
    db.session.add(user)
    db.session.commit()



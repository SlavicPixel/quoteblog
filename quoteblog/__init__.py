import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a14ca7f30abdb6b81e94e8866d205738'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME']= 'divosic98@gmail.com'              # os.environ.get['EMAIL_USER')
app.config['MAIL_PASSWORD'] = 'xfztleumgsmmucrf'                 # os.environ.get('EMAIL_PASS')
mail = Mail(app)

from quoteblog import routes
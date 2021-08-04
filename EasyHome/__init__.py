

from flask import Flask
__author__ = 'ibininja'

from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)

from EasyHome import route
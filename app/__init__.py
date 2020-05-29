from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config


configuration = Config()
app = Flask(__name__)
configuration.set_config(app)
db = SQLAlchemy(app)
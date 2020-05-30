import os
from flask_wtf.csrf import CSRFProtect

class Config:
    """Class to configure Flask app."""

    def __init__(self):  # Temporary configuration
        """Adding the database URI as a environment variable."""
        os.environ['DATABASE_URL'] = "sqlite:///remoteja.db"

    def set_config(self, app):
        """Set the config for the Flask app."""
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///remoteja.db"
        app.config['SQL_ALCHEMY_ECHO'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
       # csrf = CSRFProtect(app)
       # csrf.init_app(app)

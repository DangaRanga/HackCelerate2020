import os


class Config:
    """Class to configure Flask app."""

    def __init__(self):  # Temporary configuration
        """Adding the database URI as a environment variable."""
        os.environ['DATABASE_URL'] = "sqlite:///remoteja.db"

    def set_config(self, app):
        """Set the config for the Flask app."""
        secret_key = os.urandom(64)
        sqlalchemy_database_uri = os.environ['DATABASE_URL']
        app.config['SECRET_KEY'] = secret_key
        app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_database_uri
        app.config['SQL_ALCHEMY_ECHO'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

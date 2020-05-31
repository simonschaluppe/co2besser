from enum import Enum

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

@app.teardown_appcontext
def shutdown_session(exception=None):
    # database.data.delete()
    db.session.remove()

from app.models import Action, Comparison



# routes
from app import routes

bootstrap = Bootstrap(app)


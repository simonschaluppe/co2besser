
from random import sample

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app.models import Action, Comparison

@app.teardown_appcontext
def shutdown_session(exception=None):
    # database.data.delete()
    db.session.remove()


# not quite sure where this is supposed to go
def reset_guess():
    if Action.query.all():
        app.action1, app.action2 = sample(Action.query.all(), 2)
    else:
        app.action1, app.action2 = None, None
    app.guess = None
    app.correct = max(app.action1, app.action2)

# routes
from app import routes

bootstrap = Bootstrap(app)



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


try:
    q = Action.query.all()
    def reset_guess():
        app.action1, app.action2 = sample(q, 2)
        app.guess = None
        app.correct = max(app.action1, app.action2)
except:
    raise Exception


# routes
from app import routes

bootstrap = Bootstrap(app)


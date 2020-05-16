from flask import Flask
from flask_bootstrap import Bootstrap
from random import sample

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
from app.database import init_db, db_session

init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    # database.data.delete()
    db_session.remove()


from app.models import Action

# add testactions

# for i in range(1, 11):
#     action = Action(id=i, name="var" + str(i),
#                     description="text" * i,
#                     savings=0.2 * i - 5,
#                     source="https://www.zwei-grad-eine-tonne.at/")
#
#     db_session.add(action)
#     db_session.commit()
#

app.a1, app.a2 = sample(database.data.all()[1:], 2)

# routes
from app import routes

if __name__ == '__main__':
    # print("lol")
    # app.run()
    a = app.database.data

bootstrap = Bootstrap(app)
from enum import Enum

from flask import Flask
from flask_bootstrap import Bootstrap
from random import sample
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.teardown_appcontext
def shutdown_session(exception=None):
    # database.data.delete()
    db.session.remove()


from app.models import Action

def reset_guess():
    app.action1, app.action2 = sample(Action.query.all(), 2)
    app.guess = None
    app.correct = min(app.action1, app.action2)

reset_guess()

# routes
from app import routes

bootstrap = Bootstrap(app)


def add_drexel_to_db():
    import csv
    with open("static/data/food.csv", encoding="utf-8", newline='') as f:
        freader = csv.DictReader(f, delimiter="\t")
        # for line in freader:
        #     print(line["Lebensmittel"], line["CO2-Äquivalent in kg pro Person und Jahr"])
        all = []
        food = {}  # keys = kategorien, vals = list of foods
        i, j = 0, 0
        for line in freader:
            all.append(line)
            i += 1
            if "Summe" in line["Lebensmittel"]:
                cat = line["Lebensmittel"][6:]
                food[cat] = all[j:i - 1]
                j = i
                print(cat)
                print(food[cat])

    # Beginnen wir damit, für das Feld "Ernährung" je Kategorie eine Maßnahme
    # pro Reduktionsniveau zu definieren:
    REDUCTIONS = {
        "30%": 0.7,
        "50%": 0.5,
        "75": 0.25,
        "90%": 0.1,
        "100%": 0.0,
    }

    for cat in food.keys():
        for reduction in REDUCTIONS:
            co2standard = sum([float(savings["CO2-Äquivalent in kg pro Person und Jahr"]) for savings in food[cat]])
            savings = round(co2standard * (1 - REDUCTIONS[reduction]), 4)

            action_dict = {
                "name": "".join([cat, " -", reduction]),
                "sector": "Ernährung",
                "category": cat,
                "savings": savings,
                "reduction_factor": REDUCTIONS[reduction],
                "description": f"Ernähringsstil: {cat} um {reduction} im Vergleich zum Durchschnitt reduzieren",
                "solution_text": f"Führt im Vergleich zum durchschnittlichen Ernährungsstil zu " \
                                 f"Einsparungen von {savings} kg CO2eq pro Jahr",
                "reference": "https://www.zwei-grad-eine-tonne.at/hintergrund-berechnungen/abschnitt-i-lustvoll-die"
                             "-welt-retten"
            }

            b = Action(**action_dict)
            db.session.add(b)
            print(b)


def delete_table(table):
    for item in table.query.all():
        db.session.delete(item)
    if input(f"Confirm deleting table '{table.__tablename__}' [y/n]? ").upper() == "Y":
        db.session.commit()
    else:
        print("rolling back changes")
        db.session.rollback()

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
    app.correct = max(app.action1, app.action2)

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
        "75%": 0.25,
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
                "description": f"Ernährungsstil: {cat} um {reduction} im Vergleich zum Durchschnitt reduzieren",
                "solution_text": f"Führt im Vergleich zum durchschnittlichen Ernährungsstil zu " \
                                 f"Einsparungen von {savings} kg CO2eq pro Jahr",
                "reference": "https://www.zwei-grad-eine-tonne.at/hintergrund-berechnungen/abschnitt-i-lustvoll-die"
                             "-welt-retten"
            }

            b = Action(**action_dict)
            db.session.add(b)
            print(b)

    action_dict = {
        "name": "Flexitarier, konventionell",
        "sector": "Ernährung",
        "category": "Gemischt",
        "description": "Zweimal pro Woche Fleisch oder Fisch, durchschnittliche Mengen an Wurtsprodukten, Milchprodukten, Obst und Gemüse.",
        "savings": 300.0,
        "reduction_factor": 300/1800,
        "solution_text": f"Führt im Vergleich zum durchschnittlichen Ernährungsstil zu Einsparungen von 300 kg CO2eq pro Jahr",
        "reference": "https://www.zwei-grad-eine-tonne.at/hintergrund-berechnungen/abschnitt-i-lustvoll-die"
                             "-welt-retten"
        }

    rm1 = Action(**action_dict)
    db.session.add(rm1)
    print(rm1)
    # %%

    drexel_dict = {
        "name": "Bio-Flexitarier",
        "sector": "Ernährung",
        "category": "Gemischt",
        "description": " ".join([action_dict["description"], "Wann immer möglich regional und bio."]),
        "savings": 1800.0 - 1100,
        "reduction_factor": (1800.0 - 1100)/1800,
        "solution_text": f"Führt im Vergleich zum durchschnittlichen Ernährungsstil zu Einsparungen von 300 kg CO2eq pro Jahr",
        "reference": "https://www.zwei-grad-eine-tonne.at/hintergrund-berechnungen/abschnitt-i-lustvoll-die"
    }
    rm2 = Action(**drexel_dict)
    db.session.add(rm2)
    print(rm2)

    with open("static/data/Abschnitt%20I%20Verkehr.csv", encoding="utf-8", newline='') as f:
        freader = csv.DictReader(f, delimiter=",")
        # for line in freader:
        #     print(line["Lebensmittel"], line["CO2-Äquivalent in kg pro Person und Jahr"])
        all = [] # keys = kategorien, vals = list of foods
        i, j = 0, 0
        for line in freader:
            if line["Verhalten"] != "":
                all.append(line)

    verkehrstile = []
    sector = "Verkehr"
    for dicts in all:
        if dicts["Fahrzweck"] == "Summe":
            savings = 1.5177 * 1000 - float(dicts["CO2-Emission gesamt in Tonnen pro Person"]) * 1000
            name = "".join([sector, ": ", dicts["Verhalten"]])
            action_dict = {
                "name": name,
                "sector": sector,
                "category": "Gemischt",
                "description": name,
                "savings": savings,
                "reduction_factor": savings / (1.5177 * 1000),
                "solution_text": f"Führt im Vergleich zum durchschnittlichen Verkehrsverhalten zu Einsparungen von {savings} kg CO2eq pro Jahr",
                "reference": "https://www.zwei-grad-eine-tonne.at/hintergrund-berechnungen/abschnitt-i-lustvoll-die"
                             "-welt-retten"
            }

            b = Action(**action_dict)
            db.session.add(b)


def delete_table(table):
    for item in table.query.all():
        db.session.delete(item)
    if input(f"Confirm deleting table '{table.__tablename__}' [y/n]? ").upper() == "Y":
        db.session.commit()
    else:
        print("rolling back changes")
        db.session.rollback()

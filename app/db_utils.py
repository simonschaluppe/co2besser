import openpyxl

from app import db, app
from app.models import Action, Emission
from app.log import configure_logger

import xlwings as xw

LOG_FORMAT = '%(levelname)-8s | %(asctime)s | %(filename)-12s | %(message)s'
LOG_TO_FILE = False
LOG_TO_CONSOLE = False
LOG_FILE_PATH = "logs\ls.log"

logger = configure_logger()
logger.info(f"entering {__name__}...")


def populate_emissions_table():
    pass


def add_food_emissions():
    import csv
    with open("app/static/data/food.csv", encoding="utf-8", newline='') as f:
        freader = csv.DictReader(f, delimiter="\t")
        # for line in freader:
        #     logger.info(line["Lebensmittel"], line["CO2-Äquivalent in kg pro Person und Jahr"])
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
                logger.debug(f"{cat}: {food[cat]}")

    for cat in food.keys():
        emissions = sum([float(savings["CO2-Äquivalent in kg pro Person und Jahr"]) for savings in food[cat]])
        emission_dict = {
            "name": "".join([cat, " Durchschnittskonsum"]),
            "sector": "Ernährung",
            "category": cat,
            "emissions": emissions,
            "description": "\n".join(["".join([item["Lebensmittel"], ": ",
                                               item["Konsum in kg/Monat"], " kg/Monat"])
                                      for item in food[cat]]),
            "reference": "https://www.zwei-grad-eine-tonne.at/hintergrund-berechnungen/abschnitt-i-lustvoll-die"
                         "-welt-retten"
        }

        b = Emission(**emission_dict)
        db.session.add(b)
        logger.info(f"db.session.add({b})")

    if input(f"Commit to db? [y/n]? ").upper() == "Y":
        db.session.commit()
        logger.info(f"db.session.commit()")


def add_drexel_to_db():
    import csv
    with open("static/data/food.csv", encoding="utf-8", newline='') as f:
        freader = csv.DictReader(f, delimiter="\t")
        # for line in freader:
        #     logger.info(line["Lebensmittel"], line["CO2-Äquivalent in kg pro Person und Jahr"]))
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
                logger.debug(f"{cat}: {food[cat]}")

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
            logger.info(f"db.session.add({b})")

    action_dict = {
        "name": "Flexitarier, konventionell",
        "sector": "Ernährung",
        "category": "Gemischt",
        "description": "Zweimal pro Woche Fleisch oder Fisch, durchschnittliche Mengen an Wurtsprodukten, Milchprodukten, Obst und Gemüse.",
        "savings": 300.0,
        "reduction_factor": 300 / 1800,
        "solution_text": f"Führt im Vergleich zum durchschnittlichen Ernährungsstil zu Einsparungen von 300 kg CO2eq pro Jahr",
        "reference": "https://www.zwei-grad-eine-tonne.at/hintergrund-berechnungen/abschnitt-i-lustvoll-die"
                     "-welt-retten"
    }

    rm1 = Action(**action_dict)
    db.session.add(rm1)
    logger.info(f"db.session.add({rm1})")
    # %%

    drexel_dict = {
        "name": "Bio-Flexitarier",
        "sector": "Ernährung",
        "category": "Gemischt",
        "description": " ".join([action_dict["description"], "Wann immer möglich regional und bio."]),
        "savings": 1800.0 - 1100,
        "reduction_factor": (1800.0 - 1100) / 1800,
        "solution_text": f"Führt im Vergleich zum durchschnittlichen Ernährungsstil zu Einsparungen von 300 kg CO2eq pro Jahr",
        "reference": "https://www.zwei-grad-eine-tonne.at/hintergrund-berechnungen/abschnitt-i-lustvoll-die"
    }
    rm2 = Action(**drexel_dict)
    db.session.add(rm2)
    logger.info(f"db.session.add({rm2})")

    with open("static/data/Abschnitt%20I%20Verkehr.csv", encoding="utf-8", newline='') as f:
        freader = csv.DictReader(f, delimiter=",")
        # for line in freader:
        #     logger.info(line["Lebensmittel"], line["CO2-Äquivalent in kg pro Person und Jahr"])
        all = []  # keys = kategorien, vals = list of foods
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

    if input(f"Commit to db? [y/n]? ").upper() == "Y":
        db.session.commit()
        logger.info(f"db.session.commit()")


def delete_table(table):
    for item in table.query.all():
        db.session.delete(item)
    if input(f"Confirm deleting table '{table.__tablename__}' [y/n]? ").upper() == "Y":
        db.session.commit()
        logger.info(f"db.session.commit()")
    else:
        db.session.rollback()
        logger.info(f"db.session.rollback()")


if __name__ == "__main__":
    wb = openpyxl.load_workbook("app/static/data/Emissionskatalog.xlsx", read_only=False, data_only=True)
    ws = wb.active
    table_ref = ws._tables["Tabelle1"].ref
    table = ws[table_ref]
    headers = {}
    for i in enumerate(table[0]):
        print(i[0], i[1])
        headers[i[1].value] = i[0]

    for row in table[1:]:
        emission_dict = {
            "sector": row[headers["sector"]].value,
            "category": row[headers["category"]].value,
            "variation": row[headers["variation"]].value,
            "name": row[headers["name"]].value,
            "description": row[headers["description"]].value,
            "emissions": row[headers["emissions"]].value,
            "reference": row[headers["reference"]].value,
            "comment": row[headers["comment"]].value,
        }
        e = Emission(**emission_dict)
        db.session.add(e)

    if input(f"Commit {len(table)-1} Emission entries to db? [y/n]? ").upper() == "Y":
        db.session.commit()
        logger.info(f"db.session.commit()")
    else:
        db.session.rollback()
        logger.info(f"db.session.rollback()")

    # emissions_table = wb.active.tables["Table1"]
    logger.info(f"finished {__name__}.")

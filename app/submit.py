from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField

from wtforms.validators import DataRequired, NumberRange, URL, Length, AnyOf

sectors = ["Ernährung",
           "Verkehr",
           "Fliegen",
           "Urlaub",
           "Sport und Freizeit",
           "Haustiere",
           "Sonstiger Konsum",
           "Bauen und Wohnen"]

class SubmitForm(FlaskForm):
    description = StringField("Beschreibung",
                              validators=[DataRequired()],
                              default="irgendwas halt")
    sector = StringField("Sektor", validators=[AnyOf(sectors)])
    category = StringField("Kategorie")
    savings = FloatField("Einsparungen [kg CO2eq/a]",
                         validators=[NumberRange(-20000, 20000,
                                                 message="Einsparungen sind positiv. Müssen zwischen -2000 und 2000 liegen", ),
                                     DataRequired()],
                         default=100.0)
    solution_text = StringField("Text zur Auflösung")
    reference = StringField("Quelle",
                            default="https://www.zwei-grad-eine-tonne.at/hintergrund-berechnungen/abschnitt-i-lustvoll-die-welt-retten")
    comment = StringField("Kommentar")
    submit = SubmitField("Abschicken")

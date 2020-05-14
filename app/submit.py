from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField

from wtforms.validators import DataRequired, NumberRange, URL


class SubmitForm(FlaskForm):
    description = StringField("Beschreibung",
                              validators=[DataRequired()],
                              default="irgendwas halt")
    savings = FloatField("Einsparung [t CO2eq/a]",
                         validators=[NumberRange(-20, 20,
                                                 message="Muss zwischen -20 und 20 liegen", ),
                                     DataRequired()],
                         default=-3.1415)
    source = StringField("Quelle",
                         validators=[URL()],
                         default="https://wikipedia.org")
    submit = SubmitField("Abschicken")

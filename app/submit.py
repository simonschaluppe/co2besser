from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField

from wtforms.validators import DataRequired, NumberRange, URL, Length


class SubmitForm(FlaskForm):
    description = StringField("Beschreibung",
                              validators=[DataRequired()],
                              default="irgendwas halt")
    savings = FloatField("Einsparung [kg CO2eq/a]",
                         validators=[NumberRange(-2000, 2000,
                                                 message="Muss zwischen -2000 und 2000 liegen", ),
                                     DataRequired()],
                         default=-3.1415)
    reference = StringField("Quelle",
                            default="https://wikipedia.org")
    comment = StringField("Kommentar")
    submit = SubmitField("Abschicken")

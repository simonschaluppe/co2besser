from random import sample

from flask import render_template, flash, redirect, url_for, logging

from app import app, db_session, database
from app.models import Action
from app.submit import SubmitForm


@app.route('/')
@app.route('/index')
def index():
    # l = len(current_actions)
    # a1, a2 = sample(range(l), 2)
    app.a1, app.a2 = sample(database.data.all()[1:], 2)
    # [a1], current_actions[a2]
    return render_template("index.html", action1=app.a1, action2=app.a2)


@app.route('/guess_left')
def guess_left():
    return render_template("guess_left.html", action1=app.a1, action2=app.a2)

@app.route('/guess_right')
def guess_right():
    return render_template("guess_right.html", action1=app.a1, action2=app.a2)
#TODO: Guesses in einem template zusammenfassen:
#def guess(side):
#   return render_template("reveal.html", guess=side, action1=app.a1, action2=app.a2)
@app.route('/reveal')
def reveal():
    return render_template("reveal.html", action1=app.a1, action2=app.a2)


@app.route('/actions')
def actions():
    # getze actions
    return render_template("actions.html", actions=database.data.all()[1:])


@app.route('/submit', methods=["GET", "POST"])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        # Maßnahme hinzufügen
        # import pdb
        # pdb.set_trace()
        id = len(database.data.all()) + 1
        new_action = Action(id=id, name="var" + str(id),
                            description=form.description.data,
                            savings=form.savings.data,
                            source=form.source.data,
                            )

        # test_actions.append(new_action)
        db_session.add(new_action)
        db_session.commit()
        flash("Maßnahme #{}: {} wurde hinzugefügt".format(new_action.name, new_action.description))
        return redirect(url_for("submit"))
    return render_template("submit_new.html", form=form)


from random import sample

from flask import render_template, flash, redirect, url_for

from app import app, db_session, database
from app.models import Action
from app.submit import SubmitForm


@app.route('/')
@app.route('/index')
def index():
    global current_actions
    current_actions = database.data.all()
    l = len(current_actions)
    a1, a2 = sample(range(1,l), 2)
    t1, t2 = current_actions[a1], current_actions[a2]
    return render_template("index.html", action1=t1, action2=t2)


@app.route('/actions')
def actions():
    # getze actions
    current_actions = database.data
    return render_template("actions.html", actions=current_actions)


@app.route('/submit', methods=["GET", "POST"])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        # Maßnahme hinzufügen
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

from random import sample

from flask import render_template, flash, redirect, url_for, logging

from app import app, db
from app.models import Action, Comparison
from app.submit import SubmitForm
from app import db_utils



# not quite sure where this is supposed to go
def reset_guess():
    if Action.query.all():
        app.action1, app.action2 = sample(Action.query.all(), 2)
        app.guess = None
        app.correct = max(app.action1, app.action2)

        #find Comparison, if existing take it, if not add it
        app.comparison = None
        new_comp = Comparison(action1=app.action1, action2=app.action2)
        for comp in db.session.query(Comparison).all():
            if new_comp == comp:
                app.comparison = comp
                flash(f"found {app.comparison}")

        if app.comparison is None:
            db.session.add(new_comp)
            db.session.commit()
            app.comparison = db.session.query(Comparison).all()[-1]

            flash(f"added {app.comparison}")

    else:
        app.action1, app.action2 = None, None
        app.comparison = None


@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/index')
def index():
    # [a1], current_actions[a2]
    reset_guess()
    return render_template("guess.html", app=app)


@app.route('/guess')
def guess():
    reset_guess()
    return render_template("guess.html", app=app)


@app.route('/guess_left')
def guess_left():
    app.guess = app.action1
    c = db.session.query(Comparison).get(app.comparison.id)
    if app.action1 == c.action1:
        c.votes_1 += 1
    elif app.action1 == c.action2:
        c.votes_2 += 1
    else:
        raise ValueError(f"{app.action1} is not part of {c.__repr__()}!")
    db.session.commit()
    flash(f"Registered Vote for {app.action1} in {c}")
    return render_template("guess.html", app=app)


@app.route('/guess_right')
def guess_right():
    app.guess = app.action2
    c = db.session.query(Comparison).get(app.comparison.id)
    if app.action2 == c.action1:
        c.votes_1 += 1
    elif app.action2 == c.action2:
        c.votes_2 += 1
    else:
        raise ValueError(f"{app.action2} is not part of {c.__repr__()}!")
    db.session.commit()
    flash(f"Registered Vote for {app.action2} in {c}")
    return render_template("guess.html", app=app)

# TODO: Guesses in einem template zusammenfassen:
# def guess(side):
#   return render_template("reveal.html", guess=side, action1=app.a1, action2=app.a2)
# @app.route('/reveal')
# def reveal():
#     return render_template("reveal.html", action1=app.a1, action2=app.a2)



@app.route('/actions')
def actions():
    # getze actions
    return render_template("actions.html", table=Action)

@app.route('/comparisons')
def comparisons():
    # getze actions
    return render_template("actions.html", table=Comparison)


@app.route('/submit', methods=["GET", "POST"])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        # Maßnahme hinzufügen
        # import pdb
        # pdb.set_trace()
        new_action = Action(name="var" + str(Action.query.count() + 1),
                            description=form.description.data,
                            sector=form.sector.data,
                            category=form.category.data,
                            savings=form.savings.data,
                            solution_text=form.solution_text.data,
                            reference=form.reference.data,
                            comment=form.comment.data
                            )

        # test_actions.append(new_action)
        db.session.add(new_action)
        db.session.commit()
        flash("Maßnahme #{}: {} wurde hinzugefügt".format(new_action.name, new_action.description))
        return redirect(url_for("submit"))
    return render_template("submit_new.html", form=form)

# @app.route('/reset_DB')
# def reset_db():
#     # reset the db
#     for i, item in enumerate(Action.query.all()):
#         db.session.delete(item)
#     db.session.commit()
#     flash(f"Reset DB: {i} Action(s) deleted.")
#     return redirect(url_for("actions"))



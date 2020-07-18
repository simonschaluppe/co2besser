from app import db


# Table action

class Emission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    sector = db.Column(db.String, index=True)
    category = db.Column(db.String, index=True)
    variation = db.Column(db.String, index=True)

    description = db.Column(db.String, index=True)

    emissions = db.Column(db.Float, index=True)

    reference = db.Column(db.String, index=True)
    comment = db.Column(db.String)

    def __lt__(self, other):
        return self.emissions < other.emissions

    def __eq__(self, other):
        if other == None:
            return False
        return self.emissions == other.emissions

    def __le__(self, other):
        return self.emissions == other.emissions or self.emissions < other.emissions

    def __repr__(self):
        return f"<Emission {self.id}: {self.name}>"

    def __str__(self):
        return self.__repr__()


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    sector = db.Column(db.String, index=True)
    category = db.Column(db.String, index=True)

    reduction_factor = db.Column(db.Float, index=True)
    savings = db.Column(db.Float, index=True)

    description = db.Column(db.String, index=True)
    solution_text = db.Column(db.String, index=True)

    reference = db.Column(db.String, index=True)
    comment = db.Column(db.String)

    # def __init__(self, **kwargs):
    #     self.name = kwargs.get('name')
    #     self.sector = kwargs.get('sector', "Kein Sektor")
    #     self.category = kwargs.get('category', "Keine Kategorie")
    #     # for key, value in kwargs.items():
    #     #     setattr(self, key, value)
    #
    #     # self.reduction_factor = kwargs.get("reduction_factor",REDUCTIONS[self.reduction])
    #     self.co2standard = kwargs.get("co2standard", 0.0)
    #     self.savings = kwargs.get("savings", 0.0)
    #     self.description = kwargs.get("description")
    #     # f"Maßnahme: {self.category} um {self.reduction} reduzieren.")

    def image(self, size):
        pass

    def __lt__(self, other):
        return self.savings < other.savings

    def __eq__(self, other):
        if other == None:
            return False
        return self.savings == other.savings

    def __le__(self, other):
        return self.savings == other.savings or self.savings < other.savings

    def __repr__(self):
        return f"<Action {self.id}: {self.name}>"


# TODO: Add Comparisons, that log action pairings, as well as votes

class Comparison(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a1_id = db.Column(db.Integer, db.ForeignKey("action.id"), index=True)
    a2_id = db.Column(db.Integer, db.ForeignKey("action.id"), index=True)
    action1 = db.relationship("Action", foreign_keys=[a1_id])
    action2 = db.relationship("Action", foreign_keys=[a2_id])
    votes_1 = db.Column(db.Integer, default=0)
    votes_2 = db.Column(db.Integer, default=0)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif (self.action1 == other.action1 and self.action2 == other.action2) \
                or (self.action1 == other.action2 and self.action2 == other.action1):
            return True
        else:
            return False

    def __repr__(self):
        return f"<Comparison {self.id}: {self.action1} {self.votes_1} : {self.votes_2} {self.action2}>"



from app import db

# Table action

class Action(db.Model):
    __tablename__ = "action"
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
        return f"< Action {self.id}: {self.name}>"


# TODO: Add Comparisons, that log action pairings, as well as votes

class Comparison(db.Model):
    __tablename__ = "comparison"
    id = db.Column(db.Integer, primary_key=True)
    a1_id = db.Column(db.Integer, db.ForeignKey("action.id"), index=True)
    a2_id = db.Column(db.Integer, db.ForeignKey("action.id"), index=True)
    action1 = db.relationship("Action", foreign_keys=[a1_id])
    action2 = db.relationship("Action", foreign_keys=[a2_id])
    votes_1 = db.Column(db.Integer)
    votes_2 = db.Column(db.Integer)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        elif (self.a1_id == other.a1_id and self.a2_id == other.a2_id)\
            or (self.a1_id == other.a2_id and self.a1_id == other.a2_id):
            return True
        else:
            return False

class Test(db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True)
    testfield = db.Column(db.String)
    testfield2 = db.Column(db.String)




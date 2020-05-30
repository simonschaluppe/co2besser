from sqlalchemy import Column, Integer, String, Float, ForeignKey

from app.database import Base
from app import db


# Table action
class Action(Base):
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    savings = Column(Float)
    source = Column(String)
    comment = Column(String)

    # action_other_data = relationship("other", backref="action")

class Action2(db.Model):
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
    id = db.Column(Integer, primary_key=True)
    action1_id = db.Column(Integer, ForeignKey("action.id"))
    action2_id = db.Column(Integer, ForeignKey("action.id"))
    votes_1 = db.Column(Integer)
    votes_2 = db.Column(Integer)
    doesnshowup = db.Column(String)


class Test(db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True)
    testfield = db.Column(db.String)
    testfield2 = db.Column(String)




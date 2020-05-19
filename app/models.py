from sqlalchemy import Column, Integer, String, Float

from app.database import Base


# Table action
class Action(Base):
    __tablename__ = 'action'
    id = Column(Integer,
                   primary_key=True)
    name = Column(String)
    description = Column(String)
    savings = Column(Float)
    source = Column(String)
    comment = Column(String)
    # action_other_data = relationship("other", backref="action")

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
        return '<Maßnahme %r>' % self.name


# TODO: Add Comparisons, that log action pairings, as well as votes
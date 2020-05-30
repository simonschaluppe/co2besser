from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

metaData = MetaData()
engine = create_engine('sqlite:///db\co2besser', convert_unicode=True,
                       connect_args={'check_same_thread': False}, echo=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()

    # noinspection PyUnresolvedReferences
    import app.models
    Base.metadata.create_all(bind=engine)


def get_actions():
    from app.models import Action
    return db_session.query(Action)

data = get_actions()

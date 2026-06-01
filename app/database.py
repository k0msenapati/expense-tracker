from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///expenses.db"

engine = create_engine(DATABASE_URL)


def get_session():
    return Session(engine)


def create_db():
    SQLModel.metadata.create_all(engine, checkfirst=True)

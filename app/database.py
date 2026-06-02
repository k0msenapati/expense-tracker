from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()


@st.cache_resource
def get_engine():
    return create_engine(os.getenv("DATABASE_URL", "sqlite:///expenses.db"))


engine = get_engine()


def get_session():
    return Session(engine)


def create_db():
    SQLModel.metadata.create_all(engine, checkfirst=True)

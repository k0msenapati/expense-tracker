from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")


@st.cache_resource
def get_engine():
    return create_engine(
        f"sqlite+{TURSO_DATABASE_URL}?secure=true",
        connect_args={
            "auth_token": TURSO_AUTH_TOKEN,
        },
    )


engine = get_engine()


def get_session():
    return Session(engine)


def create_db():
    SQLModel.metadata.create_all(engine, checkfirst=True)

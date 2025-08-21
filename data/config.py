from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
from os import environ

load_dotenv()

IP = environ.get("IP")
ENV = environ.get("ENV")
ADMIN_M1 = environ.get("ADMIN_M1")
ADMIN_M2 = environ.get("ADMIN_M2")
BOT_TOKEN = environ.get("BOT_TOKEN")
DATABASE_URL = environ.get("DATABASE_URL")
STATEMENT_TIMEOUT_MS = environ.get("STATEMENT_TIMEOUT_MS")
engine = create_engine(environ.get("DATABASE_URL"))
Base = declarative_base()
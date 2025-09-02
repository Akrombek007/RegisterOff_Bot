from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
from os import environ

load_dotenv()

IP = environ.get("IP")
ENV = environ.get("ENV")
ADMIN_M1 = environ.get("ADMIN_M1")
ADMIN_M2 = environ.get("ADMIN_M2")
ADMIN_PROF_T = environ.get("ADMIN_PROF_T")
ADMIN_PED_PSIX = environ.get("ADMIN_PED_PSIX")
ADMIN_ANIQ_HARBIY = environ.get("ADMIN_ANIQ_HARBIY")
ADMIN_INO_FILOLOG = environ.get("ADMIN_INO_FILOLOGIYA")
ADMIN_TABIIY_MAGISTR = environ.get("ADMIN_TABIIY_MAGISTR")
ADMIN_MAKTABGACHA_BOSHLANGICH = environ.get("ADMIN_MAKTABGACHA_BOSHLANGICH")
BOT_TOKEN = environ.get("BOT_TOKEN")
DATABASE_URL = environ.get("DATABASE_URL")
STATEMENT_TIMEOUT_MS = environ.get("STATEMENT_TIMEOUT_MS")
engine = create_engine(environ.get("DATABASE_URL"))
Base = declarative_base()
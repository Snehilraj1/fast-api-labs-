from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

password = quote_plus("Sraj@1332")
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://postgres:{password}@localhost:5432/fastapi"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
from sqlalchemy import create_engine
from databases import Database

DATABASE_URL = "postgresql://postgres:12345678@localhost/http-qt"

engine = create_engine(DATABASE_URL, pool_size=3, max_overflow=0)
database = Database(DATABASE_URL)

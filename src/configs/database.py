from decouple import config
from pymongo import MongoClient

DATABASE_URL = config("DATABASE_URL")

db = MongoClient(DATABASE_URL)

def get_db():
    """Função geradora para fornecer uma conexão com o banco."""
    yield db

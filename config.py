import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_student_cep_2026")
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://apnabazar:cepprojectapnabazar20@cluster0.vwp0bzh.mongodb.net/inventory_billing_db?retryWrites=true&w=majority"
    )
    DATABASE_NAME = os.getenv("DATABASE_NAME", "inventory_billing_db")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1")

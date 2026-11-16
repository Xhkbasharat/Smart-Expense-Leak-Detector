
import os

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "change-this-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = "sqlite:///expenses.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

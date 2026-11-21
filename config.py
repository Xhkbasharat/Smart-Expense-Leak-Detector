
import os


class Config:

    # =================================
    # APPLICATION SECURITY
    # =================================

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-key-change-before-deployment"
    )

    # =================================
    # DATABASE CONFIGURATION
    # =================================

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    INSTANCE_DIR = os.path.join(
        BASE_DIR,
        "instance"
    )

    os.makedirs(
        INSTANCE_DIR,
        exist_ok=True
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + os.path.join(INSTANCE_DIR, "expenses.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =================================
    # APPLICATION SETTINGS
    # =================================

    APP_NAME = "Smart Expense Leak Detector"

    APP_VERSION = "1.0.0"

    DEBUG = os.environ.get(
        "FLASK_DEBUG",
        "False"
    ).lower() == "true"
    

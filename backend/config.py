import os

class Config:
    FLASK_ENV = os.getenv('.env', 'production')
    # DEBUG = os.getenv(".debug", False)
import os

import dotenv

if os.environ.get("ENVIRONMENT", "local") == "production":
    dotenv.load_dotenv(".production.env")
    DB_HOST = os.environ["COCKTAILS_DB_HOST"]
    DB_USER = os.environ["COCKTAILS_DB_USER"]
    DB_PASSWORD = os.environ["COCKTAILS_DB_PASSWORD"]
    DB_DATABASE = os.environ["COCKTAILS_DB_DATABASE"]
    DB_PORT = os.environ["COCKTAILS_DB_PORT"]
else:
    DB_HOST = "localhost"
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_DATABASE = "cocktails"
    DB_PORT = 5432

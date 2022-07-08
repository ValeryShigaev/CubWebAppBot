from os import getenv

from dotenv import load_dotenv

load_dotenv()

#app
secret_key = getenv("SECRET_KEY")
allowed_hosts = getenv("ALLOWED_HOSTS").split(" ")

#db
sql_engine = getenv("SQL_ENGINE")
sql_database = getenv("SQL_DATABASE")
sql_user = getenv("SQL_USER")
sql_password = getenv("SQL_PASSWORD")
sql_host = getenv("SQL_HOST")
sql_port = getenv("SQL_PORT")
database = getenv("DATABASE")

#bot
bot_token = getenv("BOT_TOKEN")
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MYSQL_USER: str = config.get("mysql_local", "mysql_user")
MYSQL_PASSWORD: str = config.get("mysql_local", "mysql_password")
MYSQL_HOST: str = config.get("mysql_local", "host")
MYSQL_DB: str = config.get("mysql_local", "db_name")
POSTGRES_USER: str = config.get("postgres_remote", "postgres_user")
POSTGRES_PASSWORD: str = config.get("postgres_remote", "postgres_password")
POSTGRES_HOST: str = config.get("postgres_remote", "host")
POSTGRES_PORT: str = config.get("postgres_remote", "port")
POSTGRES_DB: str = config.get("postgres_remote", "db_name")

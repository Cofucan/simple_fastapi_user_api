import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MYSQL_USER: str = config.get("mysql", "user")
MYSQL_PASSWORD = config.get("mysql", "password")
SERVER_IP = config.get("mysql", "server_ip")
DB_NAME = config.get("mysql", "db_name")

import configparser

config = configparser.ConfigParser()
config.read("config.ini")

MYSQL_USER: str = config.get("mysql", "mysql_user")
MYSQL_PASSWORD: str = config.get("mysql", "mysql_password")
SERVER_IP: str = config.get("mysql", "server_ip")
DB_NAME: str = config.get("mysql", "db_name")

from peewee import *
import os

db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_name = os.environ["DB_NAME"]
db_host = os.environ["DB_HOST"]

host_args = db_host.split(":")
db_hostname, db_port = host_args[0], int(host_args[1])

conn = MySQLDatabase(
    db_name, user=db_user,
    password=db_pass,
    host=db_hostname
)
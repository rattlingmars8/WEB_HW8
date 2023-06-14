from mongoengine import connect
import configparser

config = configparser.ConfigParser()
config.read('D:\PYton\DZshki\WEB\WEB_HW_8\PT2\source\config.ini')

mongo_user = config.get('DB', 'USER')
mongo_pass = config.get('DB', 'PASS')
mongo_domain = config.get('DB', 'DOMAIN')
mongo_db_name = config.get('DB', 'DATA_BASE')

connect(
    host=f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_domain}/{mongo_db_name}?retryWrites=true&w=majority", ssl=True
)


# def get_database():
#     from mongoengine import get_db
#
#     return get_db()

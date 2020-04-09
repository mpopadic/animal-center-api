from configparser import ConfigParser

config = ConfigParser()

config['settings'] = {
    'debug': 'true',
    'secret_key': 'animal-center-secret',
    'log_path': 'requests.log',
    'python_version': '3',
}

config['db'] = {
    'db_name': 'db.sqlite3'
}


with open('./config.ini', 'w') as f:
    config.write(f)
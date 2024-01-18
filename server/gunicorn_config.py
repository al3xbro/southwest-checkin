import configparser
config = configparser.ConfigParser()
config.read('config.ini')

bind = f"{config.get('App', 'host_ip')}:{config.get('App', 'host_port')}"
workers = 2 
certfile = config.get('App', 'certfile_path')
keyfile = config.get('App', 'keyfile_path')

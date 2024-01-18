import configparser
conf = configparser.ConfigParser()
conf.read('conf.ini')

bind = f"{conf.get('App', 'host_ip')}:{conf.get('App', 'host_port')}"
workers = 2 
certfile = conf.get('App', 'certfile_path')
keyfile = conf.get('App', 'keyfile_path')

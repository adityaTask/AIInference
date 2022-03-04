# from jproperties import Properties
#
# configs = Properties()
#
# with open('D:\\workspace_python\\AITesting\\utilities\\config.properties', 'rb') as config_file:
#     configs.load(config_file)
#
# items_view = configs.items()
#
# configs_dict = {}
#
# for item in items_view:
#     configs_dict[item[0]] = item[1].data


import configparser
config = configparser.ConfigParser()
config.read('..\\utilities\\config.ini')


#print( config['files']['export_file'])


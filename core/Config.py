import ConfigParser

'''
@author Asiri Hewage
date : 31 May 2020
Class : Config
Objective : Manage configurations through a single point
'''


class Conf:

    def __init__(self):
        self.Config = ConfigParser.ConfigParser()
        self.conf_path = 'config/config.ini'
        self.Config.read(self.conf_path)

    def get_configs(self, section, option):
        return self.Config.get(section=section,
                               option=option)

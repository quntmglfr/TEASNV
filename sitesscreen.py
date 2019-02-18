from kivy.config import Config
from kivy.uix.screenmanager import Screen


class SitesScreen(Screen):

    def __init__(self, **kwargs):
        super(SitesScreen, self).__init__(**kwargs)
        self.config = Config.get_configparser('app')
    
    def set_site(self, **kwargs):
        self.config.set('network', 'host', kwargs['host'])
        self.config.set('network', 'port', kwargs['port'])
        self.config.set('network', 'password', kwargs['password'])
        self.parent.parent.current = 'snvscreen'

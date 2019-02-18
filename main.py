import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

Builder.load_file('snvchassis.kv')
Builder.load_file('indicator.kv')
Builder.load_file('sitevoter.kv')
Builder.load_file('controlprocessor.kv')
Builder.load_file('sitesscreen.kv')


class TeaSnv(ScreenManager):
    pass


class TeaSnvApp(App):

    def build(self):
        return TeaSnv()

    def build_config(self, config):
        config.setdefaults('network', {'host': '192.168.1.200', 
                                       'port': '23', 
                                       'password': 'lightfoot'})

    def build_settings(self, settings):
        settings.add_json_panel('TEA SNV', self.config, filename='teasnv.json')


if __name__ == '__main__':
    TeaSnvApp().run()

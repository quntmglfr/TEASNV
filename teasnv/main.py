import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder

Builder.load_file('data/snvchassis.kv')
Builder.load_file('data/indicator.kv')
Builder.load_file('data/sitevoter.kv')
Builder.load_file('data/controlprocessor.kv')
Builder.load_file('data/sitesscreen.kv')


class TeaSnvApp(App):
    kv_directory = 'data'

    def build(self):
        self.icon = 'data/icon.png'
        self.title = 'SNV-12 Remote Display'

    def build_config(self, config):
        config.setdefaults('network', {'host': '192.168.1.200', 
                                       'port': '23', 
                                       'password': 'lightfoot'})

    def build_settings(self, settings):
        settings.add_json_panel('TEA SNV',
                                self.config,
                                filename='data/teasnv.json')


if __name__ == '__main__':
    TeaSnvApp().run()

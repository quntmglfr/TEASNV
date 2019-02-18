import requests
import socket

from bs4 import BeautifulSoup

from kivy.clock import Clock
from kivy.config import Config
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from telnetlib import Telnet


class ControlProcessor(BoxLayout):

    link = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ControlProcessor, self).__init__(**kwargs)
        self.connected = None
        self.header = None
        self.host = None
        self.password = None
        self.port = None
        self.tn = None
        self.update_event = None

    def connection(self, instance, value):
        if value == 'down':
            config = Config.get_configparser('app')
            self.host = config.get('network', 'host')
            self.port = str(config.get('network', 'port'))
            self.password = config.get('network', 'password')
            try:
                self.tn = Telnet(self.host, self.port, 3)
                self.header = self.tn.read_until(b'Password:')
                self.tn.write(self.password.encode('ascii') + b'\n')
                self.connected = self.tn.read_very_eager()
                self.connection_button.text = 'DCN'
                self.link = True
                self.update_event = Clock.schedule_interval(self.update,1.0/30)
                self.snv_chassis.site_names = self._get_site_names()
                self.snv_chassis.channel_name = self._get_channel_name()
            except (socket.herror,
                    socket.error,
                    socket.gaierror,
                    socket.timeout,
                    EOFError) as err:
                popup = Popup(title='Connection Error',
                              content=Label(text=str(err),
                                            halign='center',
                                            valign='center'),
                              size_hint=(.4, .4))
                popup.open()
                self.connection_button.state = 'normal'
                self._clear_statuses()
        else:
            if self.tn is not None:
                self.tn.close()
            self.connection_button.text = 'CON'
            if self.update_event is not None:
                self.update_event.cancel()
            self._clear_statuses()

    def on_link(self, instance, value):
        self.link_indicator.led_active = value

    def _get_site_names(self):
        req = requests.get('http://' + self.host + '/SVMNames.html',
                            auth=('', self.password))
        soup = BeautifulSoup(req.text, 'html.parser')
        return [tag['value'] for tag in soup('input', type='text')]

    def _get_channel_name(self):
        lines = self.header.splitlines()
        for line in lines:
            if line.startswith(b'CPM'):
                return line.partition(b':')[2].strip().decode()
            
    def _clear_statuses(self):
        self.snv_chassis.status_bytes = [
                [str(site).encode('ascii'), b'0', b'0', b'OK']
                for site in range(1, 13)
                ]
        self.snv_chassis.site_names = ['' for i in range(32)]
        self.snv_chassis.channel_name = 'Touch for Sites'
        self.link = False

    def update(self, dt):
        try:
            raw_data = self.tn.read_very_eager()
            lines = raw_data.splitlines()
            status_bytes = [line.split() for line in lines if line]
            self.snv_chassis.status_bytes = status_bytes
        except EOFError as err:
            popup = Popup(title='Update Error',
                          content=Label(text=str(err)),
                          size_hint=(.4, .4))
            popup.open()
            self.update_event.cancel()
            self._clear_statuses()

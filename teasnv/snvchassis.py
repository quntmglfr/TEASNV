from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ListProperty
from teasnv.sitevoter import SiteVoter


class SnvChassis(BoxLayout):
    channel_name = StringProperty('Touch for Sites')
    site_names = ListProperty()
    status_bytes = ListProperty()

    def on_status_bytes(self, instance, value):
        try:
            for site_status in value:
                if site_status == [b'OK']:
                    pass
                else:
                    for child in self.children:
                        if isinstance(child, SiteVoter):
                            if child.site_number == int(site_status[0]):
                                child.status_bytes = site_status
        except ValueError as err:
            popup = Popup(title='Status Error',
                          content=Label(text=(str(err) + ' ' + str(value))), 
                          size_hint=(.4, .4))
            popup.open()

    def on_site_names(self, instance, value):
        if value:
            for child in self.children:
                if isinstance(child, SiteVoter):
                    child.site_name = self.site_names[child.site_number - 1]

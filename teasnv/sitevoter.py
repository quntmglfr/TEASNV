from kivy.properties import BooleanProperty, BoundedNumericProperty,\
    NumericProperty, ReferenceListProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout


class SiteVoter(BoxLayout):
    site_number = NumericProperty(0)
    site_name = StringProperty('')
    status_byte = NumericProperty(0)
    signal_quality = BoundedNumericProperty(0, min=0, max=31)
    site_status = ReferenceListProperty(status_byte, signal_quality)
    status_bytes = ListProperty()
    voted = BooleanProperty(False)
    unsquelched = BooleanProperty(False)
    fault = BooleanProperty(False)
    enabled = BooleanProperty(False)
    selected = BooleanProperty(False)
    tx_select = BooleanProperty(False)
    transmit = BooleanProperty(False)

    def on_status_byte(self, instance, value):
        self.voted = bool(value & 0b10000000)
        self.unsquelched = bool(value & 0b01000000)
        self.fault = bool(value & 0b00100000)
        self.enabled = bool(value & 0b00010000)
        self.selected = bool(value & 0b00001000)
        self.tx_select = bool(value & 0b00000100)
        self.transmit = bool(value & 0b00000010)

    def on_status_bytes(self, instance, value):
        if value[-1] == b'OK':
            self.site_status = [int(value[1], 16),
                                int(value[2], 16)]

    def on_voted(self, instance, value):
        self.voted_indicator.led_active = value

    def on_unsquelched(self, instance, value):
        self.unsquelched_indicator.led_active = value

    def on_fault(self, instance, value):
        self.fault_indicator.led_active = value

    def on_enabled(self, instance, value):
        if value and self.disabled:
            self.state_spinner.text = 'NRML'
            self.disabled = False
        elif not value and not self.disabled:
            self.state_spinner.text = 'DSBL'
            self.disabled = True

    def on_selected(self, instance, value):
        self.state_spinner.text = 'SEL'

    def on_tx_select(self, instance, value):
        self.tx_select_indicator.led_active = value

    def on_transmit(self, instance, value):
        # self.transmit_indicator.led_active = value
        if value:
            self.tx_select_indicator.led_color = 'orange'
        else:
            self.tx_select_indicator.led_color = 'red'

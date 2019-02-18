from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, OptionProperty, StringProperty


class Indicator(BoxLayout):
    text = StringProperty('')
    led_active = BooleanProperty(False)
    led_color = OptionProperty('grey', options=['green',
                                                'grey',
                                                'orange',
                                                'red'])

    def on_led_active(self, instance, value):
        if value:
            self.indicator_led.source = 'led-circle-' + self.led_color + '.png'
        else:
            self.indicator_led.source = 'led-circle-grey.png'

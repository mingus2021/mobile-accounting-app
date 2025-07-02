from kivy.app import App
from kivy.uix.label import Label

class MobileAccountingApp(App):
    def build(self):
        return Label(text='Mobile Accounting App - Build Test')

MobileAccountingApp().run()

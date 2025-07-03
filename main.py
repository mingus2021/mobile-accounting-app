from kivy.app import App
from kivy.uix.label import Label

class HelloWorldApp(App):
    def build(self):
        return Label(text='Hello World - APK Build Test')

HelloWorldApp().run()

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class HelloWorldApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        label = Label(
            text='Hello World!\nAPK Build Test Success!',
            font_size='20sp',
            halign='center'
        )

        button = Button(
            text='Click Me!',
            size_hint=(1, 0.3),
            on_press=self.on_button_click
        )

        layout.add_widget(label)
        layout.add_widget(button)

        return layout

    def on_button_click(self, instance):
        instance.text = 'Button Clicked!'

if __name__ == '__main__':
    HelloWorldApp().run()

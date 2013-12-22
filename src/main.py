from kivy.app import App
from kivy.uix.widget import Widget


class AgentBasedUni(Widget):
    pass


class AgentBasedUniApp(App):
    def build(self):
        return AgentBasedUni()


if __name__ == '__main__':
    AgentBasedUniApp().run()
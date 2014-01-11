import conf
import model

if conf.KIVY_READY:
	from kivy.app import App
	from kivy.uix.widget import Widget
	from kivy.properties import NumericProperty, ReferenceListProperty
	from kivy.vector import Vector

if conf.KIVY_READY:
	class PongBall(Widget):
	    velocity_x = NumericProperty(0)
	    velocity_y = NumericProperty(0)
	    velocity = ReferenceListProperty(velocity_x, velocity_y)

	    def move(self):
	        self.pos = Vector(*self.velocity) + self.pos


	class PongGame(Widget):
	    pass


	class PongApp(App):
	    def build(self):
	        return PongGame()


if __name__ == '__main__':
	if conf.KIVY_READY:
		PongApp().run()

	lec =  model.Lecturer("Bob", "m")
	print lec.getName()

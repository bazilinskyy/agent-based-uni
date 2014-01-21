import conf
import model
from simulation import simulate
from UniData import UniData
import sys

# Kivy imports
if conf.KIVY_READY:
	from kivy.app import App
	from kivy.uix.widget import Widget
	from kivy.vector import Vector
	# from kivy.garden.graph import Graph, MeshLinePlot
	from kivy.uix.slider import Slider
	from kivy.app import App
	from kivy.uix.button import Button
	from kivy.uix.boxlayout import BoxLayout
	from kivy.uix.checkbox import CheckBox
	from kivy.uix.scrollview import ScrollView
	from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

if conf.KIVY_READY:
	# class PongBall(Widget):
	#     velocity_x = NumericProperty(0)
	#     velocity_y = NumericProperty(0)
	#     velocity = ReferenceListProperty(velocity_x, velocity_y)

	#     def move(self):
	#         self.pos = Vector(*self.velocity) + self.pos
	 
	class HBoxWidget(Widget):
		def __init__(self, **kwargs):
			super(HBoxWidget, self).__init__(**kwargs)

	class VBoxWidget(Widget):
		def __init__(self, **kwargs):
			super(VBoxWidget, self).__init__(**kwargs)

	class SliderWithLabel(Widget):
		def __init__(self, **kwargs):
			super(SliderWithLabel, self).__init__(**kwargs)

	class CheckBoxWithLabel(Widget):
		def __init__(self, **kwargs):
			super(CheckBoxWithLabel, self).__init__(**kwargs)
			
	class ContainerBox(BoxLayout):
		scrollView = ObjectProperty(None)

		def update():
			print self.scrollView.text

		def __init__(self, **kwargs):
			super(ContainerBox, self).__init__(**kwargs)
			print self.scrollView.text
	 
	class UniSimulationApp(App):
		def build(self):
			return ContainerBox() 

# if conf.SHOW_TIMESTAMPS:
# 	old_f = sys.stdout
# 	class F:
# 	    def write(self, x):
# 	       sys.stdout.write(x.replace("\n", " [%s]\n" % str(datetime.now()) )
# 	sys.stdout = F()

if __name__ == '__main__':
	if conf.KIVY_READY:
		UniSimulationApp().run()

	# Run simulation
	simulate()
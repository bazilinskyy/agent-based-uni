import conf
import model
from simulation import simulate
from UniData import UniData
import sys

# Kivy imports
if conf.KIVY_READY:
	from kivy.app import App
	from kivy.uix.widget import Widget
	from kivy.properties import NumericProperty, ReferenceListProperty
	from kivy.vector import Vector
	from kivy.garden.graph import Graph, MeshLinePlot

if conf.KIVY_READY:
	# class PongBall(Widget):
	#     velocity_x = NumericProperty(0)
	#     velocity_y = NumericProperty(0)
	#     velocity = ReferenceListProperty(velocity_x, velocity_y)

	#     def move(self):
	#         self.pos = Vector(*self.velocity) + self.pos


	class MainWindow(Widget):   
		graph = Graph(xlabel='X', ylabel='Y', x_ticks_minor=5,
		x_ticks_major=25, y_ticks_major=1,
		y_grid_label=True, x_grid_label=True, padding=5,
		x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
		plot = MeshLinePlot(color=[1, 0, 0, 1])
		plot.points = [(x, sin(x / 10.)) for x in xrange(0, 101)]
		graph.add_plot(plot)


	class UniSimulationApp(App):
	    def build(self):
	        return MainWindow()

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
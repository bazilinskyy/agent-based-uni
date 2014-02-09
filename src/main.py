import conf
import model
from simulation import simulate
from UniData import UniData
import simulation
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
	from kivy.uix.tabbedpanel import TabbedPanel
	from kivy.uix.floatlayout import FloatLayout

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
		enrolledSlider = ObjectProperty(None)
		compensationLevelSlider = ObjectProperty(None)
		passingMarkSlider = ObjectProperty(None)
		numberOfModulesSlider = ObjectProperty(None)
		numberOfCourseSlider = ObjectProperty(None)
		compensationLevelSlider = ObjectProperty(None)
		compensationCheckBox = ObjectProperty(None)

		def __init__(self, **kwargs):
			super(VBoxWidget, self).__init__(**kwargs)

		def on_touch_up(self, touch):
			print self.enrolledSlider.value

	class SliderWithLabel(Widget):
		def __init__(self, **kwargs):
			super(SliderWithLabel, self).__init__(**kwargs)

	class CheckBoxWithLabel(Widget):
		def __init__(self, **kwargs):
			super(CheckBoxWithLabel, self).__init__(**kwargs)


			
	class ContainerBox(BoxLayout):
		textView = ObjectProperty(None)
		compensationLevelSlider = ObjectProperty(None)
		compensationLevelLabel = ObjectProperty(None)
		compensationThresholdSlider = ObjectProperty(None)
		compensationThresholdLabel = ObjectProperty(None)
		transferCheckBox = ObjectProperty(None)
		repeatsCheckBox = ObjectProperty(None)
		transferLabel = ObjectProperty(None)
		repeatsLabel = ObjectProperty(None)
 
		# Record current values in the GUI for updates
		previousValues= []

		def on_touch_up(self, touch):
			currentValues= [
				self.compensationLevelSlider.value,
				self.compensationThresholdSlider.value,
				self.transferCheckBox.active,
				self.repeatsCheckBox.active
			]

			# Update simulation variables
			compensationLevel = int(self.compensationLevelSlider.value)
			compensationThreashold = int(self.compensationThresholdSlider.value)
			repeatsLabel = self.repeatsCheckBox.active
			transferOfCredits = self.transferCheckBox.active

			# Update labels
			self.compensationLevelLabel.text = "Compensation\nlevel - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(compensationLevel) + "[/color]"
			self.compensationThresholdLabel.text = "Compensation\nthreashold - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(compensationThreashold) + "[/color]"

			for i in range(len(currentValues)):
				if (currentValues[i] != self.previousValues[i]):
					# TODO pass parameters to simulation function
					update = simulate(compensationLevel, compensationThreashold, repeatsLabel, transferOfCredits)
					if conf.DEBUG:
						print "Update from simulation: \n", update
					self.textView.text = update
					break
			self.previousValues = currentValues[:]

		def __init__(self, **kwargs):
			super(ContainerBox, self).__init__(**kwargs)
			self.previousValues= [
				self.compensationLevelSlider.value,
				self.compensationThresholdSlider.value,
				self.transferCheckBox.active,
				self.repeatsCheckBox.active
			]

			# Populate list of student in current intake
			# Load data from Excel and csv files
			data = UniData() 
			simulation.update = data.importData()
			simulation.intake = UniData.intakeSummer
			simulation.intakeAutumn = UniData.intakeAutumn
			simulation.modules = UniData.modules
			simulation.courses = UniData.courses
			self.textView.text = simulation.update

			# Update labels ans sliders with current values
			self.compensationLevelLabel.text = "Compensation\nlevel - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(conf.COMPENSATION_LEVEL) + "[/color]"
			self.compensationThresholdLabel.text = "Compensation\nthreashold - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(conf.COMPENSATION_THREASHOLD) + "[/color]"
			self.repeatsCheckBox.active = conf.AUTO_REPEATS
			self.transferCheckBox.active = conf.TRANSFER_OF_CREDITS
			self.compensationLevelSlider.value = conf.COMPENSATION_LEVEL
			self.compensationThresholdSlider.value = conf.COMPENSATION_THREASHOLD

	class UniSimulationApp(App):
		title = 'Agent-based simualation of NUIM by pavlo.bazilinskyy@gmail.com'

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
	# simulate()
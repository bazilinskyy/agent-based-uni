import conf
import model
from simulation import simulate
from UniData import UniData
import simulation
import sys
import copy

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
			pass

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
		intAgentLabelCheckBox = ObjectProperty(None)
		intAgentLabel = ObjectProperty(None)
		simulateButton = ObjectProperty(None)
		intAgentThresholdLabel = ObjectProperty(None)
		intAgentThresholdTextInput = ObjectProperty(None)
		intAgentChangeTextInput = ObjectProperty(None)
		intAgentChangeLabel = ObjectProperty(None)

		#Output labels - students
		studentsPassedLabel = ObjectProperty(None)
		studentsPassedValue = ObjectProperty(None)
		studentsPassedByCompensationLabel = ObjectProperty(None)
		studentsPassedByCompensationValue = ObjectProperty(None)
		studentsPassedByTransferOfCreditsLabel = ObjectProperty(None)
		studentsPassedByTransferOfCreditsValue = ObjectProperty(None)
		studentsPassedByAutoRepeatsLabel = ObjectProperty(None)
		studentsPassedByAutoRepeatsValue = ObjectProperty(None)
		averageGradeLabel = ObjectProperty(None)
		averageGradeValue = ObjectProperty(None)
		averageLeavingCertificateLabel = ObjectProperty(None)
		averageLeavingCertificateValue = ObjectProperty(None)
		studentsFailedLabel = ObjectProperty(None)
		studentsFailedValue = ObjectProperty(None)

		#Output labels - modules
		modulesPassedLabel = ObjectProperty(None)
		modulesPassedValue = ObjectProperty(None)
		modulesFailedLabel = ObjectProperty(None)
		modulesFailedValue = ObjectProperty(None)
		modulesPassedByCompensationLabel = ObjectProperty(None)
		modulesPassedByCompensationValue = ObjectProperty(None)
		modulesAbsentLabel = ObjectProperty(None)
		modulesAbsentValue = ObjectProperty(None)
		modulesPassedByAutoRepeatsLabel = ObjectProperty(None)
		modulesPassedByAutoRepeatsValue = ObjectProperty(None)
 
		# Record current values in the GUI for updates
		currentValues = []

		def runSimulation(self, instance):
			# Run simulation
			update = simulate(conf.COMPENSATION_LEVEL, conf.COMPENSATION_THREASHOLD, conf.AUTO_REPEATS , conf.TRANSFER_OF_CREDITS, conf.INTELLIGENT_AGENTS)

			if conf.DEBUG:
				print "Update from simulation: \n", update
			#self.textView.text = update
			self.updateLabels(update) # Update lebels on GUI

		def updateLabels(self, a):
			#Output labels - students
			self.studentsPassedValue.text = "[b]" + a["studentsPassedValue"] + "[b]"
			self.studentsPassedByCompensationValue.text = "[b]" + a["studentsPassedByCompensationValue"] + "[b]"
			self.studentsPassedByTransferOfCreditsValue.text = "[b]" + a["studentsPassedByTransferOfCreditsValue"] + "[b]"
			self.studentsPassedByAutoRepeatsValue.text = "[b]" + a["studentsPassedByAutoRepeatsValue"] + "[b]"
			self.averageGradeValue.text = "[b]" + a["averageGradeValue"] + "[b]"
			self.averageLeavingCertificateValue.text = "[b]" + a["averageLeavingCertificateValue"] + "[b]"
			self.studentsFailedValue.text = "[b]" + a["studentsFailedValue"] + "[b]"

			#Output labels - modules
			# self.modulesPassedValue = a["modulesPassedValue"]
			# self.modulesFailedValue = a["modulesFailedValue"]
			# self.modulesPassedByCompensationValue = a["modulesPassedByCompensationValue"]
			# self.modulesAbsentValue = a["modulesAbsentValue"]
			# self.modulesPassedByAutoRepeatsValue = a["modulesPassedByAutoRepeatsValue"]

		def on_touch_up(self, touch):
			# Auto repeats and transfer of credits cannot be True at the same time
			if (self.transferCheckBox.active and self.currentValues[3]):
				self.repeatsCheckBox.active = False
			if (self.repeatsCheckBox.active and self.currentValues[4]):
				self.transferCheckBox.active = False

			self.currentValues = [
				self.compensationLevelSlider.value,
				self.compensationThresholdSlider.value,
				self.transferCheckBox.active,
				self.repeatsCheckBox.active,
				self.intAgentCheckBox.active
			]

			# Update simulation variables
			conf.COMPENSATION_LEVEL = int(self.compensationLevelSlider.value)
			conf.COMPENSATION_THREASHOLD = int(self.compensationThresholdSlider.value)
			conf.AUTO_REPEATS = self.repeatsCheckBox.active
			conf.TRANSFER_OF_CREDITS = self.transferCheckBox.active
			conf.INTELLIGENT_AGENTS = self.intAgentCheckBox.active
			conf.INTELLENT_AGENT_LC_THRESHOLD = int(self.intAgentThresholdTextInput.text)
			conf.INTELLENT_AGENT_CHANGE = float(self.intAgentChangeTextInput.text)

			# Update labels
			self.compensationLevelLabel.text = "Compensation\nlevel - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(conf.COMPENSATION_LEVEL) + "[/color]"
			self.compensationThresholdLabel.text = "Compensation\nthreashold - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(conf.COMPENSATION_THREASHOLD) + "[/color]"

		def __init__(self, **kwargs):
			super(ContainerBox, self).__init__(**kwargs)
			self.currentValues= [
				self.compensationLevelSlider.value,
				self.compensationThresholdSlider.value,
				self.transferCheckBox.active,
				self.repeatsCheckBox.active,
				self.intAgentCheckBox.active
			]

			# Populate list of student in current intake
			# Load data from Excel and csv files
			data = UniData() 
			simulation.update = data.importData()
			simulation.intake = UniData.intakeSummer
			simulation.intakeAutumn = UniData.intakeAutumn
			simulation.modules = UniData.modules
			simulation.courses = UniData.courses
			#self.textView.text = simulation.update

			# Populate initial data
			simulation.initial_intake = copy.deepcopy(UniData.intakeSummer)
			simulation.initial_intakeAutumn = copy.deepcopy(UniData.intakeAutumn)
			simulation.initial_modules = copy.deepcopy(UniData.modules)
			simulation.initial_courses = copy.deepcopy(UniData.courses)

			# Update labels ans sliders with current values
			self.compensationLevelLabel.text = "Compensation\nlevel - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(conf.COMPENSATION_LEVEL) + "[/color]"
			self.compensationThresholdLabel.text = "Compensation\nthreashold - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(conf.COMPENSATION_THREASHOLD) + "[/color]"
			self.repeatsCheckBox.active = conf.AUTO_REPEATS
			self.transferCheckBox.active = conf.TRANSFER_OF_CREDITS
			self.compensationLevelSlider.value = conf.COMPENSATION_LEVEL
			self.compensationThresholdSlider.value = conf.COMPENSATION_THREASHOLD
			self.intAgentCheckBox.active = conf.INTELLIGENT_AGENTS
			self.intAgentThresholdTextInput.text = str(conf.INTELLENT_AGENT_LC_THRESHOLD)
			self.intAgentChangeTextInput.text = str(conf.INTELLENT_AGENT_CHANGE)

			self.simulateButton.bind(on_press=self.runSimulation)

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
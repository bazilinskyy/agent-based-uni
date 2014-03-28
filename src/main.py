#!/usr/bin/env python
"""
Main file. To run with Kivy, type "kivy main.py" in the folder with this file.
Requires graph module from Kivy.garden. See: http://kivy.org/docs/api-kivy.garden.html
Also requires xlrg.
"""
# Copyright (c) 2014, Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
# Department of Computer Science, National University of Ireland, Maynooth
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
__author__ = "Pavlo Bazilinskyy"
__copyright__ = "Copyright 2008, National University of Ireland, Maynooth"
__credits__ = "Ronan Reilly"
__version__ = "1.0"
__maintainer__ = "Pavlo Bazilinskyy"
__email__ = "pavlo.bazilinskyy@gmail.com"
__status__ = "Production"

import conf
import model
from simulation import simulate
from UniData import UniData
import simulation
import sys
import copy
import re
from math import sin
from collections import OrderedDict

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
	from kivy.uix.textinput import TextInput
	from kivy.garden.graph import Graph, MeshLinePlot

if conf.KIVY_READY:
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
		# Plots for the graphs
		plotPassed = None
		plotFailed = None
		plotPassedArts = None
		plotFailedArts = None
		plotPassedSocial = None
		plotFailedSocial = None
		plotPassedScience = None
		plotFailedScience = None

		textView = ObjectProperty(None)
		compensationLevelSlider = ObjectProperty(None)
		compensationLevelLabel = ObjectProperty(None)
		compensationThresholdSlider = ObjectProperty(None)
		compensationThresholdLabel = ObjectProperty(None)
		transferCheckBox = ObjectProperty(None)
		repeatsCheckBox = ObjectProperty(None)
		transferLabel = ObjectProperty(None)
		repeatsLabel = ObjectProperty(None)
		repeatsCreditsLabel = ObjectProperty(None)
		repeatsCreditsSlider = ObjectProperty(None)
		intAgentLabelCheckBox = ObjectProperty(None)
		intAgentLabel = ObjectProperty(None)
		simulateButton = ObjectProperty(None)
		# intAgentThresholdLabel = ObjectProperty(None)
		# intAgentThresholdSlider = ObjectProperty(None)
		# intAgentChanceSlider = ObjectProperty(None)
		# intAgentChanceLabel = ObjectProperty(None)
		intAgentLevelLabel = ObjectProperty(None)
		intAgentLevelTextInput = ObjectProperty(None)
		graph = ObjectProperty(None)
		graphArts = ObjectProperty(None)
		graphSocial = ObjectProperty(None)
		graphScience = ObjectProperty(None)
		passByCompensationCheckBox = ObjectProperty(None)
		passByCompensationLabel = ObjectProperty(None)

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
			update = simulate(conf.COMPENSATION_LEVEL, conf.COMPENSATION_THREASHOLD, conf.AUTUMN_REPEATS , conf.TRANSFER_OF_CREDITS, conf.INTELLIGENT_AGENTS)

			if conf.DEBUG:
				print "Update from simulation: \n", update
			#self.textView.text = update
			self.updateLabels(update) # Update lebels on GUI

			##Plot graphs
			# Try to remove plots
			try:
				self.graph.remove_plot(self.plotPassed) # Remove passed plot
				self.graph.remove_plot(self.plotFailed) # Remove failed plot
				self.graphArts.remove_plot(self.plotPassedArts) # Remove passed plot
				self.graphArts.remove_plot(self.plotFailedArts) # Remove failed plot
				self.graphSocial.remove_plot(self.plotPassedSocial) # Remove passed plot
				self.graphSocial.remove_plot(self.plotFailedSocial) # Remove failed plot
				self.graphScience.remove_plot(self.plotPassedScience) # Remove passed plot
				self.graphScience.remove_plot(self.plotFailedScience) # Remove failed plot
			except Exception, e:
				pass

			# Sort dictionaries
			# Sort dictionaries with passed / failed agains leaving certificates
			lcPassed = OrderedDict(sorted(simulation.lcPassed.items()))
			lcFailed = OrderedDict(sorted(simulation.lcFailed.items()))
			lcPassedArts = OrderedDict(sorted(simulation.lcPassedArts.items()))
			lcFailedArts = OrderedDict(sorted(simulation.lcFailedArts.items()))
			lcPassedScience = OrderedDict(sorted(simulation.lcPassedScience.items()))
			lcFailedScience = OrderedDict(sorted(simulation.lcFailedScience.items()))
			lcPassedSocial = OrderedDict(sorted(simulation.lcPassedSocial.items()))
			lcFailedSocial = OrderedDict(sorted(simulation.lcFailedSocial.items()))

			#Plot for passed
			self.plotPassed = MeshLinePlot(color=[0, 1, 0, 1])
			self.plotPassed.points = [(x, y) for x, y in lcPassed.iteritems()]
			self.graph.add_plot(self.plotPassed)

			#Plot for failed
			self.plotFailed = MeshLinePlot(color=[1, 0, 0, 1])
			self.plotFailed.points = [(x, y) for x, y in lcFailed.iteritems()]
			self.graph.add_plot(self.plotFailed)

			#Plot for passed for ARTS,CELT.STUD. AND PHILOSOPHY
			self.plotPassedArts = MeshLinePlot(color=[0, 1, 0, 1])
			self.plotPassedArts.points = [(x, y) for x, y in lcPassedArts.iteritems()]
			self.graphArts.add_plot(self.plotPassedArts)

			#Plot for failed for ARTS,CELT.STUD. AND PHILOSOPHY
			self.plotFailedArts = MeshLinePlot(color=[1, 0, 0, 1])
			self.plotFailedArts.points = [(x, y) for x, y in lcFailedArts.iteritems()]
			self.graphArts.add_plot(self.plotFailedArts)

			#Plot for passed for SOCIAL SCIENCES
			self.plotPassedSocial = MeshLinePlot(color=[0, 1, 0, 1])
			self.plotPassedSocial.points = [(x, y) for x, y in lcPassedSocial.iteritems()]
			self.graphSocial.add_plot(self.plotPassedSocial)

			#Plot for failed for SOCIAL SCIENCES
			self.plotFailedSocial = MeshLinePlot(color=[1, 0, 0, 1])
			self.plotFailedSocial.points = [(x, y) for x, y in lcFailedSocial.iteritems()]
			self.graphSocial.add_plot(self.plotFailedSocial)

			#Plot for passed for SCIENCE AND ENGINEERING
			self.plotPassedScience = MeshLinePlot(color=[0, 1, 0, 1])
			self.plotPassedScience.points = [(x, y) for x, y in lcPassedScience.iteritems()]
			self.graphScience.add_plot(self.plotPassedScience)

			#Plot for failed for SCIENCE AND ENGINEERING
			self.plotFailedScience = MeshLinePlot(color=[1, 0, 0, 1])
			self.plotFailedScience.points = [(x, y) for x, y in lcFailedScience.iteritems()]
			self.graphScience.add_plot(self.plotFailedScience)


		def updateLabels(self, a):
			#Output labels - students
			self.studentsPassedValue.text = "[b]" + a["studentsPassedValue"] + "[b]"
			self.studentsPassedByCompensationValue.text = "[b]" + a["studentsPassedByCompensationValue"] + "[b]"
			self.studentsPassedByTransferOfCreditsValue.text = "[b]" + a["studentsPassedByTransferOfCreditsValue"] + "[b]"
			self.studentsPassedByAutoRepeatsValue.text = "[b]" + a["studentsPassedByAutoRepeatsValue"] + "[b]"
			self.averageGradeValue.text = "[b]" + "{0:.2f}".format(float(a["averageGradeValue"])) + "[b]"
			self.averageLeavingCertificateValue.text = "[b]" + "{0:.2f}".format(float(a["averageLeavingCertificateValue"])) + "[b]"
			self.studentsFailedValue.text = "[b]" + a["studentsFailedValue"] + "[b]"

			#Output labels - modules
			# self.modulesPassedValue = a["modulesPassedValue"]
			# self.modulesFailedValue = a["modulesFailedValue"]
			# self.modulesPassedByCompensationValue = a["modulesPassedByCompensationValue"]
			# self.modulesAbsentValue = a["modulesAbsentValue"]
			# self.modulesPassedByAutoRepeatsValue = a["modulesPassedByAutoRepeatsValue"]

		def on_touch_up(self, touch):
			self.refreshUIElements() # Activate / deactivate UI elements based on current values
			# Auto repeats and transfer of credits cannot be True at the same time. Same for pass by compensation. Only one method can be anabled at a time.

			self.currentValues = [
				self.compensationLevelSlider.value,
				self.compensationThresholdSlider.value,
				self.transferCheckBox.active,
				self.repeatsCheckBox.active,
				self.intAgentCheckBox.active,
				self.passByCompensationCheckBox.active,
				self.intAgentLevelTextInput.text,
				self.repeatsCreditsSlider.value
				# self.intAgentThresholdSlider.value,
				# self.intAgentChanceSlider.value
			]

			# Update simulation variables
			conf.COMPENSATION_LEVEL = int(self.compensationLevelSlider.value)
			conf.COMPENSATION_THREASHOLD = int(self.compensationThresholdSlider.value)
			conf.AUTUMN_REPEATS = self.repeatsCheckBox.active
			conf.TRANSFER_OF_CREDITS = self.transferCheckBox.active
			conf.INTELLIGENT_AGENTS = self.intAgentCheckBox.active
			# conf.INTELLENT_AGENT_LC_THRESHOLD = int(self.intAgentThresholdSlider.value)
			# conf.INTELLENT_AGENT_CHANCE = self.intAgentChanceSlider.value
			conf.INTELLENT_AGENT_COEF = float(self.intAgentLevelTextInput.text)
			conf.PASS_BY_COMPENSATION = self.passByCompensationCheckBox.active
			conf.AUTUMN_REPEATS_LIMIT = int(self.repeatsCreditsSlider.value)

			self.updateConfLabels()

		def on_touch_move(self, touch):
			self.updateConfLabels()
			
		## Update labels
		def updateConfLabels(self):
			self.compensationLevelLabel.text = "Compensation\nlevel - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(int(self.compensationLevelSlider.value)) + "[/color]"
			self.compensationThresholdLabel.text = "Compensation\nthreashold - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(int(self.compensationThresholdSlider.value)) + "[/color]"
			self.repeatsCreditsLabel.text = "Allowed credits\nin autumn repeats - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(int(self.repeatsCreditsSlider.value)) + "[/color]"
			# self.intAgentThresholdLabel.text = "Intelligent\nthreashold - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(int(self.intAgentThresholdSlider.value)) + "[/color]"
			# Add zero to the value of chance to avoid jumping labels
			# chance = self.intAgentChanceSlider.value
			# if chance in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]: # Modulus does not work somehow
			# 	chance = str(chance) + "0"
			# else:
			# 	chance = str(chance)
			# self.intAgentChanceLabel.text = "Intelligent\nchance - [color=" + conf.LABEL_VALUE_COLOR + "]" + chance + "[/color]"

		# Activate / disable elements of GUI based on input
		def refreshUIElements(self):
			if self.transferCheckBox.active and not self.currentValues[2]:
				self.repeatsCheckBox.active = False
				self.passByCompensationCheckBox.active = False

				# Does not work somehow..
				self.compensationLevelSlider.disabled = True
				self.compensationThresholdSlider.disabled = True
				self.repeatsCreditsSlider.disabled = True

			elif self.repeatsCheckBox.active and not self.currentValues[3]:
				self.transferCheckBox.active = False
				self.passByCompensationCheckBox.active = False

				self.compensationLevelSlider.disabled = True
				self.compensationThresholdSlider.disabled = True
				self.repeatsCreditsSlider.disabled = False

			elif self.passByCompensationCheckBox.active and not self.currentValues[5]:
				self.transferCheckBox.active = False
				self.repeatsCheckBox.active = False

				self.compensationLevelSlider.disabled = False
				self.compensationThresholdSlider.disabled = False
				self.repeatsCreditsSlider.disabled = True

		def __init__(self, **kwargs):
			super(ContainerBox, self).__init__(**kwargs)

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
			self.repeatsCreditsLabel.text = "Allowed credits\nin autumn repeats - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(int(conf.AUTUMN_REPEATS_LIMIT)) + "[/color]"

			# self.intAgentThresholdLabel.text = "Intelligent\nthreashold - [color=" + conf.LABEL_VALUE_COLOR + "]" + str(conf.INTELLENT_AGENT_LC_THRESHOLD) + "[/color]"
			# Add zero to the value of chance to avoid jumping labels
			# chance = conf.INTELLENT_AGENT_CHANCE
			# if chance in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]: # Modulus does not work somehow
			# 	chance = str(chance) + "0"
			# else:
			# 	chance = str(chance)
			# self.intAgentChanceLabel.text = "Intelligent\nchance - [color=" + conf.LABEL_VALUE_COLOR + "]" + chance + "[/color]"
			self.repeatsCheckBox.active = conf.AUTUMN_REPEATS
			self.transferCheckBox.active = conf.TRANSFER_OF_CREDITS
			self.compensationLevelSlider.value = conf.COMPENSATION_LEVEL
			self.compensationThresholdSlider.value = conf.COMPENSATION_THREASHOLD
			self.intAgentCheckBox.active = conf.INTELLIGENT_AGENTS
			# self.intAgentThresholdSlider.value = conf.INTELLENT_AGENT_LC_THRESHOLD
			# self.intAgentChanceSlider.value = conf.INTELLENT_AGENT_CHANCE
			self.intAgentLevelTextInput.text = str(conf.INTELLENT_AGENT_COEF)
			self.passByCompensationCheckBox.active = conf.PASS_BY_COMPENSATION
			self.repeatsCreditsSlider.value = conf.AUTUMN_REPEATS_LIMIT

			# Use button to run simulation
			self.simulateButton.bind(on_press=self.runSimulation)

			# Records current values in the GUI
			self.currentValues= [
				self.compensationLevelSlider.value,
				self.compensationThresholdSlider.value,
				self.transferCheckBox.active,
				self.repeatsCheckBox.active,
				self.intAgentCheckBox.active,
				self.passByCompensationCheckBox.active,
				self.intAgentLevelTextInput.text,
				self.repeatsCreditsSlider.value
				# self.intAgentThresholdSlider.value,
				# self.intAgentChanceSlider.value
			]

	class UniSimulationApp(App):
		title = 'Agent-based simualation of NUIM by pavlo.bazilinskyy@gmail.com'

		def build(self):
			return ContainerBox() 

	class FloatInput(TextInput):

		pat = re.compile('[^0-9]')
		def insert_text(self, substring, from_undo=False):
			pat = self.pat
			if '.' in self.text:
				s = re.sub(pat, '', substring)
			else:
				s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
			return super(FloatInput, self).insert_text(s, from_undo=from_undo)

# if conf.SHOW_TIMESTAMPS:
# 	old_f = sys.stdout
# 	class F:
# 	    def write(self, x):
# 	       sys.stdout.write(x.replace("\n", " [%s]\n" % str(datetime.now()) )
# 	sys.stdout = F()

if __name__ == '__main__':
	if conf.KIVY_READY:
		UniSimulationApp().run()
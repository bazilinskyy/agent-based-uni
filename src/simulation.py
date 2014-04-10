#!/usr/bin/env python
"""
Actual simualtion happens here. It uses data from conf.py for simualation parameters.
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
import random
from UniData import UniData
import random
import copy
from math import ceil

# Populate list of student in current intake
# Load data from Excel and csv files
intake = {} 		# Summer intake
intakeAutumn = {} 	# Autumn intake
modules = {}		# All modules, sorted by ID
courses = []		# List of all courses

# Record initial state, with no changes
initial_intake = {} 		# Summer intake
initial_intakeAutumn = {} 	# Autumn intake
initial_modules = {}		# All modules, sorted by ID
initial_courses = []		# List of all courses	

# Record statistics of students passing/failing based on their school leaving certificates
lcPassed = {}
lcFailed = {}
# Also record passed/failed ratios for individual faculties
# ARTS,CELT.STUD. AND PHILOSOPHY
lcPassedArts = {}
lcFailedArts = {}
# SOCIAL SCIENCES
lcPassedSocial = {}
lcFailedSocial = {}
# SCIENCE AND ENGINEERING
lcPassedScience = {}
lcFailedScience = {}

# Algorithm by Pavlo Bazilinskyy
def simulate(compensationLevel, compensationThreashold, autoRepeats, transferOfCredits, intelligentAgents):
	# Reset data
	intake = copy.deepcopy(initial_intake)
	intakeAutumn = copy.deepcopy(initial_intakeAutumn)
	modules = copy.deepcopy(initial_modules)
	courses = copy.deepcopy(initial_courses)
	lcPassed.clear()
	lcFailed.clear()
	lcPassedArts.clear()
	lcFailedArts.clear()
	lcPassedSocial.clear()
	lcFailedSocial.clear()
	lcPassedScience.clear()
	lcFailedScience.clear()

	# Variables for calculating 
	studentsPassed = 0
	studentsFailed = 0
	studentsPassedByCompensation = 0
	studentsPassedByTransferCredits = 0
	studentsPassedByAutoRepeats = 0
	totalAverageMark = 0.0

	# For calculation of the average leaving certificate
	averageLeavingCert = 0.0

	# Sanity check for a number of failed students
	tempFailedCounter = 0
	for student in intake.keys(): # Iterate through all students
		for moduleEnr in intake[student].moduleEnrollments: 
			if (intake[student].moduleEnrollments[moduleEnr].status == "PASS BY COMPENSATION" or
			intake[student].moduleEnrollments[moduleEnr].status == "FAIL" or
			intake[student].moduleEnrollments[moduleEnr].status == "ABSENT" or
			intake[student].moduleEnrollments[moduleEnr].status == "DID NOT COMPLETE"):

				tempFailedCounter += 1
				break
	if conf.DETAILED_DEBUG:
		print "SUMMER INTAKE: ", len(intake)
		print "FAILED before adjustments: ", tempFailedCounter

	for student in intake.keys(): # Iterate through all students

		# Define variables to calculate results in modules
		passedModules = 0
		failedModules = 0
		failedModulesList = []
		absentModules = 0
		passByCompensationModules = 0
		excemptionModules = 0
		satisfactoryModules = 0
		didNotCompleteModules = 0

		## Normalise some values of received marks as they seem to be wrong in Excel sheets			
		# Check if it is actually a pass based on received marks
		for moduleEnr in intake[student].moduleEnrollments:
			moduleEnr = intake[student].moduleEnrollments[moduleEnr]
			if conf.NORMALISE_VALUES:
				if moduleEnr.status == "PASS BY COMPENSATION":
					if (moduleEnr.marksReceived < conf.COMPENSATION_LEVEL):
						moduleEnr.marksReceived = conf.PASSING_THRESHOLD - 1
				elif moduleEnr.status == "PASS":
					if (moduleEnr.marksReceived < conf.PASSING_THRESHOLD):
						moduleEnr.marksReceived = conf.PASSING_THRESHOLD
				elif moduleEnr.status == "FAIL":
					if (moduleEnr.marksReceived == 0):
						moduleEnr.marksReceived = int(conf.PASSING_THRESHOLD / 2) # Many rows have mark == 0 in the table
					elif (moduleEnr.marksReceived > conf.PASSING_THRESHOLD):
						moduleEnr.marksReceived = conf.PASSING_THRESHOLD - 1
				# elif moduleEnr.status == "DID NOT COMPLETE": # Artificially, bring the average grade up
				# 	if (moduleEnr.marksReceived < conf.COMPENSATION_LEVEL):
				# 		moduleEnr.marksReceived = conf.PASSING_THRESHOLD - 1

		# Calculate average grade
		averageGrade = 0.0
		for moduleEnr in intake[student].moduleEnrollments:
			# Average grade calculation
			averageGrade += intake[student].moduleEnrollments[moduleEnr].marksReceived
		averageGrade /= len(intake[student].moduleEnrollments)
		totalAverageMark += averageGrade # Calculating average grade among all students

		# Calculating average leaving certificate
		averageLeavingCert += intake[student].leavingCertificate

		if conf.DETAILED_DEBUG:
			print "Student ID: ", intake[student].studentID, " Average grade: ", averageGrade

		##### MAIN ALGORITHM Iterate through all modeules that were taken by the student
		for moduleEnr in intake[student].moduleEnrollments:
			moduleEnr = intake[student].moduleEnrollments[moduleEnr]

			if conf.DETAILED_DEBUG:
				print "MODULE ID: ", moduleEnr.module.moduleID, " MARK: ", moduleEnr.marksReceived, " STATUS: ", moduleEnr.status


			## Adjust what was assigned to modules, based on the configuration
			if moduleEnr.status == "PASS BY COMPENSATION":
				if (averageGrade < conf.COMPENSATION_THREASHOLD or 
				moduleEnr.marksReceived < conf.COMPENSATION_LEVEL or
				conf.PASS_BY_COMPENSATION == False):
				# Could be two possibilities
					if moduleEnr.marksReceived < conf.PASSING_THRESHOLD: # Check if received grade is less than passing threshold
						moduleEnr.status = "FAIL"
					else:
						moduleEnr.status = "PASS"

			elif moduleEnr.status == "PASS":
				if (moduleEnr.marksReceived >= conf.COMPENSATION_LEVEL and 
				averageGrade >= conf.COMPENSATION_THREASHOLD and 
				moduleEnr.marksReceived < conf.PASSING_THRESHOLD and
				conf.PASS_BY_COMPENSATION == True):
					moduleEnr.status = "PASS BY COMPENSATION"

				elif moduleEnr.marksReceived < conf.PASSING_THRESHOLD: # Check if received grade is less than passing threshold
					moduleEnr.status = "FAIL"

			elif moduleEnr.status == "FAIL":
				if (moduleEnr.marksReceived >= conf.COMPENSATION_LEVEL and 
				averageGrade >= conf.COMPENSATION_THREASHOLD and 
				moduleEnr.marksReceived < conf.PASSING_THRESHOLD and
				conf.PASS_BY_COMPENSATION == True):
					moduleEnr.status = "PASS BY COMPENSATION"
					
				elif moduleEnr.marksReceived < conf.PASSING_THRESHOLD: # Check if received grade is less than passing threshold
					moduleEnr.status = "FAIL"


			## Intelligent agent behaviour
			grade = moduleEnr.marksReceived
			# Add marks based on the leaving school certificate mark, based on probability of exhibiting intellgent behaviour INTELLENT_AGENT_CHANGE
			if conf.INTELLIGENT_AGENTS and random.random() <= conf.INTELLENT_AGENT_CHANCE and intake[student].leavingCertificate >= conf.INTELLENT_AGENT_LC_THRESHOLD:
				#print "grade: ", grade, " plus: ", float(conf.INTELLENT_AGENT_COEF) / 1000 * intake[student].leavingCertificate
				grade += float(conf.INTELLENT_AGENT_COEF) / 1000 * intake[student].leavingCertificate
				moduleEnr.marksReceived = grade
				# Check if it makes a failed module passed
				# if (moduleEnr.status == "FAIL" and moduleEnr.marksReceived >= conf.PASSING_THRESHOLD):
				# 	moduleEnr.status = "PASS"
				# Check if it makes a failed module passed by compensation
				# elif (moduleEnr.status == "FAIL" and 
				# 	moduleEnr.marksReceived >= conf.COMPENSATION_LEVEL and 
				# 	averageGrade >= conf.COMPENSATION_THREASHOLD and 
				# 	conf.PASS_BY_COMPENSATION == True):

				# 	moduleEnr.status = "PASS BY COMPENSATION"
				# 	print "pass 2 ", moduleEnr.marksReceived
				# # Check if it makes a passed by compensation module passed
				# elif moduleEnr.status == "PASS BY COMPENSATION" and moduleEnr.marksReceived >= conf.PASSING_THRESHOLD:
				# 	moduleEnr.status = "PASS"
				# Check if a student was absent on the exam
				if (moduleEnr.status == "ABSENT" and conf.INTELLENT_AGENT_ABSENT_MODULE):
					# Calcualate total average grade
					tempAverageGrade = 0.0
					for tempModuleEnr in intake[student].moduleEnrollments:
						tempAverageGrade += moduleEnr.marksReceived
					tempAverageGrade /= len(intake[student].moduleEnrollments)
					# If average grade > conf.INTELLENT_AGENT_ABSENT_MODULE_THRESHOLD, there is "conf.INTELLENT_AGENT_CHANGE / 2" chance the student passed this module with a grade equal to his average grade
					if tempAverageGrade >= conf.INTELLENT_AGENT_ABSENT_MODULE_THRESHOLD and random.random() <= conf.INTELLENT_AGENT_CHANCE / 2:
						moduleEnr.status = "PASS"
						moduleEnr.marksReceived = int(tempAverageGrade)

			#First check if pass by compesation still holds
			if (moduleEnr.status == "PASS BY COMPENSATION"):
				passByCompensationModules += 1	
			elif (moduleEnr.status == "PASS"):
				passedModules += 1
			elif (moduleEnr.status == "FAIL"):
				failedModules += 1
				failedModulesList.append(moduleEnr)
			elif (moduleEnr.status == "ABSENT"):
				absentModules += 1				
			elif (moduleEnr.status == "DID NOT COMPLETE"): # Treat it as missing data
				failedModules += 1
				failedModulesList.append(moduleEnr)
			elif (moduleEnr.status == "EXEMPTION"): # Treat it as passed
				passedModules += 1
			elif (moduleEnr.status == "SATISFACTORY"):
				#satisfactoryModules += 1
				passedModules += 1

		# Found failed modules, and autumn repeats are possible
		if (failedModules > 0 and conf.AUTUMN_REPEATS == True and conf.TRANSFER_OF_CREDITS == False
			and conf.PASS_BY_COMPENSATION == False):
			# Check if a student failed fewer or equal number of modules that can be repeated in autumn
			failedCredits = 0
			for fMod in failedModulesList:
				try:
					failedCredits += int(fMod.module.moduleCredit)
				except Exception, e:
					failedCredits += 5 # Give 5 credits by default, if information is missing

			if failedModules <= conf.AUTUMN_REPEATS_LIMIT:
				# Find this student in autumn intake
				if (intake[student].studentID in intakeAutumn.keys()):
					for moduleEnr in intake[student].moduleEnrollments:
						moduleEnr = intake[student].moduleEnrollments[moduleEnr]
						# Iterate through failed modules
						if (moduleEnr.module.moduleID in intakeAutumn[intake[student].studentID].moduleEnrollments.keys()):
							# Check new status of the module after it was retaken
							modEnrAutumn = intakeAutumn[intake[student].studentID].moduleEnrollments[moduleEnr.module.moduleID]
							if (modEnrAutumn.status == "PASS"): 
								failedModules -= 1

							# elif (intakeAutumn[intake[student].studentID].moduleEnrollments[moduleEnr.module.moduleID] == "FAIL"):
							# 	failedModules += 1
							# 	failedModulesList.append(moduleEnr)
							# elif (intakeAutumn[intake[student].studentID].moduleEnrollments[moduleEnr.module.moduleID] == "ABSENT"):
							# 	absentModules += 1
							elif (modEnrAutumn.status == "PASS BY COMPENSATION"):
									# Check if pass by compensation holds, if not mark this module as failed
									if (averageGrade >= conf.COMPENSATION_THREASHOLD and modEnrAutumn.marksReceived >= conf.COMPENSATION_LEVEL):
										failedModules -= 1
							elif (modEnrAutumn.status == "DID NOT COMPLETE"):
								didNotCompleteModules += 1
								failedModules -= 1
							elif (modEnrAutumn.status == "EXEMPTION"):
								excemptionModules += 1
								failedModules -= 1
							# Treat Satisfactory as Passed
							elif (modEnrAutumn.status == "SATISFACTORY"):
								#satisfactoryModules += 1
								failedModules -= 1

					# Check if students managed to pass all modules by auto repeats
					if (failedModules == 0):
						if conf.DETAILED_DEBUG:
							print "1 passed with autumn repeats"
						studentsPassedByAutoRepeats += 1
						studentsPassed += 1
						intake[student].resultFromSimluation = True
						addLcPassed(intake[student])
						continue

			# Student did not pass failed modules
			if conf.DETAILED_DEBUG:
				print "2 failed modules: ", failedModules
				for fMod in failedModulesList:
					print fMod.status, " ", fMod.module.moduleID
			studentsFailed += 1
			intake[student].resultFromSimluation = False
			addLcFailed(intake[student])
			continue

		# Pass by compensation modules found, but it was used for more than two modules
		if (passByCompensationModules > 2 and conf.PASS_BY_COMPENSATION == True):
			studentsFailed += 1
			intake[student].resultFromSimluation = False
			addLcFailed(intake[student])
			continue
		# Found failed modules, transer of credits is allowed
		elif (failedModules > 0 and conf.TRANSFER_OF_CREDITS == True and conf.AUTUMN_REPEATS == False and conf.PASS_BY_COMPENSATION == False):
			# Calculate how many modules were failed and compare that number 
			# to the number of modules that can be transfered to the next year
			if (failedModules > conf.TRANSFER_OF_CREDITS_MODULES):
				if conf.DETAILED_DEBUG:
					print "7 failed modules: ", failedModules
					for fMod in failedModulesList:
						print fMod.status, " ", fMod.module.moduleID
				studentsFailed += 1
				intake[student].resultFromSimluation = False
				addLcFailed(intake[student])
				continue
			else:
				if conf.DETAILED_DEBUG:
					print "8 passed with transfer of credits."
				studentsPassedByTransferCredits += 1
				studentsPassed += 1
				intake[student].resultFromSimluation = True
				addLcPassed(intake[student])
				continue
		# Student can pass by compensation
		elif (passByCompensationModules <= 2 and passByCompensationModules > 0 and conf.PASS_BY_COMPENSATION == True):
			# for moduleEnr in intake[student].moduleEnrollments:
			# 	if (intake[student].moduleEnrollments[moduleEnr].status == "PASS BY COMPENSATION"):
			# 		print intake[student].moduleEnrollments[moduleEnr].marksReceived
			if conf.DETAILED_DEBUG:
				print "10 passed by compensation. Modules passed by compensation: ", passByCompensationModules
			studentsPassedByCompensation += 1
			studentsPassed += 1
			intake[student].resultFromSimluation = True
			addLcPassed(intake[student])
			continue

		# Students still has failed modules -> fail
		elif (failedModules > 0):
			if conf.DETAILED_DEBUG:
				print "11 failed: ", failedModules
				for fMod in failedModulesList:
					print fMod.status, " ", fMod.module.moduleID
			studentsFailed += 1
			intake[student].resultFromSimluation = False
			addLcFailed(intake[student])
			continue
		# Student has absent modules, and auto repeats, transfer of credits and pass by compensation are disabled
		elif (absentModules > 0):
			if conf.DETAILED_DEBUG:
				print "6 absent: ", absentModules
			studentsFailed += 1
			intake[student].resultFromSimluation = False
			addLcFailed(intake[student])
			continue
				# Student did not complete modules
		elif (didNotCompleteModules > conf.DID_NOT_COMPLETE_MODULES and didNotCompleteModules > 0):
			if conf.DETAILED_DEBUG:
				print "9 did not complete: ", didNotCompleteModules
			studentsFailed += 1
			intake[student].resultFromSimluation = False
			addLcFailed(intake[student])
			continue

		# Everything is fine and this student can go to the next year
		studentsPassed += 1
		intake[student].resultFromSimluation = True
		addLcPassed(intake[student])


	totalAverageMark /= len(intake) # Calculate average grade
	averageLeavingCert /= len(intake) # Calcualte average leaving certificate

	if conf.DEBUG:
		print "Simulation finished."

		print 'Results:'
		print 'Students passed: ', str(studentsPassed)
		print 'Students failed: ', str(studentsFailed)
		print 'Students passed by compensation: ', str(studentsPassedByCompensation)
		print 'Students passed by transfer of credits: ', str(studentsPassedByTransferCredits)
		print 'Students passed by auto repeats: ', str(studentsPassedByAutoRepeats)
		print 'Average grade: ', str(totalAverageMark)
		print 'Average leaving certificate: ', str(averageLeavingCert)

	update = {}
	update["studentsPassedValue"] = str(studentsPassed)
	update["studentsFailedValue"] = str(studentsFailed)
	update["studentsPassedByCompensationValue"] = str(studentsPassedByCompensation)
	update["studentsPassedByTransferOfCreditsValue"] = str(studentsPassedByTransferCredits)
	update["studentsPassedByAutoRepeatsValue"] = str(studentsPassedByAutoRepeats)
	update["averageGradeValue"] = str(totalAverageMark)
	update["averageLeavingCertificateValue"] = str(averageLeavingCert)

	# update["modulesPassedValue"] = str(passedModules)
	# update["modulesFailedValue"] = str(failedModulesd)
	# update["modulesPassedByCompensationValue"] = str(modulesPass)
	# update["modulesAbsentValue"] = str(studentsPassed)
	# update["modulesPassedByAutoRepeatsValue"] = str(studentsPassed)

	if conf.DEBUG:
		print update

	return update

# Record in the dictionary of numbers of students who failed sorted by leaving certificate points
def addLcFailed(student):
	try:
		lcFailed[roundup(student.leavingCertificate)] += 1
	except KeyError, e:
		lcFailed[roundup(student.leavingCertificate)] = 1

		# Also add to the list of the faculty
	if (student.faculty == "ARTS,CELT.STUD. AND PHILOSOPHY"):
		try:
			lcFailedArts[roundup(student.leavingCertificate)] += 1
		except KeyError, e:
			lcFailedArts[roundup(student.leavingCertificate)] = 1
	if (student.faculty == "SOCIAL SCIENCES"):
		try:
			lcFailedSocial[roundup(student.leavingCertificate)] += 1
		except KeyError, e:
			lcFailedSocial[roundup(student.leavingCertificate)] = 1
	if (student.faculty == "SCIENCE AND ENGINEERING"):
		try:
			lcFailedScience[roundup(student.leavingCertificate)] += 1
		except KeyError, e:
			lcFailedScience[roundup(student.leavingCertificate)] = 1

# Record in the dictionary of numbers of students who passed sorted by leaving certificate points
def addLcPassed(student):
	try:
		lcPassed[roundup(student.leavingCertificate)] += 1
	except KeyError, e:
		lcPassed[roundup(student.leavingCertificate)] = 1

	# Also add to the list of the faculty
	if (student.faculty == "ARTS,CELT.STUD. AND PHILOSOPHY"):
		try:
			lcPassedArts[roundup(student.leavingCertificate)] += 1
		except KeyError, e:
			lcPassedArts[roundup(student.leavingCertificate)] = 1
	if (student.faculty == "SOCIAL SCIENCES"):
		try:
			lcPassedSocial[roundup(student.leavingCertificate)] += 1
		except KeyError, e:
			lcPassedSocial[roundup(student.leavingCertificate)] = 1
	if (student.faculty == "SCIENCE AND ENGINEERING"):
		try:
			lcPassedScience[roundup(student.leavingCertificate)] += 1
		except KeyError, e:
			lcPassedScience[roundup(student.leavingCertificate)] = 1

# Round integer, used for smoothing graphs
def roundup(x):
	return int(ceil(x / float(conf.GRAPH_ROUND)) * conf.GRAPH_ROUND)

# Algorithm by Ronan Reilly and Pavlo Bazilinskyy
def simulate_old(compensationLevel, compensationThreashold, autoRepeats, transferOfCredits):
	#createIntake()
	semester = 1

	# Assume a four year course with two semesters per year
	while (semester <= 8):

		for student in intake:
			# intake
			if (semester == 1):
				course = random.choice(courses)
				course.addStudent(intake[student])
				modules = course.getModules()

				for module in modules:
					if (intake[student].canTake(module) and module.getSemesterGiven() == intake[student].getSemester()):
						module.addStudent(intake[student])
			
			# progress
			modulesTaken = intake[student].moduleEnrollments
			for module in modulesTaken:
				result = modulesTaken[module].marksReceived
				if (result >= 40):
					intake[student].points += modulesTaken[module].module.getModuleCredit()
					intake[student].marks += result * modulesTaken[module].module.getModuleCredit() / course.getCourseCredit()
				intake[student].semester += 1
		semester += 1

	if conf.DEBUG:
		print "Simulation finished."

	return "SIMULATION FINISHED."
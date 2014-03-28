#!/usr/bin/env python
"""
Loading data from Excel files stored at /src/data.
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

import traceback
from xlrd import open_workbook, cellname
import csv
import model
import conf
import random

class UniData():
	intakeSummer = {}
	intakeAutumn = {}
	courses = []
	courseTypes = []
	modules = {}
	moduleEnrollments = []
	courseEnrollments = []
	departments = []
	faculties = []

	# @property
	# def intakeAutumn(self):
	# 	return self._intakeAutumn

	# @intakeAutumn.setter
	# def intakeAutumn(self, value):
	# 	self._intake = value

	# @property
	# def intakeSummer(self):
	# 	print "BOO"
	# 	return self._intakeSummer

	# @intakeSummer.setter
	# def intakeSummer(self, value):
	# 	self._intakeSummer = value

	# @property
	# def courses(self):
	# 	return self._courses

	# @courses.setter
	# def courses(self, value):
	# 	self._courses = value

	# @property
	# def modules(self):
	# 	return self._modules

	# @modules.setter
	# def modules(self, value):
	# 	self._modules = modules

	def importData(self):		
		# Populate  
		if (len(self.courses) < 1 and len(self.modules) < 1 and len(self.intakeSummer) < 1 and len(self.intakeAutumn) < 1): # import from files only once
			try:
				## Opening the excel or csv file
				if (not conf.USE_SMALL_DATA): # Use full data
					fileCourses = self.openDataFile(conf.FILE_WITH_COURSES)
					fileModules = self.openDataFile(conf.FILE_WITH_MODULES)
					fileIntakeSummer = self.openDataFile(conf.FILE_WITH_INTAKE_SUMMER)
					fileIntakeAutumn = self.openDataFile(conf.FILE_WITH_INTAKE_AUTUMN)
				else: # Use a smalls sample of data
					fileCourses = self.openDataFile(conf.SMALL_FILE_WITH_COURSES)
					fileModules = self.openDataFile(conf.SMALL_FILE_WITH_MODULES)
					fileIntakeSummer = self.openDataFile(conf.SMALL_FILE_WITH_INTAKE_SUMMER)
					fileIntakeAutumn = self.openDataFile(conf.SMALL_FILE_WITH_INTAKE_AUTUMN)
				
				sheetModules = fileModules.sheet_by_index(0)
				#sheetIntakeSummer = fileIntakeSummer.sheet_by_index(0)
				sheetIntakeAutumn = fileIntakeAutumn.sheet_by_index(0)
				## Calculating numbers of rows in received sheets
				
				#numRowsIntakeSummer = sheetIntakeSummer.nrows - 1
				numRowsIntakeAutumn = sheetIntakeAutumn.nrows - 1

				## Courses and course types
				linesIgnoreCourses = [1, 25, 36, 40, 44, 45, 56, 60, 63, 81, 82] # Lines to ignore in the file
				sheetCourses = fileCourses.sheet_by_index(0) # Only 1 sheet present
				numRowsCourses = sheetCourses.nrows - 1

				currentCourseType = ""
				for i in range(numRowsCourses):
					row = sheetCourses.row_slice(i+1)
					if (i + 1 not in linesIgnoreCourses):
						jointHons = -1
						singleHons = -1
						accepts = -1
						if (row[3].value != 0):
							accepts = row[3].value
						if (row[4].value != 0):
							singleHons = row[4].value
						if (row[5].value  != 0):
							jointHons = row[5].value

						# Check if it is a type of course
						if (row[0].value in model.CourseType.possibleCourseTypes):
							self.courseTypes.append(model.CourseType(row[0].value, row[3].value, singleHons, jointHons))
							currentCourseType = row[0].value

						# Otherwise, it must be a course
						else:
							courseCredit = -1 #TODO: need this data
							self.courses.append(model.Course(row[0].value, courseCredit,currentCourseType, accepts, singleHons, jointHons))

				## Modules, departments, faculties
				linesIgnoreModules = [0, 1, 2, 1209, 1210, 1211] # Lines to ignore in the file
				sheetModules = fileModules.sheet_by_index(0) # Reading the sheet with UG
				numRowsModules = sheetModules.nrows - 1

				## Courses and course types
				currentFaculty = model.Faculty("NA")
				currentDepartment = model.Department("NA", currentFaculty)

				for i in range(numRowsModules):
					row = sheetModules.row_slice(i+1)
					if (i + 1 not in linesIgnoreModules):
						# Check if we found a new faculty
						if (row[0].value != currentFaculty.name):
							newFaculty = model.Faculty(row[0].value)
							self.faculties.append(newFaculty)
							currentFaculty = newFaculty

						# Check if we found a new department
						if (row[1].value != currentDepartment.name):
							newDepartment = model.Department(row[1].value, currentFaculty)
							self.departments.append(newDepartment)
							currentDepartment = newDepartment

						# Add new module
						semesterGiven = -1 #TODO mossing data
						self.modules[row[2].value] = model.Module(
							row[2].value, # Module ID
							row[3].value, # Module name
							row[5].value, # Module credit
							semesterGiven, # Semester given
							currentDepartment, # Department
							row[4].value # Enrolled students
							)

				## Summer and autumn intakes
				
				# Summer intake
				tempSet = set()
				linesIgnoreIntakeSummer = [0, 1, 2, 3, 4, 5, 6] # Lines to ignore in the file
				sheetIntakeSummer = fileIntakeSummer.sheet_by_index(0) # Reading the sheet with UG
				numRowsIntakeSummer = sheetIntakeSummer.nrows - 1

				for i in range(numRowsIntakeSummer):
					row = sheetIntakeSummer.row_slice(i+1)
					if (i + 1 not in linesIgnoreIntakeSummer and row[2].value == 1): # Limit to result from only the first year
						if (str(row[3]) not in tempSet): 
							self.intakeSummer[str(int(row[3].value))] = model.Student(str(int(row[3].value)))

							# Leaving certificate
							if (int(row[11].value) <= 625):
								self.intakeSummer[str(int(row[3].value))].leavingCertificate = int(row[11].value) # Leaving certificate from Wrs column
							else:
								if (int(row[12].value) <= 625): # Check if the value is still correct
									self.intakeSummer[str(int(row[3].value))].leavingCertificate = int(row[12].value) # Leaving certificate from Random column
								else: # The value is not real leaving certificate -> assign to a random value
									self.intakeSummer[str(int(row[3].value))].leavingCertificate = random.randint(250, 625) # Leaving certificate from Random column

							# Faculty
							self.decideFaculty(str(row[1].value), self.intakeSummer[str(int(row[3].value))]) # Call a separate function, as there are a lot of programs

							tempSet.add(str(row[3]))

						## Enrol student into a module
						# Default to the first semester of a given year

						# Try to find a previously loaded module
						try:
							moduleEnrolled = self.modules[row[4].value]
						except KeyError, e: # If not found, add a new entry
							moduleEnrolled = model.Module(
								row[2].value, # Module ID
								"", # Module name
								0, # Module credit
								row[2].value * 2, # Semester given
								None, # Department
								None # Enrolled Students
								) #TODO add more accurate information

							# And add to the list of modules
							self.modules[row[2].value] = moduleEnrolled
						# And module enrollment
						moduleEnroll = model.ModuleEnrollment(self.intakeSummer[str(int(row[3].value))], moduleEnrolled, 1)

						# PASS / FAIL / ABSENT / PASS BY COMPENSATION etc.
						if (row[6].value == "PASS"): 
							moduleEnroll.status = "PASS"
						elif (row[6].value == "FAIL"):
							moduleEnroll.status = "FAIL"
						elif (row[6].value == "ABSENT"):
							moduleEnroll.status = "ABSENT"
						elif (row[6].value == "PASS BY COMPENSATION"):
							moduleEnroll.status = "PASS BY COMPENSATION"
						elif (row[6].value == "DID NOT COMPLETE"):
							moduleEnroll.status = "DID NOT COMPLETE"
						elif (row[6].value == "EXEMPTION"):
							moduleEnroll.status = "EXEMPTION"
						elif (row[6].value == "SATISFACTORY"):
							moduleEnroll.status = "SATISFACTORY"

						# Marks received
						if (row[5].value != ""): 
							moduleEnroll.marksReceived = row[5].value
						else:
							moduleEnroll.marksReceived = 0

						self.moduleEnrollments.append(moduleEnroll)

						# And add to the list of modules of a particular student
						self.intakeSummer[str(int(row[3].value))].modules.append(moduleEnrolled)
						# Also, add module enrollment to the student
						self.intakeSummer[str(int(row[3].value))].moduleEnrollments[row[4].value] = moduleEnroll


				# Autumn intake
				tempSet.clear()
				linesIgnoreIntakeAutumn = [0, 1, 2, 3, 4, 5, 6] # Lines to ignore in the file
				sheetIntakeAutumn = fileIntakeAutumn.sheet_by_index(0) # Reading the sheet with UG
				numRowsIntakeAutumn = sheetIntakeAutumn.nrows - 1

				for i in range(numRowsIntakeAutumn):
					row = sheetIntakeAutumn.row_slice(i+1)
					if (i + 1 not in linesIgnoreIntakeAutumn and row[2].value == 1): # Limit to result from only the first year
						if (str(row[3]) not in tempSet): 
							self.intakeAutumn[str(int(row[3].value))] = model.Student(str(int(row[3].value)))
							
							# Leaving certificate
							if (int(row[11].value) <= 625):
								self.intakeAutumn[str(int(row[3].value))].leavingCertificate = int(row[11].value) # Leaving certificate from Wrs column
							else:
								if (int(row[12].value) <= 625): # Check if the value is still correct
									self.intakeAutumn[str(int(row[3].value))].leavingCertificate = int(row[12].value) # Leaving certificate from Random column
								else: # The value is not real leaving certificate -> assign to a random value
									self.intakeAutumn[str(int(row[3].value))].leavingCertificate = random.randint(250, 625) # Leaving certificate from Random column

							# Faculty
							self.decideFaculty(str(row[1].value), self.intakeAutumn[str(int(row[3].value))]) # Call a separate function, as there are a lot of programs

							tempSet.add(str(row[3]))

						## Enrol student into a module
						# Default to the second semester of a given year

						# Try to find a previously loaded module
						try:
							moduleEnrolled = self.modules[row[4].value]
						except KeyError, e: # If not found, add a new entry
							moduleEnrolled = model.Module(
								row[2].value, # Module ID
								"", # Module name
								0, # Module credit
								row[2].value * 2, # Semester given
								None, # Department
								None # Enrolled Students
								) #TODO add more accurate information

							# And add to the list of modules
							self.modules[row[2].value] = moduleEnrolled
						# And module enrollment
						moduleEnroll = model.ModuleEnrollment(self.intakeAutumn[str(int(row[3].value))], moduleEnrolled, 2)

						# PASS / FAIL / ABSENT / PASS BY COMPENSATION etc.
						if (row[6].value == "PASS"): 
							moduleEnroll.status = "PASS"
						elif (row[6].value == "FAIL"):
							moduleEnroll.status = "FAIL"
						elif (row[6].value == "ABSENT"):
							moduleEnroll.status = "ABSENT"
						elif (row[6].value == "PASS BY COMPENSATION"):
							moduleEnroll.status = "PASS BY COMPENSATION"
						elif (row[6].value == "DID NOT COMPLETE"):
							moduleEnroll.status = "DID NOT COMPLETE"
						elif (row[6].value == "EXEMPTION"):
							moduleEnroll.status = "EXEMPTION"
						elif (row[6].value == "SATISFACTORY"):
							moduleEnroll.status = "SATISFACTORY"

						# Marks received
						if (row[5].value != ""): 
							moduleEnroll.marksReceived = row[5].value
						else:
							moduleEnroll.marksReceived = 0

						self.moduleEnrollments.append(moduleEnroll)

						# And add to the list of modules of a particular student
						self.intakeAutumn[str(int(row[3].value))].modules.append(moduleEnrolled)
						# Also, add module enrollment to the student
						self.intakeAutumn[str(int(row[3].value))].moduleEnrollments[row[4].value] = moduleEnroll

				update = 'Data imported'
				update += "\n" +  'SUMMER INTAKE length:' + str(len(self.intakeSummer))

				# # Print student IDs
				# keys = self.intakeSummer.keys()
				# keys.sort()
				# for key in keys:
				# 	update += "\n" +  self.intakeSummer[key].studentID

				update += "\n" +  'AUTUMN INTAKE length:' + str(len(self.intakeAutumn))       
				update += "\n" +  'COURSES       length:' + str(len(self.courses))   
				update += "\n" +  'COURSE TYPES  length:' + str(len(self.courseTypes))
				update += "\n" +  'MODULES       length:' + str(len(self.modules))     
				update += "\n" +  'FACULTIES     length:' + str(len(self.faculties))        
				update += "\n" +  'DEPARTMENTS   length:' + str(len(self.departments))
				
				# Calculate an average number of enrolled modules per student
				keys = self.intakeSummer.keys()
				numModulesEnrolled = 0
				for key in keys:
					numModulesEnrolled += len(self.intakeSummer[key].getModules())

				keys = self.intakeAutumn.keys()
				for key in keys:
					numModulesEnrolled += len(self.intakeAutumn[key].getModules())
				numModulesEnrolled /= (len(self.intakeSummer.keys()) + len(self.intakeAutumn.keys()))
				update += "\n" +  'STUDENTS average enrolled modules:' + str(numModulesEnrolled)

				update += "\n" +  'SUMMER'
				passedList = []
				failedList = []
				compensationList = []
				absentList = []
				didnotcompleteList = []
				excemptionList = []
				satisfactoryList = []
				for i in self.moduleEnrollments:
					if (i.semesterTaken == 1):
						if (i.status == "PASS"):
							passedList.append(i)
						elif (i.status == "FAIL"):
							failedList.append(i)
						elif (i.status == "PASS BY COMPENSATION"):
							compensationList.append(i)
						elif (i.status == "ABSENT"):
							absentList.append(i)
						elif (i.status == "DID NOT COMPLETE"):
							didnotcompleteList.append(i)
						elif (i.status == "EXEMPTION"):
							excemptionList.append(i)
						elif (i.status == "SATISFACTORY"):
							satisfactoryList.append(i)
				update += "\n" +  'Passed:' + str(len(passedList))
				update += "\n" +  'Failed:' + str(len(failedList))
				update += "\n" +  'Passed by compensation:' + str(len(compensationList))
				update += "\n" +  'Absent:' + str(len(absentList))
				update += "\n" +  'Did not complete:' + str(len(didnotcompleteList))
				update += "\n" +  'Excempt:' + str(len(excemptionList))
				update += "\n" +  'Satisfactory:' + str(len(satisfactoryList))

				update += "\n" +  'AUTUMN'
				passedList = []
				failedList = []
				compensationList = []
				absentList = []
				didnotcompleteList = []
				excemptionList = []
				satisfactoryList = []
				for i in self.moduleEnrollments:
					if (i.semesterTaken == 2):
						if (i.status == "PASS"):
							passedList.append(i)
						elif (i.status == "FAIL"):
							failedList.append(i)
						elif (i.status == "PASS BY COMPENSATION"):
							compensationList.append(i)
						elif (i.status == "ABSENT"):
							absentList.append(i)
						elif (i.status == "DID NOT COMPLETE"):
							didnotcompleteList.append(i)
						elif (i.status == "EXEMPTION"):
							excemptionList.append(i)
						elif (i.status == "SATISFACTORY"):
							satisfactoryList.append(i)

				update += "\n" +  'Passed:' + str(len(passedList))
				update += "\n" +  'Failed:' + str(len(failedList))
				update += "\n" +  'Passed by compensation:' + str(len(compensationList))
				update += "\n" +  'Absent:' + str(len(absentList))
				update += "\n" +  'Did not complete:' + str(len(didnotcompleteList))
				update += "\n" +  'Excempt:' + str(len(excemptionList))
				update += "\n" +  'Satisfactory:' + str(len(satisfactoryList))

				if conf.DEBUG:
					print update

				for i in self.faculties:
					print i.name

				return update
			except:
				print traceback.format_exc()

	## Add a name of the faculty that a student is enrolled in, based on the name of the programme
	def decideFaculty(self, programme, student):
		if str(programme) == "ARTS (ANTHROPOLOGY) SINGLE HONOURS":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "MATHEMATICS":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "ARTS - SINGLE HONOURS":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "ANTHROPOLOLGY - INTERNATIONAL":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "INTERNATIONAL FINANCE & ECONOMICS":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY" # ?
		elif str(programme) == "MEDIA STUDIES - INTERNATIONAL":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "MULTIMEDIA - INTERNATIONAL":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "MUSIC TECHNOLOGY - INTERNATIONAL":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "BA INTERNATIONAL DEGREE":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "POLITICS INTERNATIONAL":
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "BUSINESS & MANAGEMENT INTERNATIONAL":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "BIOLOGICAL AND BIOMEDICAL SCIENCES":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "SCIENCE (BIOTECHNOLOGY)":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "B.B.S. BUSINESS & MANAGEMENT":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "B.B.S. BUSINESS & ACCOUNTING":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "B.B.S. BUSINESS & ACCOUNTING INTERNATION":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "BGENETICS & BIOINFORMATICS":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "COMPUTATIONAL THINKING":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "COMPUTER SCI & SOFTWARE ENG (ARTS)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "COMPUTER SCI.& SOFTWARE ENGINEERING":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "BA COMMUNITY & YOUTH WORK":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "BA COMMUNITY & YOUTH WORK P/T":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "PRODUCT DESIGN (MARKETING & INNOVATION)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "DIGITAL MEDIA":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "BA IN EARLY CHILDHOOD - TEACHING & LEARN":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "BACHELOR OF EDUCATION":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "BACHELOR OF EDUCATION":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "B.B.A. BUSINESS & ACCOUNTING":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "ENGINEERING":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "ELECTRONIC ENGINEER. WITH COMMUNICATIONS":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "ELECTRONIC ENGINEERING WITH COMPUTERS":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "ELECTRONIC ENGINEERING":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "ARTS (ENGLISH)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "B.B.S. EQUINE BUSINESS":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "B.B.A. EQUINE BUSINESS":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "B.B.S. EQUINE BUSINESS INTERNATIONAL":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "EUROPEAN STUDIES":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY" # ?
		elif str(programme) == "ARTS (FINANCE)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "ARTS(FINANCE) MAJOR/MINOR":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "ACCOUNTING & FINANCE":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY" # ?
		elif str(programme) == "ARTS (GEOGRAPHY)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "ARTS (HISTORY)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "LL.B. LAW":
			student.faculty = "SOCIAL SCIENCES" # ? 
		elif str(programme) == "LL.B. LAW WITH PLACEMENT": 
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "LAW AND ARTS":
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "LAW AND ARTS INTERNATIONAL":
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "LAW & ARTS INTERNATIONAL WITH PLACEMENT":
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "LAW AND MINOR ARTS":
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "LAW AND ARTS WITH PLACEMENT":
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "LAW AND BUSINESS":
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "LAW AND BUSINESS WITH PLACEMENT":
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "B.B.S. MARKETING":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "MATHEMATICS EDUCATION":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "MEDIA STUDIES":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "ARTS (MULTIMEDIA)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "MUSIC HONOURS":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "MUSIC TECHNOLOGY":
			student.faculty = "SCIENCE AND ENGINEERING" # ?
		elif str(programme) == "PHARMACEUTICAL AND BIOMEDICAL CHEMISTRY":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "PHYSICS WITH ASTROPHYSICS":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "PHYSICS WITH ASTROPHYSICS INTERNATIONAL":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "ARTS (POLITICS)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "PHILOSOPHY,POLITICS & ECONOMICS":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "ARTS (PSYCHOLOGY)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "BA (PUBLIC POLICY)":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "SCIENCE EDUCATION":
			student.faculty = "SOCIAL SCIENCES" # ?
		elif str(programme) == "SCIENCE HONOURS":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "SCIENCE HONOURS ACCELERATED":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "THEORETICAL PHYSICS & MATHEMATICS":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "SCIENCE SINGLE HONOURS":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "SCIENCE MULTIMEDIA":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "MULTIMEDIA, MOBILE & WEB DEVELOPMENT":
			student.faculty = "SCIENCE AND ENGINEERING"
		elif str(programme) == "SOCIAL SCIENCE":
			student.faculty = "SOCIAL SCIENCES"
		elif str(programme) == "THEOLOGY":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "FINANCE & VENTURE MANAGEMENT":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "ENTREPRENEURSHIP":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		elif str(programme) == "ENTREPRENEURSHIP WITH PLACEMENT":
			student.faculty = "ARTS,CELT.STUD. AND PHILOSOPHY"
		else:
			student.faculty = "N/A"

	# Based on http://stackoverflow.com/questions/5731670/simple-random-name-generator-in-python/5732034#5732034
	def createIntake(self):
		# Fetch lists of names
		parts = {}
		with open(conf.FILE_WITH_NAMES, 'r') as f:
			nameList = []
			for line in f.readlines():
				line = line.strip()
				if line.startswith('[') and line.endswith(']'):
					nameList = []
					parts[line[1:-1]] = nameList
				else:
					nameList.append(line.strip())

		i = 0

		# Create student instances
		for count in xrange(conf.INTAKE_SIZE):
			name = ' '.join(random.choice(parts[partName]) for partName in sorted(parts))

			gender = random.choice(["m", "f"])
			studentID = i
			i = i + 1
			s = model.Student(studentID, name, gender)
			intake.append(s)

		# for x in intake:
		# 	print x.name, x.gender, x.studentID

	# Open either Excel of CSV file with data
	def openDataFile(self, path):
		try:
			return open_workbook(path)
		except:
			return open(path, 'r')
		return None
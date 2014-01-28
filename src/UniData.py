import traceback
from xlrd import open_workbook, cellname
import csv
import model
import conf

class UniData():
	intakeSummer = {}
	intakeAutumn = {}
	courses = []
	courseTypes = []
	modules = {}
	moduleEnrollments = []
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
				fileCourses = self.openDataFile(conf.FILE_WITH_COURSES)
				fileModules = self.openDataFile(conf.FILE_WITH_MODULES)
				fileIntakeSummer = self.openDataFile(conf.FILE_WITH_INTAKE_SUMMER)
				fileIntakeAutumn = self.openDataFile(conf.FILE_WITH_INTAKE_AUTUMN)

				
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


				# Autumn intake
				tempSet.clear()
				linesIgnoreIntakeAutumn = [0, 1, 2, 3, 4, 5, 6] # Lines to ignore in the file
				sheetIntakeAutumn = fileIntakeAutumn.sheet_by_index(0) # Reading the sheet with UG
				numRowsIntakeAutumn = sheetIntakeAutumn.nrows - 1

				for i in range(numRowsIntakeAutumn):
					row = sheetIntakeAutumn.row_slice(i+1)
					if (i + 1 not in linesIgnoreIntakeAutumn and row[2].value == "1"): # Limit to result from only the first year
						if (str(row[3]) not in tempSet): 
							self.intakeAutumn[str(int(row[3].value))] = model.Student(str(int(row[3].value)))
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
						




				if conf.DEBUG:
					print 'Data imported'
					print 'SUMMER INTAKE length:', len(self.intakeSummer)   

					# # Print student IDs
					# keys = self.intakeSummer.keys()
					# keys.sort()
					# for key in keys:
					# 	print self.intakeSummer[key].studentID

					print 'AUTUMN INTAKE length:', len(self.intakeAutumn)          
					print 'COURSES       length:', len(self.courses)         
					print 'COURSE TYPES  length:', len(self.courseTypes)          
					print 'MODULES       length:', len(self.modules)          
					print 'FACULTIES     length:', len(self.faculties)        
					print 'DEPARTMENTS   length:', len(self.departments)   

					print 'SUMMER'
					print '1st YEAR'
					passedList = []
					failedList = []
					compensationList = []
					absentList = []
					didnotcompleteList = []
					excemptionList = []
					satisfactoryList = []
					for i in self.moduleEnrollments:
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
					print 'STUDENTS                   passed:', len(passedList)
					print 'STUDENTS                   failed:', len(failedList)
					print 'STUDENTS   passed by compensation:', len(compensationList)
					print 'STUDENTS                   absent:', len(absentList)
					print 'STUDENTS         did not complete:', len(didnotcompleteList)
					print 'STUDENTS                  excempt:', len(excemptionList)
					print 'STUDENTS             satisfactory:', len(satisfactoryList)


			except:
				print traceback.format_exc()

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
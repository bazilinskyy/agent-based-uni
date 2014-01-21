import traceback
from xlrd import open_workbook, cellname, XL_CELL_TEXT
import csv
import model
import conf

class UniData():
	intakeSummer = []
	intakeAutumn = []
	courses = []
	modules = []

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
		# TODO populate with real courses
		#_courses = [model.Course("CS101", 10), model.Course("AA104", 5), model.Course("DC105", 5), model.Course("CS110", 15), model.Course("IT402", 10)]
		
		# Populate  
		if (len(self.courses) < 1 and len(self.modules) < 1 and len(self.intakeSummer) < 1 and len(self.intakeAutumn) < 1): # import from files only once
			try:
				## Opening the excel or csv file
				fileCourses = self.openDataFile(conf.FILE_WITH_COURSES)
				fileModules = self.openDataFile(conf.FILE_WITH_MODULES)
				fileIntakeSummer = self.openDataFile(conf.FILE_WITH_INTAKE_SUMMER)
				fileIntakeAutumn = self.openDataFile(conf.FILE_WITH_INTAKE_AUTUMN)
				## Reading the sheet we need
				sheetCourses = fileCourses.sheet_by_index(0)
				sheetModules = fileModules.sheet_by_index(0)
				#sheetIntakeSummer = fileIntakeSummer.sheet_by_index(0)
				sheetIntakeAutumn = fileIntakeAutumn.sheet_by_index(0)
				## Calculating numbers of rows in received sheets
				numRowsCourses = sheetCourses.nrows - 1
				numRowsModules = sheetModules.nrows - 1
				#numRowsIntakeSummer = sheetIntakeSummer.nrows - 1
				numRowsIntakeAutumn = sheetIntakeAutumn.nrows - 1

				## Looping over sheet rows
				## We already know the number of rows
				for i in range(numRowsCourses):
					row = sheetCourses.row_slice(i+1)
					pass

				if conf.DEBUG:
					print 'Data imported'
					print 'SUMMER INTAKE length:', len(self.intakeSummer)          
					print 'AUTUMN INTAKE length:', len(self.intakeAutumn)          
					print 'COURSES       length:', len(self.courses)          
					print 'MODULES       length:', len(self.modules)          
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
			s = model.Student(name, gender, studentID)
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
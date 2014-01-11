class Course:
	__doc__ = "Course"

	totalSemesters = 8
	modules = []
	students = []

	def __init__(self, courseID, courseCredit):
		self.courseID = courseID
		self.courseCredit = courseCredit

	def getModules(self):
		return self.modules

	def getCourseID(self):
		return self.courseID

	def getCourseCredit(self):
		return self.courseCredit

	def getTotalSemesters(self):
		return self.totalSemesters

	def addModule(self, module):
		self.modules.append(module)

	def addStudent(self, student):
		self.students.append(student)
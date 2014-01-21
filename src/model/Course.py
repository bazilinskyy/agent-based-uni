class Course:
	__doc__ = "Course"

	totalSemesters = 8
	modules = []
	students = []

	def __init__(self, courseID, courseCredit, courseType, accepts = 0, singleHons = 0, jointHons = 0):
		self.courseID = courseID
		self.courseCredit = courseCredit
		self.courseType = courseType
		self.accepts = accepts
		self.singleHons = singleHons
		self.jointHons = jointHons

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
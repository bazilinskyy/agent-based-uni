from Student import Student

class Module:
	__doc__ = "Module"

	students = []

	def __init__(self, moduleID, moduleName, moduleCredit, semesterGiven, department, enrolledStudents):
		self.moduleID = moduleID
		self.moduleName = moduleName
		self.moduleCredit = moduleCredit
		self.semesterGiven = semesterGiven
		self.enrolledStudents = enrolledStudents
		self.students = []

	def addStudent(self, student):
		students.append(student)

	def removeStudent(self, student):
		students.remove(student)

	def getModuleCredit(self):
		return self.moduleCredit

	def getSemesterGiven(self):
		return self.semesterGiven

	def getModuleCreditSum(self):
		return self.moduleCredit * self.enrolledStudents

from Student import Student

class Module:
	__doc__ = "Module"

	students = []

	def __init__(self, moduleID, moduleCredit, semesterGiven):
		self.moduleID = studentID
		self.moduleCredit = moduleCredit
		self.semesterGiven = semesterGiven

	def addStudent(self, student):
		students.append(student)

	def removeStudent(self, student):
		students.remove(student)

	def getModuleCredit(self):
		return self.moduleCredit

	def getSemesterGiven(self):
		return self.semesterGiven

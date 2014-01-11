from Person import Person

#TODO make name private
class Student(Person):
	__doc__ = "Student"

	points = 0
	semester = 0
	totalSemesters = 8
	totalMarks = 0
	modules = []

	def __init__(self, name, gender, studentID):
		self.studentID = studentID
		Person.__init__(self, name, gender)

		self.semester = 1

	def getModules(self):
		return self.modules

	def getCourse(self):
		return self.course

	#TODO
	def canTake(self, module):
		return True

	#TODO
	def hasTaken(self, module):
		return True

	def getSemester(self):
		return self.semester

	def getTotalSemesters():
		return self.totalSemesters

	def getTotalMarks():
		return self.totalMarks
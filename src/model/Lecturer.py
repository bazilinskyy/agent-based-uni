from Person import Person

class Lecturer(Person):
	__doc__ = "Lecturer"

	modules = []

	def __init__(self, name, gender, staffID):
		self.staffID = staffID
		Person.__init__(self, name, gender)

	def getModules(self):
		return self.modules
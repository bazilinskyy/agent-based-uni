from Person import Person

class Lecturer(Person):
	__doc__ = "Person"

	def __init__(self, name, gender, staffID):
		self.staffID = staffID
		Person.__init__(self, name, gender)

	def getStaffID(self):
		return self.staffID

	#TODO add input validation
	def setStaffID(self, staffID):
		self.staffID = staffID
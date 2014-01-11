class Person:
	__doc__ = "Person"

	def __init__(self, name, gender):
		self.name = name
		if self.checkGender(gender):
			self.gender = gender # Values: "m", "f", "na"

	def getName(self):
		return self.name

	#TODO add input validation
	def setName(self, name):
		self.name = name

	def getGender(self):
		return self.gender

	def setGender(self, gender):
		if self.checkGender(gender):
			self.gender = gender # Values: "m", "f", "na"

	def checkGender(self, gender):
		if (gender == "m" or gender == "f" or gender == "na"):
			return True
		else:
			raise ValueError("Gender must be of values: \"m\", \"f\", \"na\"")

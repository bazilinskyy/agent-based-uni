class Person:
	__doc__ = "Person"

	def __init__(self, name, gender):
		self.name = name
		if self.checkGender(gender):
			self._gender = gender # Values: "m", "f", "na"

	@property
	def gender(self):
		return self._gender

	@gender.setter
	def gender(self, value):
		if self.checkGender(value):
			self._gender = gender # Values: "m", "f", "na"

	def checkGender(self, gender):
		if (gender == "m" or gender == "f" or gender == "na"):
			return True
		else:
			raise ValueError("Gender must be of values: \"m\", \"f\", \"na\"")



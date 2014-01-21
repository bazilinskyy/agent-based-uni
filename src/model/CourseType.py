class CourseType():
	__doc__ = "Type of degree, e.g. BA, BEng, BSc"
	possibleCourseTypes = ["BA", "BSc"] #TODO extend to values from http://typesofdegrees.org/

	def __init__(self, name, accepts, singleHons = 0, jointHons = 0):
		if self.checkName(name):
			self._name = name

		self.accepts = accepts
		self.singleHons = singleHons
		self.jointHons = jointHons

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		if self.checkName(value):
			self._name = name # Must be one of possibleCourseTypes

	def checkName(self, name):
		if (name in self.possibleCourseTypes):
			return True
		else:
			raise ValueError("Name must be one of: ", self.possibleCourseTypes)
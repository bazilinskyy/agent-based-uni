class CourseEnrollment(object):
	"""CourseEnrollment"""

	finalGrade = "0"
	marksReceived = 0.0
	creditReceived = 0

	def __init__(self, arg):
		super(CourseEnrollment, self).__init__()
		self.arg = arg

	def getGrade(self):
		return self.finalGrade

	def getMarksReceived(self):
		return self.marksReceived

	def getCreditReceived(self):
		return self.creditReceived
		
class CourseEnrollment(object):
	"""CourseEnrollment"""

	finalGrade = 0.0
	marksReceived = 0.0
	creditReceived = 0

	def __init__(self, student, course):
		self.student = student
		self.course = course

	def getGrade(self):
		return self.finalGrade

	def getMarksReceived(self):
		return self.marksReceived

	def getCreditReceived(self):
		return self.creditReceived
		
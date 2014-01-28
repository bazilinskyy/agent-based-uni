class ModuleEnrollment:
	"""ModuleEnrollment"""

	status = "FAIL"
	marksReceived = 0.0

	def __init__(self, student, module, semesterTaken):
		self.semesterTaken = semesterTaken
		self.student = student
		self.module = module
	
	def getMark(self):
		return self.marksReceived

	def hasPassed(self):
		return self.Autumn

	def getSemesterTaken(self):
		return self.semesterTaken
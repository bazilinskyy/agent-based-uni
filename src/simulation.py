import conf
import model
import random
from UniData import UniData

# Populate list of student in current intake
# Load data from Excel and csv files
data = UniData() 
data.importData()
intake = UniData.intakeSummer #TODO process both intakes
modules = UniData.modules
courses = UniData.courses

# Algorithm by Ronan Reilly 
def simulate():
	#createIntake()
	semester = 1

	# Assume a four year course with two semesters per year
	while (semester <= 8):

		for student in intake:
			# intake
			if (semester == 1):
				course = random.choice(courses)
				course.addStudent(student)
				modules = course.getModules()

				for module in modules:
					if (student.canTake(module) and module.getSemesterGiven() == student.getSemester()):
						module.addStudent(student)
			
			# progress
			modulesTaken = student.getModules()
			for module in modulesTaken:
				result = assess(module, student.getPoints())
				if (result >= 40):
					student.credit += module.getModuleCredit()
					student.marks += result * module.getModuleCredit() / course.getCourseCredit(semester)
				student.semester += 1
		semester += 1

	if conf.DEBUG:
		print "Simulation finished."

	return "SIMULATION FINISHED."
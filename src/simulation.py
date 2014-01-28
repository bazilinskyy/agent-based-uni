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
				course.addStudent(intake[student])
				modules = course.getModules()

				for module in modules:
					if (intake[student].canTake(module) and module.getSemesterGiven() == intake[student].getSemester()):
						module.addStudent(intake[student])
			
			# progress
			modulesTaken = intake[student].moduleEnrollments
			for module in modulesTaken:
				result = modulesTaken[module].marksReceived
				if (result >= 40):
					intake[student].points += modulesTaken[module].module.getModuleCredit()
					intake[student].marks += result * modulesTaken[module].module.getModuleCredit() / course.getCourseCredit()
				intake[student].semester += 1
		semester += 1

	if conf.DEBUG:
		print "Simulation finished."

	return "SIMULATION FINISHED."
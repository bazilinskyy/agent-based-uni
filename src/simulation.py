import conf
import model
import random

# Populate list of student in current intake
intake = []
courses = [model.Course("CS101", 10), model.Course("AA104", 5), model.Course("DC105", 5), model.Course("CS110", 15), model.Course("IT402", 10)]

# Based on http://stackoverflow.com/questions/5731670/simple-random-name-generator-in-python/5732034#5732034
def createIntake():
	# Fetch lists of names
	parts = {}
	with open(conf.FILE_WITH_NAMES, 'r') as f:
		nameList = []
		for line in f.readlines():
			line = line.strip()
			if line.startswith('[') and line.endswith(']'):
				nameList = []
				parts[line[1:-1]] = nameList
			else:
				nameList.append(line.strip())

	i = 0

	# Create student instances
	for count in xrange(conf.INTAKE_SIZE):
		name = ' '.join(random.choice(parts[partName]) for partName in sorted(parts))

		gender = random.choice(["m", "f"])
		studentID = i
		i = i + 1
		s = model.Student(name, gender, studentID)
		intake.append(s)

	# for x in intake:
	# 	print x.name, x.gender, x.studentID

# Algorithm by Ronan Reilly 
def simulate():
	createIntake()
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
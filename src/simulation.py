import conf
import model
import random
from UniData import UniData
import random

# Populate list of student in current intake
# Load data from Excel and csv files
intake = {} 		# Summer intake
intakeAutumn = {} 	# Autumn intake
modules = {}		# All modules, sorted by ID
courses = []		# List of all courses

# Record initial state, with no changes
initial_intake = {} 		# Summer intake
initial_intakeAutumn = {} 	# Autumn intake
initial_modules = {}		# All modules, sorted by ID
initial_courses = []		# List of all courses

# Algorithm by Pavlo Bazilinskyy
def simulate(compensationLevel, compensationThreashold, autoRepeats, transferOfCredits, intelligentAgents):
	# Reset data
	intake = initial_intake
	intakeAutumn = initial_intakeAutumn
	modules = initial_modules
	courses = initial_courses

	# Variables for calculating 
	studentsPassed = 0
	studentsFailed = 0
	studentsPassedByCompensation = 0
	studentsPassedByTransferCredits = 0
	studentsPassedByAutoRepeats = 0
	totalAverageMark = 0.0

	# For calculation of the average leaving certificate
	averageLeavingCert = 0.0

	for student in intake.keys(): # Iterate through all students
		# Define variables to calculate results in modules
		passedModules = 0
		failedModules = 0
		failedModulesList = []
		absentModules = 0
		passByCompensationModules = 0
		excemptionModules = 0
		satisfactoryModules = 0
		didNotCompleteModules = 0

		# Calculate average grade
		averageGrade = 0.0
		for moduleEnr in intake[student].moduleEnrollments:
			# Intelligent agent behaviour
			grade = intake[student].moduleEnrollments[moduleEnr].marksReceived
			# print "1: ", grade, " plus: ", conf.INTELLENT_AGENT_COEF * intake[student].leavingCertificate
			# Add marks based on the leaving school certificate mark, based on probability of exhibiting intellgent behaviour INTELLENT_AGENT_CHANGE
			if random.random() <= conf.INTELLENT_AGENT_CHANGE and intake[student].leavingCertificate >= conf.INTELLENT_AGENT_LC_THRESHOLD:
				grade += conf.INTELLENT_AGENT_COEF * intake[student].leavingCertificate
				intake[student].moduleEnrollments[moduleEnr].marksReceived = grade
				# Check if it makes a failed module passed
				if ((intake[student].moduleEnrollments[moduleEnr].status == "FAIL" or
					intake[student].moduleEnrollments[moduleEnr].status == "PASS BY COMPENSATION") and 
					averageGrade >= conf.COMPENSATION_THREASHOLD and 
					intake[student].moduleEnrollments[moduleEnr].marksReceived <= conf.COMPENSATION_LEVEL):
					print "PASSED"
					intake[student].moduleEnrollments[moduleEnr].status == "PASS"

			# Average grade calculation
			averageGrade += intake[student].moduleEnrollments[moduleEnr].marksReceived
		averageGrade /= len(intake[student].moduleEnrollments)
		totalAverageMark += averageGrade

		# Calculating average leaving certificate
		averageLeavingCert += intake[student].leavingCertificate

		for moduleEnr in intake[student].moduleEnrollments: # Iterate through all enrolled modules for each student
			#First check if pass by compesation still holds
			moduleEnr = intake[student].moduleEnrollments[moduleEnr]
			if (moduleEnr.status == "PASS BY COMPENSATION"):
				if (averageGrade < conf.COMPENSATION_THREASHOLD or 
					moduleEnr.marksReceived < conf.COMPENSATION_LEVEL or 
					conf.PASS_BY_COMPENSATION == False):
					moduleEnr.status = "FAIL"

			if (moduleEnr.status == "PASS"): 
				passedModules += 1
			elif (moduleEnr.status == "FAIL"):
				failedModules += 1
				failedModulesList.append(moduleEnr)
			elif (moduleEnr.status == "ABSENT"):
				absentModules += 1
			elif (moduleEnr.status == "PASS BY COMPENSATION"):
				passByCompensationModules += 1
			elif (moduleEnr.status == "DID NOT COMPLETE"):
				didNotCompleteModules += 1
			elif (moduleEnr.status == "EXEMPTION"):
				excemptionModules += 1
			elif (moduleEnr.status == "SATISFACTORY"):
				satisfactoryModules += 1

		# Found failed modules, and auto repeats are possible
		if (failedModules > 0 and conf.AUTO_REPEATS == True and conf.TRANSFER_OF_CREDITS == False):
			modulesPassedByAutoRepeats = False
			# Find this student in autumn intake
			if (intake[student].studentID in intakeAutumn.keys()):
					for moduleEnr in intake[student].moduleEnrollments:
						moduleEnr = intake[student].moduleEnrollments[moduleEnr]
						# Iterate through failed modules
						if (moduleEnr.module.moduleID in intakeAutumn[intake[student].studentID].moduleEnrollments.keys()):
							# Check new status of the module after it was retaken
							modEnrAutumn = intakeAutumn[intake[student].studentID].moduleEnrollments[moduleEnr.module.moduleID]
							if (modEnrAutumn.status == "PASS"): 
								passedModules += 1
								failedModules -= 1
								modulesPassedByAutoRepeats = True

							# elif (intakeAutumn[intake[student].studentID].moduleEnrollments[moduleEnr.module.moduleID] == "FAIL"):
							# 	failedModules += 1
							# 	failedModulesList.append(moduleEnr)
							# elif (intakeAutumn[intake[student].studentID].moduleEnrollments[moduleEnr.module.moduleID] == "ABSENT"):
							# 	absentModules += 1
							elif (modEnrAutumn.status == "PASS BY COMPENSATION"):
									if (averageGrade >= conf.COMPENSATION_THREASHOLD or modEnrAutumn.marksReceived >= conf.COMPENSATION_LEVEL):
										passByCompensationModules += 1
										failedModules -= 1
							elif (modEnrAutumn.status == "DID NOT COMPLETE"):
								didNotCompleteModules += 1
								failedModules -= 1
							elif (modEnrAutumn.status == "EXEMPTION"):
								excemptionModules += 1
								failedModules -= 1
							elif (modEnrAutumn.status == "SATISFACTORY"):
								satisfactoryModules += 1
								failedModules -= 1

			# Student did not retake failed modules
			else:
				studentsFailed += 1
				intake[student].resultFromSimluation = False
				continue

			if (modulesPassedByAutoRepeats):
				studentsPassedByAutoRepeats += 1


		# Pass by compensation modules found, but it was used for more than two modules
		if (passByCompensationModules > 2):
			studentsFailed += 1
			intake[student].resultFromSimluation = False
			continue
		# Student has failed moduels, and both auto repeats and transfer of credits are disabled
		elif (failedModules > 0 and conf.AUTO_REPEATS == False and conf.TRANSFER_OF_CREDITS == False):
			studentsFailed += 1
			intake[student].resultFromSimluation = False
			continue
		# Found failed modules, but auto repeats and transfer of credits are not allowed
		elif (failedModules > 0 and conf.TRANSFER_OF_CREDITS == True and conf.AUTO_REPEATS == False):
			# Calculate how many modules were failed and compare that number 
			# to the number of modules that can be transfered to the next year
			if (failedModules < conf.TRANSFER_OF_CREDITS_MODULES):
				studentsFailed += 1
				intake[student].resultFromSimluation = False
				continue
			else:
				studentsPassedByTransferCredits += 1
		# Student has failed moduels, and both auto repeats and transfer of credits are disabled
		elif (didNotCompleteModules > conf.DID_NOT_COMPLETE_MODULES):
			studentsFailed += 1
			intake[student].resultFromSimluation = False
			continue
		# Everything is fine and this student can advance to the next year
		if (passByCompensationModules <= 2 and passByCompensationModules > 0):
			studentsPassedByCompensation += 1

		# Everything is fine and this student can go to the next year
		studentsPassed += 1
		intake[student].resultFromSimluation = True

	totalAverageMark /= len(intake) # Calculate average grade
	averageLeavingCert /= len(intake) # Calcualte average leaving certificate

	if conf.DEBUG:
		print "Simulation finished."

	update = 'Results:'
	update += "\n" +  'Students passed: ' + str(studentsPassed)
	update += "\n" +  'Students failed: ' + str(studentsFailed)
	update += "\n" +  'Students passed by compensation: ' + str(studentsPassedByCompensation)
	update += "\n" +  'Students passed by transfer of credits: ' + str(studentsPassedByTransferCredits)
	update += "\n" +  'Students passed by auto repeats: ' + str(studentsPassedByAutoRepeats)
	update += "\n" +  'Average grade: ' + str(totalAverageMark)
	update += "\n" +  'Average leaving certificate: ' + str(averageLeavingCert)

	if conf.DEBUG:
		print update

	return update


# Algorithm by Ronan Reilly and Pavlo Bazilinskyy
def simulate_old(compensationLevel, compensationThreashold, autoRepeats, transferOfCredits):
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
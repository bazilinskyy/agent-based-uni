# ENVIRONMENT
DEBUG				= 1
SHOW_TIMESTAMPS 	= 1
KIVY_READY 			= 1		# Ready to be published with Kivy

# SIMULATION
INTELLIGENT_AGENTS 				= True 		# Agent exhibit intelligent behaviour based on their school leaving certificated
INTELLENT_AGENT_COEF			= 0.02  	# By how many percent agents are more clever 
INTELLENT_AGENT_CHANGE			= 0.8  		# What is a chance of the agent exhibiting intelligent behaviour. 1.0 - always intelligent
INTELLENT_AGENT_LC_THRESHOLD	= 600		# Appluy intelligent behaviour only if leaving certificate is higher that this number
INTAKE_SIZE 					= 500  # Not used
COMPENSATION_LEVEL 				= 25
COMPENSATION_THREASHOLD 		= 50
AUTO_REPEATS 					= True
AUTO_REPEATS_LIMIT				= 999 # Missing information, set to very large numer
TRANSFER_OF_CREDITS				= False
TRANSFER_OF_CREDITS_MODULES		= 2 # How many modules can be transfered
PASS_BY_COMPENSATION			= True
SEMESTER_FINISH					= 2
DID_NOT_COMPLETE_MODULES		= 0 # How many modules can be unfinished

# FILES WITH DATA
FILE_WITH_NAMES = "names.txt"
FILE_WITH_INTAKE_SUMMER = "data/curriculum_raw_Data_Summer_allYrs-Leaving Cert Pts.xlsx"
FILE_WITH_INTAKE_AUTUMN = "data/curriculum_raw_Data_Autumn_allYrs-Leaving Certs-Leaving Cert Pts.xlsx"
FILE_WITH_COURSES = "data/NUIM degrees.xlsx"
FILE_WITH_MODULES = "data/UG and PG summary no intoc no period study.xlsx"

# GUI
LABEL_VALUE_COLOR = "ff3333"
LABEL_GREEN_COLOR = "ff3333"
LABEL_RED_COLOR = "ff3333"
LABEL_ORANGE_COLOR = "ff3333"
#!/usr/bin/env python
"""
List pf parameters used in the application.
"""
# Copyright (c) 2014, Pavlo Bazilinskyy <pavlo.bazilinskyy@gmail.com>
# Department of Computer Science, National University of Ireland, Maynooth
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
__author__ = "Pavlo Bazilinskyy"
__copyright__ = "Copyright 2008, National University of Ireland, Maynooth"
__credits__ = "Ronan Reilly"
__version__ = "1.0"
__maintainer__ = "Pavlo Bazilinskyy"
__email__ = "pavlo.bazilinskyy@gmail.com"
__status__ = "Production"

# ENVIRONMENT
DEBUG				= 0		# 1 - show debugging information, 0 - do not show debugging information
DETAILED_DEBUG		= 1		# 1 - show detailed debugging information, 0 - do not show detailed debugging information
SHOW_TIMESTAMPS 	= 0		# Show timestamps with debuggin information
KIVY_READY 			= 1		# Ready to be published with Kivy

# SIMULATION
NORMALISE_VALUES				= True
USE_SMALL_DATA					= False		# Use data with small intake for testing
PASSING_THRESHOLD				= 40		# Passing grade
INTELLIGENT_AGENTS 				= True 		# Agent exhibit intelligent behaviour based on their school leaving certificated
INTELLENT_AGENT_COEF			= 5 	  	# If an agent exhibits intelligent behaviour, his modules receive additional (INTELLENT_AGENT_COEF / 1000 * LeavingCertificate) marks
											# e.g. if INTELLENT_AGENT_COEF = 5 => grade:  46.0 + 4.995
INTELLENT_AGENT_CHANCE			= 0.81 		# What is a chance of the agent exhibiting intelligent behaviour. 1.0 - always intelligent
INTELLENT_AGENT_LC_THRESHOLD	= 600		# Apply intelligent behaviour only if leaving certificate is higher that this number
INTELLENT_AGENT_ABSENT_MODULE   = True      # Intelligent agent with an average grade > INTELLENT_AGENT_ABSENT_MODULE_THRESHOLD can pass an absent module
INTELLENT_AGENT_ABSENT_MODULE_THRESHOLD = 50 # There is INTELLENT_AGENT_CHANGE/2 chance to pass a module with a grade = average grade, if average grade of the student > INTELLENT_AGENT_ABSENT_MODULE_THRESHOLD
INTAKE_SIZE 					= 500  		# Not used
COMPENSATION_LEVEL 				= 25		# Level for using pass by compensation
COMPENSATION_THREASHOLD 		= 50		# Average grade threshold for using pass by compensation
AUTUMN_REPEATS 					= False  	# Enable auto repeats
AUTUMN_REPEATS_LIMIT			= 10 		# Autumn repeats can be used for a AUTUMN_REPEATS_LIMIT number of credit
TRANSFER_OF_CREDITS				= False  	# Enable transfer of credits
TRANSFER_OF_CREDITS_MODULES		= 2 		# How many modules can be transfered
PASS_BY_COMPENSATION			= True  	# Enable pass by compensation
SEMESTER_FINISH					= 2 		# How many semesters to process in simulation
DID_NOT_COMPLETE_MODULES		= 0 		# How many modules can be unfinished

# GRAPHS
GRAPH_ROUND						= 10 		# Round values to 10, 100 etc. for smoothing graphs

# FILES WITH DATA
FILE_WITH_NAMES = "names.txt" # Not used
FILE_WITH_INTAKE_SUMMER = "data/curriculum_raw_Data_Summer_allYrs-Leaving Cert Pts.xlsx"
FILE_WITH_INTAKE_AUTUMN = "data/curriculum_raw_Data_Autumn_allYrs-Leaving Certs-Leaving Cert Pts.xlsx"
FILE_WITH_COURSES = "data/NUIM degrees.xlsx"
FILE_WITH_MODULES = "data/UG and PG summary no intoc no period study.xlsx"

# SMALL SAMPLE WITH DATA FOR TESTING
SMALL_FILE_WITH_INTAKE_SUMMER = "data/small_sample/curriculum_raw_Data_Summer_allYrs-Leaving Cert Pts.xlsx"
SMALL_FILE_WITH_INTAKE_AUTUMN = "data/small_sample/curriculum_raw_Data_Autumn_allYrs-Leaving Certs-Leaving Cert Pts.xlsx"
SMALL_FILE_WITH_COURSES = "data/small_sample/NUIM degrees.xlsx"
SMALL_FILE_WITH_MODULES = "data/small_sample/UG and PG summary no intoc no period study.xlsx"

# GUI
LABEL_VALUE_COLOR = "ff3333" # Color for values in labeles shown in the sidebar in GUI
LABEL_GREEN_COLOR = "ff3333"
LABEL_RED_COLOR = "ff3333"
LABEL_ORANGE_COLOR = "ff3333"
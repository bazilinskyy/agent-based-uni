import unittest, os, sys
lib_path = os.path.abspath('../../src')
sys.path.append(lib_path)

import model

# Lecturer class
class Lecturer(unittest.TestCase):

	def setUp(self):
		self.l =  model.Lecturer("Bob Fisher", "m", "1234567")

	# Constructor
	def test1(self):
		self.assertEqual(self.l.name, "Bob Fisher")
		self.assertEqual(self.l.gender, "m")
		self.assertEqual(self.l.staffID, "1234567")

	# getModules
	def test2(self):
		self.assertEqual(len(self.l.getModules()), 0)

# Person class
class Person(unittest.TestCase):

	def setUp(self):
		self.p =  model.Lecturer("Bob Fisher", "m", "1234567")

	# Constructor
	def test1(self):
		self.assertEqual(self.p.name, "Bob Fisher")
		self.assertEqual(self.p.gender, "m")

# CourseType class
class CourseType(unittest.TestCase):

	def setUp(self):
		self.ct =  model.CourseType("BSc", 1400, 340, 210)

	# Constructor
	def test1(self):
		self.assertEqual(self.ct.name, "BSc")
		self.assertEqual(self.ct.accepts, 1400)
		self.assertEqual(self.ct.singleHons, 340)
		self.assertEqual(self.ct.jointHons, 210)

def main():
	unittest.main()

if __name__ == '__main__':
	main()
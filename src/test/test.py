#!/usr/bin/env python
"""
Attempt to use TTD...
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
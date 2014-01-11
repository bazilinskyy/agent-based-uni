import unittest, os, sys
lib_path = os.path.abspath('../../src')
sys.path.append(lib_path)

import model

# Here's our "unit tests".
class Lecturer(unittest.TestCase):

	# Consturctor
    def test1(self):
    	lec =  model.Lecturer("Bob Fisher", "m", "1234567")
        self.assertEqual(lec.getName(), "Bob Fisher")
        self.assertEqual(lec.getGender(), "m")
        self.assertEqual(lec.getStaffID(), "1234567")

def main():
    unittest.main()

if __name__ == '__main__':
    main()
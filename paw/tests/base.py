import unittest
import paw


class paw_test(unittest.TestCase):
    def setUp(self):
        self.paw = paw.Paw()
        self.w1 = [["A", "B", "C"], ["1", "2", "3"]]
        self.w2 = [["A"], ["1", "2", "3"]]
        self.w3 = 'a'
        self.no_duplicates = [["A", "A"], ["1", "1"]]
        self.badchar = chr(0)
        self.tfilepath = 'paw/tests/test_files/tmp'
        self.tfile = open(self.tfilepath, 'w')
        self.tfile.close()
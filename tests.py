import unittest
from paw import paw

class paw_test(unittest.TestCase):

    def setUp(self):
        self.paw = paw()
        self.w1 = [["A", "B", "C"], ["1", "2", "3"]]
        self.w2 = [["A"], ["1","2","3"]]
        self.no_duplicates = [["A","A"] ,["1", "1"]]
        self.badchar = chr(0)

    def test_generate_wordlist(self):
        # Set the arguments

        words1 = self.paw.gen_wordlist(self.w1)
        words2 = self.paw.gen_wordlist(self.w2)

        self.assertEqual(words1, ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], "test successfull")
        self.assertEqual(words2, ["A1","A2","A3"])

    def test_generate_wordlist_no_duplicates(self):
        self.paw.args.gensets = True
        no_duplicates = self.paw.gen_wordlist(self.no_duplicates)
        self.assertEqual(no_duplicates, ["A1"])

    def test_generate_wordlist_from_file_no_duplicates(self):
        self.paw.args.infile = "test_files/gen_words_sample.txt"
        self.paw.args.custsets = True
        self.paw.gen_charset()
        words3 = self.paw.gen_wordlist(self.paw.cset)
        self.assertEqual(words3, ["B1"])

    def test_passwords_simple(self):
        self.paw.args.pattern = True
        self.paw.args.infile = "test_files/test_pw.txt"
        self.paw.from_passwords()
        (key, value), = self.paw.patterns.items()
        self.assertEqual(key, 8)
        value = "".join(value)
        self.assertEqual(value, "%hl%di%lu%dl%dl%d%di%dh")

    def test_passwords_all(self):
        self.paw.args.pattern = True
        self.paw.args.infile = "test_files/test_pw_all_std.txt"
        self.paw.from_passwords()
        (key, value), = self.paw.patterns.items()
        value= "".join(value)
        self.assertEqual(5, key)
        self.assertEqual(value, "%h%i%d%s%s")

    def test_warning_badchars(self):
        self.paw.cset_lookup(self.badchar)
        self.assertEqual(1, self.paw.wcount)

    def test_error_c_and_g(self):
        self.paw.args.custsets = True
        self.paw.args.gensets = True
        with self.assertRaises(SystemExit) as value:
            self.paw.gen_charset()
        self.assertEqual(value.exception.code, None)

if __name__ == '__main__':
    unittest.main()


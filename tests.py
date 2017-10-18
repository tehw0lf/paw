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

    def test_parse_cset(self):
        self.paw.args.gensets = "[%dd]"
        self.paw.gen_charset()
        (key, value), = self.paw.cset.items()
        self.assertEqual(value, "0123456789d")

    def test_parse_cset_uneven(self):
        self.paw.args.gensets= '[a'
        self.paw.gen_charset()
        self.assertEqual(self.paw.wcount, 1)

    def test_gen_hcat_cmd_one_h(self):
        self.paw.args.hcat = True
        self.paw.patterns[0] = ['%h']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs, {0: '-a 3 -1 ABCDEF ?1'})

    def test_gen_hcat_cmd_one_dh(self):
        self.paw.args.hcat = True
        self.paw.patterns[0] = ['%dh']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs, {0: '-a 3 -1 0123456789ABCDEF ?1'})

    def test_gen_hcat_cmd_one_di(self):
        self.paw.args.hcat = True
        self.paw.patterns[0] = ['%di']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs, {0: '-a 3 -2 0123456789abcdef ?2'})
        
    def test_gen_hcat_cmd_one_i(self):
        self.paw.args.hcat = True
        self.paw.patterns[0] = ['%i']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs, {0: '-a 3 -2 abcdef ?2'})
        
    def test_gen_hcat_cmd_single(self):
        self.paw.args.hcat = True
        self.paw.patterns[0] = ['%h', '%i', '%d', '%s', '%s']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs,
                         {0: '-a 3 -1 ABCDEF -2 abcdef ?1?2?d?s?s'})
        
    def test_gen_hcat_cmd_multi(self):
        self.paw.args.hcat = True
        self.paw.patterns[0] = ['%h', '%i', '%d', '%s', '%s']
        self.paw.patterns[1] = ['%h', '%i', '%i', '%s', '%u', '%d']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 2)
        self.assertEqual(self.paw.catstrs,
                         {0: '-a 3 -1 ABCDEF -2 abcdef ?1?2?d?s?s',
                          1: '-a 3 -1 ABCDEF -2 abcdef ?1?2?2?s?u?d'})
    
    def test_gen_hcat_cmd_empty_pattern(self):
        self.paw.args.hcat = True
        self.paw.patterns[0] = ['']
        self.paw.gen_hcat_cmd()
        self.assertEqual(self.paw.wcount, 1)
        
if __name__ == '__main__':
    unittest.main()


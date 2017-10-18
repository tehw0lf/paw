import filecmp
import unittest
from paw import paw

class paw_test(unittest.TestCase):

    def setUp(self):
        self.paw = paw()
        self.w1 = [["A", "B", "C"], ["1", "2", "3"]]
        self.w2 = [["A"], ["1","2","3"]]
        self.w3 = 'a'
        self.no_duplicates = [["A","A"] ,["1", "1"]]
        self.badchar = chr(0)
        self.tfilepath = 'test_files/tmp'        
        self.tfile = open(self.tfilepath, 'w')
        self.tfile.close()
    
    # function tests
    
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
        
    def test_gen_wordlist(self):
        words1 = self.paw.gen_wordlist(self.w1)
        words2 = self.paw.gen_wordlist(self.w2)

        self.assertEqual(words1, ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'], "test successfull")
        self.assertEqual(words2, ["A1","A2","A3"])

    def test_gen_wordlist_no_duplicates(self):
        self.paw.args.gensets = True
        no_duplicates = self.paw.gen_wordlist(self.no_duplicates)
        self.assertEqual(no_duplicates, ["A1"])

    def test_gen_wordlist_from_file_no_duplicates(self):
        self.paw.args.infile = "test_files/gen_words_sample.txt"
        self.paw.args.custsets = True
        self.paw.gen_charset()
        words3 = self.paw.gen_wordlist(self.paw.cset)
        self.assertEqual(words3, ["B1"])
        
    def test_parse_cset(self):
        self.paw.args.gensets = "[%dd]"
        self.paw.gen_charset()
        (key, value), = self.paw.cset.items()
        self.assertEqual(value, "0123456789d")

    def test_parse_cset_uneven(self):
        self.paw.args.gensets= '[a'
        self.paw.gen_charset()
        self.assertEqual(self.paw.wcount, 1)        

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

    def test_save_wordlist(self):
        self.paw.args.outfile = self.tfilepath
        self.paw.cset = {0: 'a'}
        self.paw.save_wordlist()
        self.assertTrue(filecmp.cmp(self.paw.args.outfile, 'test_files/test_out'))
        
    def test_save_wordlist_stdout(self):
        self.paw.cset = {0: 'a'}
        self.paw.save_wordlist()
        self.assertEqual(self.w3, self.paw.wlist)

    def test_warning_badchars(self):
        self.paw.cset_lookup(self.badchar)
        self.assertEqual(1, self.paw.wcount)
        
    # command line interface tests

    def test_flag_c(self):
        self.paw.args.infile = "test_files/gen_words_sample.txt"
        self.paw.args.custsets = True
        self.paw.parse_commands()
        words3 = self.paw.gen_wordlist(self.paw.cset)
        self.assertEqual(words3, ["B1"])
        
    def test_flag_c_hcat(self):
        self.paw.args.infile = "test_files/gen_words_sample.txt"
        self.paw.args.custsets = True
        self.paw.args.hcat = True
        self.paw.parse_commands()
        words3 = self.paw.gen_wordlist(self.paw.cset)
        self.assertEqual(words3, ["B1"])
        
    def test_flag_p(self):
        self.paw.args.infile = "test_files/gen_words_sample.txt"
        self.paw.args.pattern = True
        self.paw.parse_commands()
        words4 = self.paw.gen_wordlist(self.paw.cset)
        self.assertEqual(words4, ['11', '1B', 'B1', 'BB'])
        
    def test_flag_p_and_h(self):
        self.paw.args.infile = "test_files/gen_words_sample.txt"
        self.paw.args.pattern = True
        self.paw.args.hcat = True
        self.paw.parse_commands()
        words4 = self.paw.gen_wordlist(self.paw.cset)
        self.assertEqual(words4, ['11', '1B', 'B1', 'BB'])

    def test_flag_error_c_and_g(self):
        self.paw.args.custsets = True
        self.paw.args.gensets = True
        with self.assertRaises(SystemExit) as value:
            self.paw.gen_charset()
        self.assertEqual(value.exception.code, None)

    def test_flag_error_c_and_p(self):
        self.paw.args.custsets = True
        self.paw.args.pattern = True
        with self.assertRaises(SystemExit) as value:
            self.paw.parse_commands()
        self.assertEqual(value.exception.code, None)

    def test_flag_error_g_and_h(self):
        self.paw.args.hcat = True
        self.paw.args.gensets = True
        with self.assertRaises(SystemExit) as value:
            self.paw.parse_commands()
        self.assertEqual(value.exception.code, None)

    def test_flag_error_g_and_p(self):
        self.paw.args.gensets = True
        self.paw.args.pattern = True
        with self.assertRaises(SystemExit) as value:
            self.paw.parse_commands()
        self.assertEqual(value.exception.code, None)

    # warning report tests
    
    def test_report_wcount_one(self):
        self.paw.wcount = 1
        self.paw.parse_commands()
        self.assertEqual(self.paw.report, 'done with 1 warning')
        
    def test_report_wcount_multi(self):
        self.paw.wcount = 2
        self.paw.parse_commands()
        self.assertEqual(self.paw.report, 'done with 2 warnings')
        
if __name__ == '__main__':
    unittest.main(buffer=True)


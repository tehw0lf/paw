from .base import paw_test
import filecmp


class save_wordlist_test(paw_test):
    def test_save_wordlist(self):
        outfile = self.tfilepath
        self.paw.cset = {0: 'a'}
        self.paw.save_wordlist(outfile)
        self.assertTrue(filecmp.cmp(outfile,
                                    'paw/tests/test_files/test_out'))

    def test_save_wordlist_stdout(self):
        self.paw.cset = {0: 'a'}
        self.paw.save_wordlist()
        self.assertEqual(self.w3, self.paw.wlist)

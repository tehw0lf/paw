from .base import paw_test
import filecmp
import mock
import sys


class save_wordlist_test(paw_test):
    def test_save_wordlist(self):
        max_buf = 1
        outfile = self.tfilepath
        self.paw.cset = {0: 'a'}
        self.paw.save_wordlist(outfile, max_buf)
        self.assertTrue(filecmp.cmp(outfile,
                                    'paw/tests/test_files/test_out'))

    def test_save_wordlist_stdout(self):
        mock_stdout = mock.Mock()
        sys.stdout = mock_stdout
        self.paw.cset = {0: 'a'}
        self.paw.save_wordlist()
        sys.stdout = sys.__stdout__

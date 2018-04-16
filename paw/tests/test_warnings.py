from .base import paw_test


class warning_test(paw_test):
    def test_warning_badchars(self):
        self.paw.cset_lookup(self.badchar)
        self.assertEqual(1, self.paw.wcount)

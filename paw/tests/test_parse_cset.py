from .base import paw_test


class parse_cset_test(paw_test):
    def test_parse_cset(self):
        self.paw.gensets = "[%dd]"
        self.paw.parse_cset()
        (key, value), = self.paw.cset.items()
        self.assertEqual(value, "0123456789d")

    def test_parse_cset_uneven(self):
        self.paw.gensets = '[a'
        self.paw.parse_cset()
        self.assertEqual(self.paw.wcount, 1)

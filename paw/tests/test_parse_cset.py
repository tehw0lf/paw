from .base import paw_test


class parse_cset_test(paw_test):
    def test_parse_cset(self):
        self.paw.gensets = "[%dd]"
        self.paw.parse_cset()
        (key, value), = self.paw.cset.items()
        self.assertEqual(value, "0123456789d")

    def test_parse_cset_empty(self):
        self.paw.gensets = "[]"
        with self.assertRaises(SystemExit):
            self.paw.parse_cset()

    def test_parse_cset_lbracket(self):
        self.paw.gensets = "[[]"
        self.paw.parse_cset()
        (key, value), = self.paw.cset.items()
        self.assertEqual(value, "[")

    def test_parse_cset_rbracket(self):
        self.paw.gensets = "[]]"
        self.paw.parse_cset()
        (key, value), = self.paw.cset.items()
        self.assertEqual(value, "]")

from .base import paw_test


class from_password_test(paw_test):
    def test_passwords_simple(self):
        self.paw.pattern = True
        self.paw.infile = "paw/tests/test_files/test_pw.txt"
        self.paw.from_passwords()
        (key, value), = self.paw.patterns.items()
        self.assertEqual(key, 8)
        value = "".join(value)
        self.assertEqual(value, "%hl%di%lu%dl%dl%d%di%dh")

    def test_passwords_all(self):
        self.paw.pattern = True
        self.paw.infile = "paw/tests/test_files/test_pw_all_std.txt"
        self.paw.from_passwords()
        (key, value), = self.paw.patterns.items()
        value = "".join(value)
        self.assertEqual(5, key)
        self.assertEqual(value, "%h%i%d%s%s")

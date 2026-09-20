from .base import paw_test


class gen_custom_charset_test(paw_test):
    """
    `gen_custom_charset` used to store the first character class of a line as a
    plain string and every later one as a set, so from the third distinct
    character on it evaluated `set(...) + str` and raised TypeError. Lines with
    one or two distinct characters happened to work, which is why the existing
    fixture (`BB` / `11`) never caught it.
    """

    SAMPLE = "paw/tests/test_files/custom_charset_sample.txt"

    def test_line_with_three_distinct_characters(self):
        self.paw.infile = self.SAMPLE
        self.paw.gen_custom_charset()

        # a, b and c are all hex lowercase, so the line collapses to one class.
        self.assertEqual(self.paw.patterns[0], "%i")

    def test_classes_are_collected_whole(self):
        self.paw.infile = self.SAMPLE
        self.paw.gen_custom_charset()

        # aA1! spans hex lowercase, hex uppercase, a digit and a symbol. The
        # two-character classes must survive intact rather than be mixed at
        # character level.
        self.assertEqual(self.paw.patterns[1], "%h%ids")

    def test_pattern_is_stable(self):
        self.paw.infile = self.SAMPLE
        self.paw.gen_custom_charset()
        first = dict(self.paw.patterns)

        self.paw.patterns = {}
        self.paw.cset = {}
        self.paw.gen_custom_charset()

        self.assertEqual(first, self.paw.patterns)

    def test_hashcat_command_from_a_custom_charset(self):
        self.paw.infile = self.SAMPLE
        self.paw.gen_custom_charset()
        self.paw.gen_hcat_cmd()

        # The consumer reads the pattern back; a torn class would surface here.
        self.assertEqual(self.paw.catstrs[0], "-a 3 -2 abcdef ?2")
        self.assertEqual(
            self.paw.catstrs[1], "-a 3 -1 0123456789ABCDEF ?1?2?d?s"
        )

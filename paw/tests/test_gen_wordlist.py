from .base import paw_test


class gen_wordlist_test(paw_test):
    def test_gen_wordlist(self):
        words1 = self.paw.gen_wordlist(self.w1)
        words2 = self.paw.gen_wordlist(self.w2)
        self.assertEqual(words1, ['A1', 'A2', 'A3', 'B1', 'B2',
                                  'B3', 'C1', 'C2', 'C3'], "test successful")
        self.assertEqual(words2, ["A1", "A2", "A3"])

    def test_gen_wordlist_no_duplicates(self):
        self.paw.gensets = True
        no_duplicates = self.paw.gen_wordlist(self.no_duplicates)
        self.assertEqual(no_duplicates, ["A1"])

    def test_gen_wordlist_from_file_no_duplicates(self):
        self.paw.infile = "paw/tests/test_files/gen_words_sample.txt"
        self.paw.custsets = True
        self.paw.gen_custom_charset()
        words3 = self.paw.gen_wordlist(self.paw.cset)
        self.assertEqual(words3, ["B1"])

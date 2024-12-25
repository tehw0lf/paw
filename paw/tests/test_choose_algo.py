import wlgen
import paw
from .base import paw_test


class choose_algo_test(paw_test):
    def test_choose_gen_wordlist(self):
        self.paw = paw.Paw(algo=0)
        self.assertTrue(
            self.paw.gen_wordlist.__code__.co_code
            == wlgen.gen_wordlist_iter.__code__.co_code
        )

    def test_choose_gen_wordlist_iter(self):
        self.paw = paw.Paw(algo=1)
        self.assertTrue(
            self.paw.gen_wordlist.__code__.co_code
            == wlgen.gen_wordlist.__code__.co_code
        )

    def test_choose_gen_words(self):
        self.paw = paw.Paw(algo=2)
        self.assertTrue(
            self.paw.gen_wordlist.__code__.co_code
            == wlgen.gen_words.__code__.co_code
        )

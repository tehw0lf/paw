from .base import paw_test


class gen_hcat_test(paw_test):
    def test_gen_hcat_cmd_one_h(self):
        self.paw.hcat = True
        self.paw.patterns[0] = ['%h']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs, {0: '-a 3 -1 ABCDEF ?1'})

    def test_gen_hcat_cmd_one_dh(self):
        self.paw.hcat = True
        self.paw.patterns[0] = ['%dh']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs, {0: '-a 3 -1 0123456789ABCDEF ?1'})

    def test_gen_hcat_cmd_one_di(self):
        self.paw.hcat = True
        self.paw.patterns[0] = ['%di']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs, {0: '-a 3 -2 0123456789abcdef ?2'})

    def test_gen_hcat_cmd_one_i(self):
        self.paw.hcat = True
        self.paw.patterns[0] = ['%i']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs, {0: '-a 3 -2 abcdef ?2'})

    def test_gen_hcat_cmd_single(self):
        self.paw.hcat = True
        self.paw.patterns[0] = ['%h', '%i', '%d', '%s', '%s']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 1)
        self.assertEqual(self.paw.catstrs,
                         {0: '-a 3 -1 ABCDEF -2 abcdef ?1?2?d?s?s'})

    def test_gen_hcat_cmd_multi(self):
        self.paw.hcat = True
        self.paw.patterns[0] = ['%h', '%i', '%d', '%s', '%s']
        self.paw.patterns[1] = ['%h', '%i', '%i', '%s', '%u', '%d']
        self.paw.gen_hcat_cmd()
        self.assertEqual(len(self.paw.catstrs), 2)
        self.assertEqual(self.paw.catstrs,
                         {0: '-a 3 -1 ABCDEF -2 abcdef ?1?2?d?s?s',
                          1: '-a 3 -1 ABCDEF -2 abcdef ?1?2?2?s?u?d'})

    def test_gen_hcat_cmd_empty_pattern(self):
        self.paw.hcat = True
        self.paw.patterns[0] = ['']
        self.paw.gen_hcat_cmd()
        self.assertEqual(self.paw.wcount, 1)

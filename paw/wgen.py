def gen_wordlist(charset, positions=None, prev_iter=None):
    '''
    Recursively generates a wordlist based on given sets of characters.
    charset is a dictionary containing character sets for each
    string position of the generated words.
    '''
    if prev_iter is None:
        positions = [0 for i in charset]
        iter = 0
    else:
        iter = prev_iter + 1
    for idx, _ in enumerate(charset[iter]):
        positions[iter] = idx
        if iter == len(charset) - 1:
            yield ''.join([charset[idx][val]
                          for idx, val in enumerate(positions)])
        else:
            yield from gen_wordlist(charset, positions, iter)

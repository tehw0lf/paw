import functools
import operator


def save_to_file(charset, gen_wordlist, outfile=None, max_buf=256):
    try:
        buffer = []
        with open(outfile, "w", encoding="utf-8") as wl:
            print(
                "generating %d lines."
                % functools.reduce(
                    operator.mul, [len(i) for i in charset.values()], 1
                )
            )
            for word in gen_wordlist(charset):
                buffer.append(word)
                if len(buffer) == max_buf:
                    wl.write("\n".join(buffer) + "\n")
                    buffer = []
            wl.write("\n".join(buffer))

    except (OSError, TypeError):  # stdout
        for word in gen_wordlist(charset):
            print(word)

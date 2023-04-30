from lexicalrichness import LexicalRichness


def compute_linguistic_properties(text):
    lex = LexicalRichness(text)

    ret = {
        'vocd': 0,
        'msttr': 0,
        'mtld': 0,
        'chars': 0,
    }

    try:
        ret['vocd'] = lex.vocd(within_sample=100)
    except ValueError:
        pass
    try:
        ret['msttr'] = lex.msttr(segment_window=25)
    except ValueError:
        pass
    try:
        ret['mtld'] = lex.mtld()
    except ValueError:
        pass
    except ZeroDivisionError:
        pass
    ret['chars'] = len(text)

    return ret


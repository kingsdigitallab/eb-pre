from lexicalrichness import LexicalRichness
import re

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
    ret['words'] = count_tokens(text)

    return ret

def count_tokens(text):
    ret = 0
    # https://www.nltk.org/api/nltk.tokenize.html
    from nltk.tokenize import sent_tokenize, word_tokenize
    for sent in sent_tokenize(text):
        words = word_tokenize(sent)
        # we exclude punctuations
        ret += len([w for w in words if (len(w) > 1 or re.match(r'\w', w))])

    return ret


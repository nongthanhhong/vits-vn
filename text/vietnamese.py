import re
from viphoneme import vi2IPA
from viphoneme import syms

from vietnam_number import n2w
from vietnam_number import n2w_single

from underthesea import text_normalize

'''
- text_normalize 
- convert to IPA
- collapse_whitespace
'''
def collapse_whitespace(text):
    text = re.sub(r'\s+$', '', text)
    return re.sub(r'\s+', ' ', text)


def vi_to_ipa(text):
    text = text.lower()
    text = text_normalize(text)
    phonemes = vi2IPA(text)
    phonemes = collapse_whitespace(phonemes)
    return phonemes
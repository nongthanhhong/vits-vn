import re
from text.japanese import japanese_to_romaji_with_accent
from text.vietnamese import vi_to_ipa

# def japanese_cleaners(text):
#     text = f'[JA]{text}[JA]'
#     text = re.sub(r'\[JA\](.*?)\[JA\]', lambda x: japanese_to_romaji_with_accent(
#         x.group(1)).replace('ts', 'ʦ').replace('u', 'ɯ').replace('...', '…')+' ', text)
#     text = re.sub(r'\s+$', '', text)
#     text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
#     return text

def vietnamese_cleaners(text):
    text = vi_to_ipa(text).replace('...', '…')
    text = re.sub(r'([A-Za-z])$', r'\1.', text)
    text = re.sub(r'([^\.,!\?\-…~])$', r'\1.', text)
    return text
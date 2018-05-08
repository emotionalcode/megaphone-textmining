from konlpy.tag import Twitter
from megaphone_tokenizer import tokenswapper
import re

def tokenize_megaphone(megaphone_text):
    """ tokenize megaphone text.
    basically tokenize by nlp. and specially tokenize itemNames that betweend brackets.
    1. swap itemname to placeholder
    2. nlp from swapped text
    3. re-swap placeholders to itemname token
    """
    # swap itemname to placeholder
    placeHolderDic, swappedText = tokenswapper.swap_to_placeholder(megaphone_text)
    
    # nlp from swapped text
    twitter = Twitter()
    nlpTokens = twitter.pos(swappedText, norm=True, stem=True)
    
    # re-swap placeholders to itemname token
    return tokenswapper.recover_placeholders(nlpTokens, placeHolderDic)
from megaphone_tokenizer import tokenizer as tk

class TestTokenizer():

    def test_tokenize_megaphone(self):
        actual = tk.tokenize_megaphone('[ 11 화둔 : 염화멸섬] 2400팝니다~~~~~~~~~~~~~~~~~~~~~~~~~')
        assert actual == [('[ 11 화둔 : 염화멸섬]', 'ItemName'), ('2400', 'Number'), ('파다', 'Verb'), ('~~~~~~~~~~~~~~~~~~~~~~~~~', 'Punctuation')]
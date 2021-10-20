import re

TOKEN_RE = re.compile(r'[\w]+')


def tokenize_text_simple_regex(txt, min_token_size=4):
    #txt = txt.lower()
    all_tokens = TOKEN_RE.findall(txt)
    return [token for token in all_tokens if len(token) >= min_token_size]


def character_tokenize(txt, min_token_size=3):
    all_tokens = TOKEN_RE.findall(txt)
    return [char for token in all_tokens if len(token) >= min_token_size for char in token]


def tokenize_corpus(texts, tokenizer=tokenize_text_simple_regex, **tokenizer_kwargs):
    return [tokenizer(text, **tokenizer_kwargs) for text in texts]


def add_fake_token(word2id, token='<PAD>'):
    word2id_new = {token: i + 1 for token, i in word2id.items()}
    word2id_new[token] = 0
    return word2id_new


def texts_to_token_ids(tokenized_texts, word2id):
    return [[word2id[token] for token in text if token in word2id]
            for text in tokenized_texts]
PAD_TOKEN = '__PAD__'
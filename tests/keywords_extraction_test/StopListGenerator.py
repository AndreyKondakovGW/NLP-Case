def generate_stop_list(text_list,min_tf=50):
    tf_base = {}
    res =[]
    for text in text_list:
        for word in text.split():
            tf_base[word] = tf_base.get(word,0) + 1
    for word, tf in tf_base.items():
        if tf > min_tf:
            res.append(word)
    return res

import random
from random import shuffle

from wordfreq import top_n_list
from nltk.corpus import wordnet as wn

WORDLIST = [
    # Add your words here.
]
MUST_HAVE = [
    # Add your words here.
]
# Range of number of letters.
LEN_RANGE = (5, 10)


# match_word('set', 'service') -> [('s', 'service'), ('se', 'service')]
def match_word(target, word) -> list[(str, str)]:
    if target[0] != word[0]:
        return []
    result = []
    i = 0
    j = 0
    while i < len(target) and j < len(word):
        if target[i] == word[j]:
            result.append((target[:i + 1], word))
            i += 1
        j += 1
    return result


def backtrack(word, name: list[(str, str)], index, result):
    if index >= len(word):
        # for mh in MUST_HAVE:
        #     if mh not in [x[1] for x in name]:
        #         return
        if word not in result:
            result[word] = []
        result[word].append(name.copy())
        return
    used_words = set(n[1] for n in name)
    for candidate in WORDLIST:
        if candidate in used_words:
            continue
        for token in match_word(word[index:], candidate):
            name.append(token)
            backtrack(word, name, index + len(token[0]), result)
            del name[-1]


def main():
    all_nouns = []
    for synset in wn.all_synsets('n'):
        all_nouns.extend(synset.lemma_names())
    nouns = set(all_nouns)

    result = {}
    for word in (w for w in top_n_list('en', 30000) if w not in top_n_list('en', 20000)):
        if not LEN_RANGE[0] <= len(word) <= LEN_RANGE[1]:
            continue
        if word not in nouns:
            continue
        if len(word) > 3 and word[-3:] == 'ing':
            continue
        backtrack(word, [], 0, result)
    for k, v in sorted(result.items(), key=lambda kv: kv[0]):
        # print(f'Abbr: {k}, Names: {sorted(v, key=lambda x: len(x))[0]}')
        print(f'Abbr: {k}, Names: {random.sample(v, 5) if len(v) > 5 else v}')


if __name__ == '__main__':
    main()

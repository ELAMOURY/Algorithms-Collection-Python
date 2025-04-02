"""
Vigenère cipher is one of the simplest that employs a form of polyalphabetic substitution (each letter is assigned
more than one substitute).

It was first described in 1553 but took an entire three centuries to break it in 1863.

Weakness: If someone finds key length then this can be broken.

Programmed by Aladdin Persson <aladdin.persson at hotmail dot com>
*  2019-11-07 Initial programming

"""
import re
from collections import Counter

alphabet = "abcdefghijklmnopqrstuvwxyz "

letter_to_index = dict(zip(alphabet, range(len(alphabet))))
index_to_letter = dict(zip(range(len(alphabet)), alphabet))


def encrypt(message, key):
    encrypted = ""
    split_message = [
        message[i : i + len(key)] for i in range(0, len(message), len(key))
    ]

    for each_split in split_message:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] + letter_to_index[key[i]]) % len(alphabet)
            encrypted += index_to_letter[number]
            i += 1

    return encrypted


def decrypt(cipher, key):
    decrypted = ""
    split_encrypted = [
        cipher[i : i + len(key)] for i in range(0, len(cipher), len(key))
    ]

    for each_split in split_encrypted:
        i = 0
        for letter in each_split:
            number = (letter_to_index[letter] - letter_to_index[key[i]]) % len(alphabet)
            decrypted += index_to_letter[number]
            i += 1

    return decrypted

# Nettoyage et préparation du texte
def clean_text(text):
    return re.sub(r'[^a-z]', '', text.lower())

# Index de Coïncidence
def index_of_coincidence(text):
    N = len(text)
    freqs = Counter(text)
    return sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1)) if N > 1 else 0

# Estimation de la longueur de la clé
def estimate_key_length(text, max_len=20):
    ic_scores = []
    for key_len in range(1, max_len + 1):
        groups = [text[i::key_len] for i in range(key_len)]
        avg_ic = sum(index_of_coincidence(group) for group in groups) / key_len
        ic_scores.append((key_len, avg_ic))
    likely_lengths = sorted(ic_scores, key=lambda x: -x[1])
    return likely_lengths[0][0]

# Déduire la clé par fréquence
def deduce_key(text, key_len):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    letter_to_index = {ch: idx for idx, ch in enumerate(alphabet)}
    index_to_letter = {idx: ch for idx, ch in enumerate(alphabet)}
    key = ''

    for i in range(key_len):
        group = text[i::key_len]
        freq = Counter(group)
        most_common = freq.most_common(1)[0][0]
        shift = (letter_to_index[most_common] - letter_to_index['e']) % 26
        key += index_to_letter[shift]
    return key

def main():
    message = "gagoclcqgzhzkwnqadgvvqbxtmnqgugczdcgjmumweuqsgirrceqffpxtugipbtqrvwfhqimntgfguwvnujvgaqggccugzogglwzognivugwgugzhtqurxsxriugbvritazipmvmwkgkjmbkgmkxgkcxcusrvbqggfpvgzhiplcuhhwmeqggqcrewitmigzmgzuhcznmuqhgquoqzfkvvmwrutgepiwqvedvgvcusevcpqgspwtuhvtiwciiuipeiegkjarepanmwiowtfsxktuqasnikfeygtgehvpmddswhcuesevlwzbskzkzqfpvwqdekauudrttgedswauusigaxazepbgerlepcdpspinaiifqrmfhgaimnhwqrqgekmpfglttgemiwfnqgdgkjqghganmaggauaiwnmwdgtjirqoyzlgfcznmoqhentkcivpgoqhxcqgzhhwmfqgtqqpfgiqciqoxtmuabeglkehmpowmwktqgzzevikxzvuwwhfekboabkcqvmwruqsgiegtcduiepgywegmrxoxgmvapckywqcyniugwvfmfullkdgdgrwzcuheoiueslpmpgwxrzqrcefmfqgjqzoqgjrmeffenmuemriqvmwipbnqgcwmwdgtgzfgsjnikegekmpfsevzghcmtcpqffplggfhgpczqygcpnfeuvqgslzcpqhivmxuccgvvqpetjqgwcnmgocqomraiiwvedwqgxcdtfkagzgifmvmqycvvximuikqbkfmunzseafqvfwqnxshgarmbjgbfqgetmvqgstcuciiompfocncoqghwvtqtcgbfqqvkavmzgwqufcyvzgfcddikfoypwkdzvuzkhspcqpqgkcxcusrviidoefaeaituaqgfuuqnzmexikfdcwasgspgpcxskgugzhhgarawktqpqgpgotauegugzhhgogzsvvlgroxkowqgfwanmdiuipfsltlgxomtmv "
    key = deduce_key(message, 5)
    encrypted_message = encrypt(message, key)
    decrypted_message = decrypt(encrypted_message, key)

  
   print("key: " + key)

main()

#!/usr/bin/env python3
from string import ascii_letters
from string import printable
import collections
import math


def bin2txt(value):
    return value.decode('utf-8')


def bin2hex(value):
    return value.hex()


def txt2bin(value):
    return value.encode('utf-8')


def hex2bin(value):
    return bytearray.fromhex(value)


def hex2txt(value):
    return bytes.fromhex(value).decode('ascii')


def txt2hex(value):
    return txt2bin(value).hex()


def xor_key(text, key):
    text_bin = txt2bin(text)
    key_bin = txt2bin(key)
    encryption = b''
    for i in range(len(text_bin)):
        encryption += bytes([text_bin[i] ^ key_bin[i % len(key_bin)]])
    return bin2hex(encryption)


def decrypt_single_xor(cipher_text, key):
    ctext = hex2txt(cipher_text)
    return hex2txt(xor_key(ctext, key))


def crack_single_xor(cipher_text, alphabet):
    for c in alphabet:
        print(c)
        print(decrypt_single_xor(cipher_text,c))


def auto_crack_single_xor(cipher_text, alphabet):
    french_chars = {
            'E': 5,
            'A': 4,
            'S': 3,
            'T': 2,
            'I': 2,
            'W': -5,
            'K': -4,
            'Y': -3,
            'Z': -2,
            'X': -2
    }
    score_list = []
    for letter in alphabet:
        decrypt = decrypt_single_xor(cipher_text, letter)
        decrypt_letters_only = ''.join(c.upper() for c in decrypt if c.isalpha())

        if 4*len(decrypt_letters_only) <= len(decrypt):
            continue
        else:
            freqs = collections.Counter(decrypt_letters_only)
            score = 0
            most_common = [tup[0] for tup in freqs.most_common(10)]
            least_common = list(reversed(freqs.most_common(10)[-10:]))
            for k, v in french_chars.items():
                if k in most_common:
                    score += v
                elif k in least_common:
                    score -= v
            score_list.append((letter, score))
    score_list.sort(key=lambda tup: tup[1], reverse=True)
    key = score_list[0][0]
    decrypt = decrypt_single_xor(cipher_text, key)
    alpha_only = ''.join(c for c in decrypt if (c.isalpha()))
    alpha_only = alpha_only[:50]
    if sum(1 for c in alpha_only if c.isupper()) > 25:
        key = key.swapcase()
        decrypt = decrypt_single_xor(cipher_text, key)

    return key, decrypt


def crack_multi_xor(cipher_text, key_length):
    data_bin = hex2bin(cipher_text)
    data_list = []
    decrypt_list = []
    full_key = ''
    for i in range(key_length):
        data_list.append(data_bin[i::key_length])
        data_list_hex = bin2hex(data_list[i])
        key, plain_text = auto_crack_single_xor(data_list_hex, printable)
        full_key += key
        decrypt_list.append(plain_text)

    result = ''
    try:
        for i in range(len(decrypt_list[0])):
            for j in range(key_length):
                result += decrypt_list[j][i]
    finally:
        return full_key, result


def get_divisors(number):
    max_key_length = 20
    factors = []
    for i in range(2, max_key_length):
        if number % i == 0:
            factors.append(i)
    return factors


def kasiski_like_test(cipher_text):
    trigram_list = {}
    i = 0
    while i < len(cipher_text) - 5:
        trigram = cipher_text[i:i+6]
        if hex2txt(trigram) not in trigram_list.keys():
            trigram_list[hex2txt(trigram)] = []
        else:
            i += 2
            continue
        for j in range(i+2, len(cipher_text) - 5, 2):
            if trigram == cipher_text[j:j+6]:
                trigram_list[hex2txt(trigram)].append(j - i)
        i += 2

    groups_list = [v for v in trigram_list.values() if len(v) > 0]
    groups = list(set([item for group in groups_list for item in group]))
    divs = []
    divisors = {}
    for g in groups:
        divs.extend(get_divisors(g))
    for d in divs:
        if d not in divisors.keys():
            divisors[d] = 1
        else:
            divisors[d] += 1

    divisors = {k: v for k, v in sorted(divisors.items(), key=lambda item: item[1], reverse=True)}
    key_lengths = []
    best = max(divisors.values())
    for k, v in divisors.items():
        if v > (best/100)*90:
            key_lengths.append(k)
            best = v
        else:
            break
    for l in range(len(key_lengths) - 1):
        if key_lengths[l + 1] % key_lengths[l] == 0:
            continue
        else:
            return key_lengths[l]
    return key_lengths[-1]


if __name__ == '__main__':
    # Exercise 1
    print("=== Exercise 1 ===")
    print("Example decrypted: ", xor_key('everything remains raw', 'word up'))
    print("Exercise solution: ", xor_key('the world is yours', 'illmatic'))
    # solution = 1d04094d161b1b0f0d4c051e410d06161b1f

    # Exercise 2
    print("=== Exercise 2 ===")
    # the number 48 is present many times, also the first part 404b48484504 is there twice
    print(decrypt_single_xor('404b48484504404b48484504464d4848045d4b','$'))

    # Exercise 3
    print("=== Exercise 3 ===")
    with open("text1.hex", "r") as file:
        data = file.readline().replace('\n','')
        crack_single_xor(data, ascii_letters)
    # the correct single letter key is M, the first line of the plain text is:
    # Busta Rhymes up in the place

    # Exercise 4
    print("=== Exercise 4 ===")
    with open("text1.hex", "r") as file:
        data = file.read().replace('\n','')
        key, result = auto_crack_single_xor(data, ascii_letters)
        print("Key: ", key)
        print(result.split("\n")[0])

    # Exercise 5
    print("=== Exercise 5 ===")
    with open("text2.hex", "r") as file:
        data = file.read().replace('\n','')

        key, result = crack_multi_xor(data, 10)
        print("Key: ", key)
        print(result.split("\n")[0])

    # Exercise 6
    print("=== Exercise 6 ===")
    with open("text3.hex", "r") as file:
        data = file.read().replace('\n','')
        key_length = kasiski_like_test(data)
        key, result = crack_multi_xor(data, key_length)
        print("Key: ", key)
        print(result.split("\n")[0])


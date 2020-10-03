#!/usr/bin/env python3
from string import ascii_letters
from string import printable
import collections


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


# def kasiski_like_test(cipher_text):
#     data = hex2bin(cipher_text)
#     i = 0
#     while i < len(data):



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
        key, result = crack_multi_xor(data, 16)
        print("Key: ", key)
        print(result.split("\n")[0])
        # for i in range(3,20):
        #     result = crack_multi_xor(data, i)
        #     print(result)
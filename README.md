# Lab 1

Solution authors:

- Petr Stejskal (*stejspe7@fel.cvut.cz*)
- Martin Hula (*hulamart@fel.cvut.cz*)
- Petra Vaňková (*vankope6@fel.cvut.cz*)

Language: Python 3

The `main.py` script prints all the answers to stdout.


## Exercise 1: encrypt xor

Implemented in the ***xor_key()*** function. It's a simple for loop.

**Solution**:

The ciphertext of the `the world is ours` sentence against the key `illmatic` is `1d04094d161b1b0f0d4c051e410d06161b1f`.


## Exercise 2: decrypt single-letter xor

Implemented in the ***decrypt_single_xor()*** function.

**Solution**:

The byte `48`, also the pair`404b` is present multiple times, also after a more thorough look, the part `404b48484504` at the beginning is duplicated right after.

The decrypted plaintext of `404b48484504404b48484504464d4848045d4b` against the key `$` is `dolla dolla bill yo`.

## Exercise 3: hand crack single-letter xor

Implemented in ***crack_single_xor()*** function. Input is an encrypted file `text1.hex`.

Since we should have decrypted this exercise with our eyes only, it means brute-forcing over the whole alphabet (as it says "encoded with a single letter") and finding a readable output. Only the first 200 bytes were used, as it should already give us a clue whether the plaintext is correct or not. 

The script `main.py` prints out outputs of all possible keys (a-z, A-Z).

**Solution**:

The *key* used to encrypt the text is `M`, the first line of the *plaintext* is `Busta Rhymes up in the place, true indeed`.

## Exercise 4: automate cracking single-letter xor

Implmeneted in ***auto_crack_single_xor()*** function. The input is the same as in the previous exercise.

The point of this task was to automate the "see the correct output" process. A ranking function was created to choose the correct key among others. It works as follows:

* Since the function is supposed to be used in polyalphabetical exercises as well, it can't be a vocabulary technique
* Instead a frequency analysis was chosen 
  * The text is decoded with all letters (both upper- and lowercase), or in exercise 5 and 6 all printable characters
  * All characters but letters are stripped from the decrypted output, all letters are transformed to uppercase (because we know letter distributions in languages for case-insensitive texts only)
  * At first, English frequencies are used. Five most frequent letters are given a score (5,4,3,2,2) and five least frequent letters as well (-5,-4,-3,-2,-2).
  * Then a letter frequency distribution is done for each key and an overall score is counted:
    * When any of the most/least frequent English letters is among 10 most frequent letters of the output, the letter score (as above) is added to overall score of the key (which means subtracting for the least frequent). If the letter is among 10 least frequent letters, its score is subtracted. 
    * A key with the highest overall score wins.
  * The only problem is that our exercise is case-sensitive, so we need to decide on that too.
    * Since the winning key in both upper- and lowercase will have the same winning score, one is chosen randomly and the text is decrypted with that.
    * The first 50 letters (only letters) of the output are taken, if there are more than 50% upper-case letters, the other case of the key is chosen.
* English frequencies were later changed to French because of Exercise 5. Since it did not seem to make any difference, we kept the French.

**Solution**:

The same as in exercise 3.

## Exercise 5: crack multiple-letter xor with given key length
Implemented in the function ***crack_multi_xor()***. At the beginning we split the ciphertext by characters into groups determined by a position of the character in the ciphertext. A character at position `i` is assigned to group `i % key_length`. In this case the key is 10 characters long, so we distinguish 10 groups (0..9).

Characters assigned to the same group are encoded by the same key character (we use all printable characters here). In the next step we decrypt each group (text) by function ***auto_crack_single_xor()*** from exercise 4. For each group we get the correct key. The plaintext is then gained by concatenation of characters from decrypted texts to right positions. The full key is concatenated the same way.

**Solution**:

File `text2.hex` is encrypted by *key* `SupremeNTM`.
First line is `C'est le nouveau, phenomenal, freestyle du visage pale`.

## Exercise 6: crack multiple-letter xor with unknown key length
In this exercise we need to also find the length of the key. When we know it, we can use the function ***crack_multi_xor()*** from exercise 5 with the key length we found.

The length of the key is found by a method based on Kasisky test, implemented in ***kasiski_like_test()*** function. The algorithm is trying to deduce the length of the key by repeating sequences (trigrams here) in the ciphertext.

**Solution**:

File `text3.hex` is encrypted with *key* `CL4SS!C_TIM3L35S`.
First line is `And now for my next number I'd like to return to the...`.
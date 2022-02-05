import random
import string
letters = string.ascii_lowercase

with open('mystery_words.txt','r') as fi:
    with open('mystery_words_16.txt','w') as fo:
        while True:
            word = fi.readline()
            if not word:
                break
            fo.write(word.strip()+''.join(random.choice(letters) for i in
                                          range(11))+'\n')


with open('guessable_words.txt','r') as fi:
    with open('guessable_words_16.txt','w') as fo:
        while True:
            word = fi.readline()
            if not word:
                break
            fo.write(word.strip()+''.join(random.choice(letters) for i in
                                          range(11))+'\n')


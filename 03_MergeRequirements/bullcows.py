from random import randrange
import argparse
from urllib.request import urlopen

def bullscows(guess: str, secret: str) -> (int, int):
    s1 = set(guess)
    s2 = set(secret)
    counter = 0
    for i in range(min(len(guess), len(secret))):
        if guess[i] == secret[i]:
            counter += 1

    return counter, len(s1 & s2)


def ask(prompt: str, valid: list[str] = None) -> str:
    print(prompt)
    word = input()
    if valid:
        while word not in valid:
            print(prompt)
            word = input()
    return word


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows))


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    word = words[randrange(0, len(words))]
    n = 0
    while True:
        n += 1
        guess = ask("Введите слово: ", words)
        if guess == word:
            break
        b, c = bullscows(guess, word)
        inform("Быки: {}, Коровы: {}", b, c)
    return n


p = argparse.ArgumentParser()
p.add_argument('dict', type=str)
p.add_argument('length', type=int, default=5)

args = p.parse_args()
f = urlopen(args.dict)
words = f.read().decode().split()
words = [word for word in words if len(word) == args.length]

print(gameplay(ask, inform, words))



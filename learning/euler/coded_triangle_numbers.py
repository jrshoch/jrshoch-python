import requests
import util

triangle_numbers = [1]

def is_triangle_number(n):
    print "number:", n, ", triangle numbers:", triangle_numbers
    if n > triangle_numbers[-1]:
        extend_triangle_numbers(n)
    return n in triangle_numbers

def extend_triangle_numbers(n):
    while n > triangle_numbers[-1]:
        triangle_numbers.append(triangle_numbers[-1] + len(triangle_numbers) + 1)

def get_word_value(word):
    return sum([util.alphabet_position(letter) for letter in word])

def is_coded_triangle_number(word):
    print "word:", word
    return is_triangle_number(get_word_value(word))

def solve():
    words_text = requests.get('http://projecteuler.net/project/words.txt').text
    words = [word[1:-1] for word in words_text.split(',')]
    return util.count(is_coded_triangle_number, words)

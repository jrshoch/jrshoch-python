import itertools
import collections

def main():
  n = 345
  counter = collections.Counter()
  lowest_cubes = {}
  while True:
    n += 1
    permutations = set()
    cube = n ** 3
    digits = list(str(cube))
    digits.sort()
    hashable_digits = tuple(digits)
    if counter[hashable_digits] == 0:
      lowest_cubes[hashable_digits] = cube
    counter[hashable_digits] += 1
    if counter[hashable_digits] >= 5:
      return lowest_cubes[hashable_digits]

if __name__ == '__main__': print main()

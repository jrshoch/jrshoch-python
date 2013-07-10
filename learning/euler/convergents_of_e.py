def main():
  num = 0
  den = 1
  for i in xrange(99):
    if i % 3 == 1:
      add = (100 - i) / 3 * 2
    else:
      add = 1
    num, den = den, num + den * add
  return sum([int(x) for x in str(2 * den + num)])

if __name__ == '__main__': print main()

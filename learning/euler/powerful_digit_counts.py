import math

def main():
  count = 0
  for n in xrange(1, 10):
    i = 1
    while i * math.log10(n) >= i - 1:
      count += 1
      i += 1
  return count

if __name__ == '__main__': print main()

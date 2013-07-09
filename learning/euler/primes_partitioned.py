import marshal
import cPickle as pickle
import math
import bisect
import os

class PrimeSegmentMetadatum(object):

  STANDARD_SEGMENT_SIZE = 10 ** 6

  def __init__ (self, index, min, max, length):
    self.index = index
    self.min = min
    self.max = max
    self.length = length

  def get_index (self):
    return self.index

  def get_min (self):
    return self.min

  def get_max (self):
    return self.max

  def get_filename (self):
    return 'data/primes_' + str(self.min) + '-' + str(self.max) + '.marshal'

  def get_length (self):
    return self.length

  def __repr__ (self):
    return 'Primes ' + str(self.min) + ' - ' + str(self.max) + ', indices ' \
        + str(self.index) + ' - ' \
        + str(self.index + self.length - 1) \
        + ', @file "' + self.get_filename() + '"'

class Primes(object):

  METADATA_FILENAME = 'data/primes_partition_metadata.pickle'

  def __init__ (self, debug=True, test=False):
    self.debug = debug
    self.test = test
    self.initialize()

  def initialize (self):
    self.segment_metadata = pickle.load(open(self.get_metadata_filename()))
    self.max_loaded = 0
    self.next_segment_index = 0
    self.primes = []

  def get_metadata_filename(self):
    return ('test_' if self.test else '') + self.METADATA_FILENAME

  def get_segment_filename(self, metadatum):
    return ('test_' if self.test else '') + metadatum.get_filename()

  def extend_primes (self, n):
    while self.max_loaded < n \
        and self.next_segment_index < len(self.segment_metadata):
      self.load_next_segment()
    if self.max_loaded < n:
      self.generate_primes_less_than(self.get_batch_endpoint(n))

  def get_batch_endpoint (self, n):
    segment_size = PrimeSegmentMetadatum.STANDARD_SEGMENT_SIZE
    decimals = int(math.log10(n))
    divisor = 10 ** decimals
    if divisor < segment_size:
      return segment_size
    dividend = n / divisor
    if dividend == 9:
      return 20 * divisor
    else:
      return (dividend + 2) * divisor

  def load_next_segment (self):
    segment_metadatum = self.segment_metadata[self.next_segment_index]
    segments_file = open(self.get_segment_filename(segment_metadatum))
    self.primes.extend(marshal.load(segments_file))
    self.max_loaded = self.primes[-1]
    if self.debug: print 'loaded up to:', self.max_loaded
    self.next_segment_index += 1

  def generate_primes_less_than (self, n):
    if self.debug: print 'extending primes to:', n
    if n < 3: return
    start = self.primes[-1] + 1
    end = int(math.sqrt(n))
    sieve_size = n - start
    if sieve_size <= 0: return
    sieve = [True] * sieve_size
    for prime in self.primes:
      if prime > end: break
      elim = prime - (((start - 1) % prime) + 1)
      while elim < sieve_size:
        sieve[elim] = False
        elim += prime
    i = start
    while i <= end:
      if sieve[i - start]:
        elim = i ** 2 - start
        while elim < sieve_size:
          sieve[elim] = False
          elim += i
        self.primes.append(i)
        if self.debug: print i
      i += 1
    for j in xrange(i - start, sieve_size):
      if sieve[j]:
        self.primes.append(j + start)
        if self.debug: print j + start
    self.adjust_segments()

  def adjust_segments (self):
    segment_size = PrimeSegmentMetadatum.STANDARD_SEGMENT_SIZE
    if len(self.segment_metadata) == 0:
      raise RuntimeException('Segment metadata should not be empty')
    previous_segment_metadatum = self.segment_metadata.pop()
    start_index = previous_segment_metadatum.get_index()
    if len(self.segment_metadata) > 0:
      previous_max = self.segment_metadata[-1].get_max()
    else:
      previous_max = -1
    if self.debug:
      print 'erasing previous_segment_metadatum:', previous_segment_metadatum
    os.remove(self.get_segment_filename(previous_segment_metadatum))
    for index in xrange(start_index, len(self.primes), segment_size):
      segment = self.primes[index:index + segment_size]
      self.segment_metadata.append(PrimeSegmentMetadatum(
          index,
          previous_max + 1,
          segment[-1],
          len(segment)))
      if self.debug: print 'added segment: ', self.segment_metadata[-1]
      segment_filename = self.get_segment_filename(self.segment_metadata[-1])
      marshal.dump(segment, open(segment_filename, 'wb'))
      previous_max = segment[-1]
    pickle.dump(self.segment_metadata, open(self.get_metadata_filename(), 'wb'))
    self.max_loaded = self.primes[-1]
    self.next_segment_index = len(self.segment_metadata)

  def get_prime (self, index):
    if index >= len(self.primes):
      if self.next_segment_index < len(self.segment_metadata):
        self.load_next_segment()
      else:
        new_endpoint = self.get_batch_endpoint(self.primes[-1] + 1)
        self.generate_primes_less_than(new_endpoint)
    return self.primes[index]

  def get_index (self, n):
    self.extend_primes(n)
    return bisect.bisect_left(self.primes, n)

  def is_prime (self, n):
    self.extend_primes(n)
    return n == self.get_next_prime(n)

  def get_next_prime (self, n):
    self.extend_primes(n)
    return self.primes[self.get_index(n)]

  def get_prime_after (self, n):
    return self.get_next_prime(n + 1)

  def get_primes_less_than (self, n):
    self.extend_primes(n)
    return self.primes[:bisect.bisect_left(self.primes, n)]

  def get_primes_between (self, lower, upper):
    extend_primes(upper)
    return self.primes[bisect.bisect_right(self.primes, lower): \
                       bisect.bisect_left(self.primes, upper)]

  def get_current_primes (self):
    return self.primes

  def factor (self, n):
    extend_primes(int(math.sqrt(n)))
    factors = []
    for prime in self.primes:
      while n % prime == 0:
        n /= prime
        factors.append(prime)
      if n == 1:
        return factors

  def reset (self, test=True):
    oldtest = self.test
    self.test = test
    metadatum = PrimeSegmentMetadatum(0, 0, 3, 2)
    reset_segment_metadata = [metadatum]
    pickle.dump(reset_segment_metadata,
        open(self.get_metadata_filename(), 'wb'))
    reset_primes = [2, 3]
    marshal.dump(reset_primes, open(self.get_segment_filename(metadatum), 'wb'))
    self.test = oldtest
    self.initialize()

primes = Primes()


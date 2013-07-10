def mark_polygonal_with_n_digits(array, n_sides):
  formula = get_formula(n_sides)
  index = 0
  number = 0
  while number < 1000:
    index += 1
    number = formula(index)
  while number < 10000:
    mark_array(array, number, n_sides)
    index += 1
    number = formula(index)

def get_formula(n_sides):
  return lambda x: x * ((n_sides - 2) * x + 4 - n_sides) / 2

def mark_array(array, number, n_sides):
  index = number / 100
  while len(array) < index + 1:
    array.append(create_array_dict())
  array[index][n_sides].append(number)

def create_array_dict():
  return dict([(x, []) for x in xrange(3, 9)])

def main():
  array = []
  for n_sides in xrange(3, 9):
    mark_polygonal_with_n_digits(array, n_sides)
  special_sequence = search_for_sequence(array)
  print special_sequence
  return sum(special_sequence)

def search_for_sequence(array, sequence=[], \
    remaining_numbers_of_sides=set([3,4,5,6,7,8])):

  def recursive_search(dic):
    for key in dic:
      if key not in remaining_numbers_of_sides:
        continue
      new_remaining_numbers = remaining_numbers_of_sides.difference(set([key]))
      for value in dic[key]:
        result = search_for_sequence(array, \
                                     sequence + [value], \
                                     new_remaining_numbers)
        if result: return result
    return None

  if len(sequence) == 0:
    for dic in array:
      result = recursive_search(dic)
      if result: return result
  index = sequence[-1] % 100
  dic = array[index]
  if len(sequence) == 5:
    remaining_number_of_sides = next(iter(remaining_numbers_of_sides))
    for value in dic[remaining_number_of_sides]:
      if value % 100 == sequence[0] / 100:
        return sequence + [value]
    return None
  return recursive_search(dic)

if __name__ == '__main__': print main()

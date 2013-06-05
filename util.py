def count(filter_function, iterable):
    return reduce(lambda x, y: x + 1, filter(filter_function, iterable), 0)

def alphabet_position(letter):
    return ord(letter.lower()) - 96

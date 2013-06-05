def get_digit(n):
    if n <= 9:
        return n
    number_of_digits = 1
    number_of_numbers = get_number_of_numbers(number_of_digits)
    reduced_n = n
    number_of_numbers_so_far = 0
    while reduced_n > number_of_numbers * number_of_digits:
        reduced_n -= number_of_numbers * number_of_digits
        number_of_digits += 1
        number_of_numbers_so_far += number_of_numbers
        number_of_numbers = get_number_of_numbers(number_of_digits)
    reduced_n -= 1 # no zero, argh!
    number = reduced_n / number_of_digits + number_of_numbers_so_far + 1
    place = reduced_n % number_of_digits
    print reduced_n, number_of_digits, number_of_numbers_so_far, number, place
    return int(str(number)[place])

def get_number_of_numbers(number_of_digits):
    return 9 * (10 ** (number_of_digits - 1))

def solve():
    product = 1
    digit_index = 1
    counter = 1
    while counter <= 7:
        counter += 1
        product *= get_digit(digit_index)
        digit_index *= 10
    return product

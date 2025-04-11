# Random integers generation

import secrets
from symoblic_arithmetic import subtract_large_numbers

def string_random_below(n_str):
    """Generate a random number below n, where n is a string."""
    n = int(n_str)
    bits = n.bit_length()  # Approximate the number of bits in n
    while True:
        candidate = secrets.randbits(bits)  # Generate a random number with similar bit length
        if 0 < candidate < n:  # Ensure the candidate is within the valid range
            return str(candidate)

def choose_two_random_numbers_symbolic(p_str):
    """Choose two distinct random numbers from [1, p-1], using symbolic arithmetic."""
    if int(p_str) <= 1:
        raise ValueError("p must be greater than 1.")
    
    # Generate two random numbers below p-1
    num1 = string_random_below(subtract_large_numbers(p_str, '1'))  # p-1 as string
    num2 = string_random_below(subtract_large_numbers(p_str, '1'))

    # Ensure the numbers are distinct
    while num1 == num2:
        num2 = string_random_below(subtract_large_numbers(p_str, '1'))

    return num1, num2
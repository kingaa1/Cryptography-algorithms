# Helper functions

# Function to perform addition
def string_add(num1, num2):
    """
    Adds two large positive numbers given as strings and returns the result as a string.
    """
    # Make sure num1 is the longer number
    if len(num2) > len(num1):
        num1, num2 = num2, num1
    
    # Reverse both numbers to add from least significant digit
    num1 = num1[::-1]
    num2 = num2[::-1]

    result = []
    carry = 0

    # Add digit by digit
    for i in range(len(num1)):
        digit1 = int(num1[i])
        digit2 = int(num2[i]) if i < len(num2) else 0

        # Sum the digits and carry
        total = digit1 + digit2 + carry
        result_digit = total % 10
        carry = total // 10

        # Append result digit to the result list
        result.append(str(result_digit))

    # If there's a remaining carry, add it
    if carry:
        result.append(str(carry))

    # Reverse the result to get the final number and join as a string
    return ''.join(result[::-1])

# Function to perform multiplication
def string_multiply(num1, num2):
    """
    Multiplies two large decimal numbers represented as strings using Karatsuba algorithm
    and returns the result as a string.
    """
    # Handle negative numbers
    is_negative = (num1[0] == '-') ^ (num2[0] == '-')  # XOR to determine if the result is negative
    if num1[0] == '-':
        num1 = num1[1:]  # Remove negative sign from num1
    if num2[0] == '-':
        num2 = num2[1:]  # Remove negative sign from num2

    # Base case for recursion: if numbers are small, multiply directly
    if len(num1) == 1 or len(num2) == 1:
        result = str(int(num1) * int(num2))
        return '-' + result if is_negative else result

    # Make numbers the same length by padding with zeros
    max_len = max(len(num1), len(num2))
    num1 = num1.zfill(max_len)
    num2 = num2.zfill(max_len)

    # Find the middle point
    mid = max_len // 2

    # Split the numbers into high and low parts
    high1, low1 = num1[:-mid], num1[-mid:]
    high2, low2 = num2[:-mid], num2[-mid:]

    # Recursively calculate three products
    z0 = string_multiply(low1, low2)  # Low1 * Low2
    z1 = string_multiply(str(int(low1) + int(high1)), str(int(low2) + int(high2)))  # (Low1 + High1) * (Low2 + High2)
    z2 = string_multiply(high1, high2)  # High1 * High2

    # Combine the results using Karatsuba's formula
    result = int(z2) * 10**(2 * mid) + (int(z1) - int(z2) - int(z0)) * 10**mid + int(z0)

    # Return result with correct sign
    return '-' + str(result) if is_negative else str(result)

# Helper function for substraction: compare_abs
def compare_abs(num1, num2):
    """
    Compares the absolute values of two numbers given as strings.
    Returns:
        1 if |num1| > |num2|,
        -1 if |num1| < |num2|,
        0 if |num1| == |num2|.
    """
    if len(num1) > len(num2):
        return 1
    elif len(num1) < len(num2):
        return -1
    else:
        return (num1 > num2) - (num1 < num2)

# Function to perform substraction, only positive numbers
def subtract_positive_large_numbers(num1, num2):
    """
    Subtracts two large positive numbers given as strings (num1 - num2).
    Returns the result as a string.
    """
    # Make sure num1 is the larger number
    if compare_abs(num1, num2) == -1:
        num1, num2 = num2, num1
        sign = "-"
    else:
        sign = ""

    # Reverse both numbers to subtract from least significant digit
    num1 = num1[::-1]
    num2 = num2[::-1]

    result = []
    borrow = 0

    # Subtract digit by digit
    for i in range(len(num1)):
        digit1 = int(num1[i])
        digit2 = int(num2[i]) if i < len(num2) else 0

        # Perform the subtraction with borrowing
        diff = digit1 - digit2 - borrow
        if diff < 0:
            diff += 10
            borrow = 1
        else:
            borrow = 0

        # Append result digit to the result list
        result.append(str(diff))

    # Remove any leading zeros and add sign if needed
    return sign + ''.join(result[::-1]).lstrip("0") or "0"

# Main function used to substract numbers
def subtract_large_numbers(num1, num2):
    """
    Subtracts two large numbers with sign handling.
    Returns the result as a string.
    """
    if num1[0] == '-' and num2[0] == '-':
        # If both numbers are negative, it's equivalent to num2 - num1
        return subtract_positive_large_numbers(num2[1:], num1[1:])
    elif num1[0] == '-':
        # If only num1 is negative, it's equivalent to -(abs(num1) + abs(num2))
        return "-" + string_add(num1[1:], num2)
    elif num2[0] == '-':
        # If only num2 is negative, it's equivalent to abs(num1) + abs(num2)
        return string_add(num1, num2[1:])
    else:
        # If both numbers are positive, perform standard subtraction
        return subtract_positive_large_numbers(num1, num2)

# Function to perform division
def string_divide(dividend, divisor):
    """
    Performs integer division of two numbers represented as strings.
    Returns the quotient as a string.
    """
    if divisor == "0":
        raise ValueError("Division by zero is undefined.")

    quotient = []
    current = ""

    for digit in dividend:
        current += digit
        current = current.lstrip('0') or "0"
        q = 0
        while len(current) > len(divisor) or (len(current) == len(divisor) and current >= divisor):
            current = subtract_large_numbers(current, divisor)
            q += 1
        quotient.append(str(q))

    return ''.join(quotient).lstrip('0') or "0"

# Helper function to check if a number is negative
def is_negative(num_str):
    """Checks if a string-based number is negative."""
    return num_str.startswith('-')

# Function to perform modulus operation
def string_mod(dividend, divisor):
    """Perform modulus operation where both numbers are strings. Returns the remainder as a string."""
    remainder = ""  # Remainder as a string
    
    for digit in dividend:
        # Add the next digit to the remainder
        remainder += digit

        # Remove leading zeros from the remainder
        remainder = remainder.lstrip('0') or "0"

        # Perform subtraction if the remainder is greater than or equal to the divisor
        while compare_abs(remainder, divisor) >= 0:
            remainder = subtract_large_numbers(remainder, divisor)

    return remainder if remainder else "0"

# Function to find modular inverse
def string_mod_inverse(a, mod):
    """
    Finds modular inverse of a under modulo mod using Extended Euclidean algorithm.
    Operates entirely on strings for large numbers.
    """
    t, new_t = "0", "1"  # Coefficients for Bézout's identity
    r, new_r = mod, a  # Remainder terms

    while new_r != "0":
        # Compute quotient as string division
        quotient = string_divide(r, new_r)

        # Update t and new_t
        t, new_t = new_t, subtract_large_numbers(t, string_multiply(quotient, new_t))

        # Update r and new_r
        r, new_r = new_r, subtract_large_numbers(r, string_multiply(quotient, new_r))

    # Check if gcd(a, mod) is 1
    if r != "1":
        raise ValueError("a is not invertible under modulo mod")

    # Ensure t is positive
    if is_negative(t):
        t = t[1:]
        t = subtract_large_numbers(mod, t)

    return t

# Function to perform modular exponentiation
def string_modular_exponentiation(base, exp, mod):
    """Computes (base^exp) % mod where base, exp, and mod are strings."""
    result = "1"
    base = string_mod(base, mod)  # Reduce base modulo mod
    
    while exp != "0":
        if is_odd(exp):  # If the current exponent is odd
            result = string_mod(string_multiply(result, base), mod)
        base = string_mod(string_multiply(base, base), mod)  # Square the base
        exp = string_divide_by_2(exp)  # Halve the exponent
    
    return result

# Function to perform division by 2
def string_divide_by_2(a):
    """Performs integer division of a string number by 2."""
    result = ""
    carry = 0
    for digit in a:
        current = carry * 10 + int(digit)
        result += str(current // 2)
        carry = current % 2
    return result.lstrip('0') or "0"

# Helper function: Check if a string number is odd
def is_odd(a):
    """Checks if the string number a is odd."""
    return int(a[-1]) % 2 != 0

# Function to encode plaintext
def encode_plaintext(plaintext):
    """Encodes plaintext to a large number using symbolic arithmetic."""
    plaintext_num = "0"
    base = "256"

    for i, c in enumerate(plaintext):
        ascii_val = str(ord(c))  # Convert ASCII value to string
        power = string_modular_exponentiation(base, str(i), str(10**18))  # Calculate base^i
        term = string_multiply(ascii_val, power)  # Multiply ASCII value by base^i
        plaintext_num = string_add(plaintext_num, term)  # Add the term to the total

    return plaintext_num

# Function to decode plaintext
def decode_plaintext(plaintext_num):
    """Decodes a large number back into plaintext using symbolic arithmetic."""
    base = "256"
    plaintext = []

    while plaintext_num != "0":
        char_val = string_mod(plaintext_num, base)  # Get remainder mod 256
        plaintext.append(chr(int(char_val)))  # Convert to character
        plaintext_num = string_divide(plaintext_num, base)  # Divide by 256

    return ''.join(plaintext)

# Helper function: Modular inverse using Extended Euclidean Algorithm
def extended_euclid_string(a, b):
    """ Extended Euclidean Algorithm with string-based arithmetic to find modular inverse. """
    # Initial values for coefficients
    x0, x1 = "1", "0"  # Coefficients of a
    y0, y1 = "0", "1"  # Coefficients of b
    b_original = b

    while b != "0":
        # Calculate a // b and a % b as strings
        quotient = string_divide(a, b)
        remainder = string_mod(a, b)

        # Update a and b for the next iteration
        a, b = b, remainder

        # Update x and y based on the quotient
        x0, x1 = x1, subtract_large_numbers(x0, string_multiply(quotient, x1))
        y0, y1 = y1, subtract_large_numbers(y0, string_multiply(quotient, y1))

    # Final GCD is a; check if modular inverse exists
    if a != "1":
        raise ValueError("a is not invertible under modulo b (gcd(a, b) != 1)")

    # Ensure x0 is positive
    if is_negative(x0):
        # x0 = string_add(x0, b_original)  # b_original is the original modulus
        x0 = x0[1:]
        x0 = subtract_large_numbers(b_original, x0)

    return x0
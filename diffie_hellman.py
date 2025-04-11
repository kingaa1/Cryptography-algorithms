# Diffie-Hellman Key Exchange Protocol Implementation with Symbolic Arithmetic

from symoblic_arithmetic import string_modular_exponentiation
from random_integer_below import choose_two_random_numbers_symbolic

# Diffie-Hellman Key Exchange Protocol
def diffie_hellman_key_exchange_string(g, p, a, b):
    """
    Implements the Diffie-Hellman key exchange protocol with string-based arithmetic.
    
    Input:
    - g: Primitive root modulo p (as a string)
    - p: Large prime number (as a string)
    - a: Alice's ephemeral key (as a string)
    - b: Bob's ephemeral key (as a string)
    
    Output:
    - The shared private key g^(ab) % p as a string
    """
    # Step 1: Compute public keys
    A = string_modular_exponentiation(g, a, p)  # Alice's public key
    B = string_modular_exponentiation(g, b, p)  # Bob's public key

    # Step 2: Compute shared secret
    shared_secret_alice = string_modular_exponentiation(B, a, p)  # Alice computes this
    shared_secret_bob = string_modular_exponentiation(A, b, p)    # Bob computes this
    
    assert shared_secret_alice == shared_secret_bob, "The shared secrets do not match!"
    return shared_secret_alice

def main():
    # Parameters
    g = "5"  # Primitive root (as string)
    p = "15234745201463007706558111083071717085392259682287044574142794675291425649677126470685490446237419785664197470483041493246021879373950819965360084406516123"  # Prime modulus (as string)
    a, b = choose_two_random_numbers_symbolic(p) # Alice's and Bob's ephemeral keys (as string)

    # Perform the key exchange
    shared_key = diffie_hellman_key_exchange_string(g, p, a, b)
    print(f"Shared secret key: {shared_key}")

if __name__ == "__main__":
    main()
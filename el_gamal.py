# El Gamal Implementation using Diffie-Hellman shared key

from symoblic_arithmetic import string_modular_exponentiation, string_multiply, string_mod, string_mod_inverse, encode_plaintext, decode_plaintext
from random_integer_below import choose_two_random_numbers_symbolic
from diffie_hellman import diffie_hellman_key_exchange_string

# ElGamal Encryption using Diffie-Hellman shared key
def elgamal_encrypt_string_with_shared_key(plaintext, p, g, g_a, b, shared_secret):
    """Encrypts plaintext using symbolic arithmetic and Diffie-Hellman shared secret."""
    # Convert plaintext to a numeric representation
    plaintext_num = encode_plaintext(plaintext)

    # Reduce numerical value mod p
    plaintext_num = string_mod(plaintext_num, p)

    # Compute ciphertext (y1, y2)
    y1 = string_modular_exponentiation(g, b, p)  # g^b % p
    g_ab = string_modular_exponentiation(g_a, b, p)  # g^(ab) % p
    g_ab_shared = string_mod(string_multiply(g_ab, shared_secret), p)  # Apply shared secret to g^(ab)
    
    # y2 = (plaintext * g^(ab) * shared_secret) % p
    y2 = string_mod(string_multiply(plaintext_num, g_ab_shared), p)

    return y1, y2

# ElGamal Decryption using Diffie-Hellman shared key
def elgamal_decrypt_string_with_shared_key(ciphertext, p, a, shared_secret):
    """Decrypts ciphertext using symbolic arithmetic and Diffie-Hellman shared secret."""
    y1, y2 = ciphertext

    # Compute g^(ab) % p
    g_ab = string_modular_exponentiation(y1, a, p)
    g_ab_shared = string_mod(string_multiply(g_ab, shared_secret), p)  # Apply shared secret to g^(ab)

    # Compute modular inverse of g^(ab) * shared_secret
    g_ab_shared_inverse = string_mod_inverse(g_ab_shared, p)

    # Recover plaintext as a number
    plaintext_num = string_mod(string_multiply(y2, g_ab_shared_inverse), p)

    # Decode numerical value to plaintext
    plaintext = decode_plaintext(plaintext_num)
    return plaintext

# Full communication example using Diffie-Hellman and ElGamal
def main():
    # Parameters (all as strings)
    g = "5"  # Primitive root modulo p
    p = "15234745201463007706558111083071717085392259682287044574142794675291425649677126470685490446237419785664197470483041493246021879373950819965360084406516123"  # Prime modulus
    a, b = choose_two_random_numbers_symbolic(p)  # Alice's and Bob's random ephemeral keys - [1,p-1]

    # Perform the Diffie-Hellman key exchange to get the shared secret
    shared_key = diffie_hellman_key_exchange_string(g, p, a, b)
    print(f"Shared secret key: {shared_key}")

    # Compute g^a mod p (Alice's public key)
    g_a = string_modular_exponentiation(g, a, p)

    # Input plaintext
    plaintext = "HELLOOOO"

    # Alice encrypts the message using ElGamal and the shared secret from Diffie-Hellman
    ciphertext = elgamal_encrypt_string_with_shared_key(plaintext, p, g, g_a, b, shared_key)
    print(f"Ciphertext: {ciphertext}")

    # Bob decrypts the message using his private key and the shared secret
    decrypted_plaintext = elgamal_decrypt_string_with_shared_key(ciphertext, p, a, shared_key)
    print(f"Decrypted Plaintext: {decrypted_plaintext}")

if __name__ == "__main__":
    main()

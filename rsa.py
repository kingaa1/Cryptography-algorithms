# RSA Implementation using Diffie-Hellman shared key

from symoblic_arithmetic import string_multiply, string_mod, string_modular_exponentiation, encode_plaintext, decode_plaintext, extended_euclid_string, subtract_large_numbers, string_mod_inverse
from random_integer_below import choose_two_random_numbers_symbolic
from diffie_hellman import diffie_hellman_key_exchange_string

# Helper function to compute Euler's totient function, phi(n)
def compute_phi(p_str, q_str):
    """Computes phi(n) = (p-1)*(q-1) using symbolic arithmetic."""
    p_minus_1 = subtract_large_numbers(p_str, "1")
    q_minus_1 = subtract_large_numbers(q_str, "1")
    phi_n = string_multiply(p_minus_1, q_minus_1)
    return phi_n

def gcd_symbolic(a_str, b_str):
    """Symbolic implementation of GCD."""
    a, b = a_str, b_str
    while b != "0":
        a, b = b, string_mod(a, b)
    return a

def is_coprime(e_str, phi_str):
    """Check if e and phi(n) are coprime."""
    return gcd_symbolic(e_str, phi_str) == "1"

def generate_rsa_keys(p_str, q_str, e_str):
    """Generates RSA public and private keys."""
    # Compute n = p * q
    n_str = string_multiply(p_str, q_str)
    
    # Compute phi(n) = (p-1)(q-1)
    phi_n_str = compute_phi(p_str, q_str)
    
    # Validate e
    if not is_coprime(e_str, phi_n_str):
        raise ValueError("e must be coprime with phi(n).")
    
    # Compute d = e^-1 mod phi(n) using modular inverse
    d_str = extended_euclid_string(e_str, phi_n_str)
    
    # Return public and private keys
    return (n_str, e_str), (n_str, d_str)

def rsa_encrypt(plaintext, public_key, shared_key):
    """Encrypts the plaintext using the RSA public key and Diffie-Hellman shared secret."""
    n_str, e_str = public_key
    
    # Convert plaintext to a numeric representation (symbolically)
    plaintext_num = encode_plaintext(plaintext)
    
    # Modify the plaintext by incorporating the shared key
    modified_plaintext = string_mod(string_multiply(plaintext_num, shared_key), n_str)
    
    # Encrypt using cK(x) = x^e mod n
    ciphertext = string_modular_exponentiation(modified_plaintext, e_str, n_str)
    return ciphertext

def rsa_decrypt(ciphertext, private_key, shared_key):
    """Decrypts the ciphertext using the RSA private key and Diffie-Hellman shared secret."""
    n_str, d_str = private_key
    
    # Decrypt using dK(y) = y^d mod n
    decrypted_num = string_modular_exponentiation(ciphertext, d_str, n_str)
    
    # Modify the decrypted message by reversing the shared key multiplication
    original_plaintext_num = string_mod(string_multiply(decrypted_num, string_mod_inverse(shared_key, n_str)), n_str)
    
    # Decode the numeric plaintext back to string
    plaintext = decode_plaintext(original_plaintext_num)
    return plaintext

# Full communication example using Diffie-Hellman and RSA
def main():
    # Parameters (all as strings)
    g = "5"  # Primitive root modulo p
    p = "15234745201463007706558111083071717085392259682287044574142794675291425649677126470685490446237419785664197470483041493246021879373950819965360084406516123"  # Prime modulus
    a, b = choose_two_random_numbers_symbolic(p)  # Alice's and Bob's random ephemeral keys - [1,p-1]

    # Perform the Diffie-Hellman key exchange to get the shared secret
    shared_key = diffie_hellman_key_exchange_string(g, p, a, b)
    print(f"Shared secret key: {shared_key}")

    # Prime numbers for RSA (symbolically represented)
    rsa_p = "15234745201463007706558111083071717085392259682287044574142794675291425649677126470685490446237419785664197470483041493246021879373950819965360084406516123"
    rsa_q = "8386506700653187088114129336508517833941752817092037266701121132685842239715196576751226666314102366205376660890913822464516288805181874490066037489054359" 
    
    # Public exponent for RSA
    e = "17"
    
    # Generate RSA keys
    public_key, private_key = generate_rsa_keys(rsa_p, rsa_q, e)
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")
    
    # Input plaintext
    plaintext = "HELLOO"
    print(f"Plaintext: {plaintext}")
    
    # Alice encrypts the message using RSA and the shared secret from Diffie-Hellman
    ciphertext = rsa_encrypt(plaintext, public_key, shared_key)
    print(f"Ciphertext: {ciphertext}")
    
    # Bob decrypts the message using RSA, his private key, and the shared secret
    decrypted_plaintext = rsa_decrypt(ciphertext, private_key, shared_key)
    print(f"Decrypted Plaintext: {decrypted_plaintext}")

if __name__ == "__main__":
    main()

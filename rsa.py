from math import gcd
from random import randrange

# Step 1: Choose two distinct prime numbers, p and q
p = 61
q = 53

# Step 2: Compute n = p * q
n = p * q  # n is the modulus for both the public and private keys

# Step 3: Compute Euler’s Totient Function φ(n)
# Since p and q are prime:
#   φ(p) = p - 1
#   φ(q) = q - 1
# And since p and q are distinct primes:
#   φ(n) = φ(p * q) = φ(p) * φ(q) = (p - 1) * (q - 1)
phi_n = (p - 1) * (q - 1)

# φ(n) gives the number of integers < n that are coprime to n
# This is essential because Euler’s theorem guarantees:
#   if gcd(m, n) == 1, then m^φ(n) ≡ 1 mod n

# Step 4: Choose public exponent e such that 1 < e < φ(n), and gcd(e, φ(n)) = 1
# This ensures e has a modular inverse mod φ(n)
e = 17  # common choice, but must check gcd
assert math.gcd(e, phi_n) == 1

# Step 5: Compute private exponent d such that (d * e) % φ(n) = 1
# i.e., d is the modular inverse of e modulo φ(n)
def modinv(a, m):
    # Extended Euclidean Algorithm to find modular inverse
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    return x % m

def extended_gcd(a, b):
    # Recursive implementation of the Extended Euclidean Algorithm
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

d = modinv(e, phi_n)

# Step 6: Public key is (e, n), private key is (d, n)

# Step 7: Encryption: c = m^e mod n
# Step 8: Decryption: m = c^d mod n

# Let's test it
message = 42
ciphertext = pow(message, e, n)     # Encrypt
decrypted = pow(ciphertext, d, n)   # Decrypt

print("Original message:", message)
print("Encrypted ciphertext:", ciphertext)
print("Decrypted message:", decrypted)

# --- Summary of Totient Role ---
# The security of RSA rests on the fact that:
# - You can compute n = p * q easily
# - But it's hard to compute φ(n) without knowing p and q
# - And φ(n) is required to compute d = e⁻¹ mod φ(n)
# This is why φ(n) is central to the RSA algorithm.


"""
More Toolish Version
"""


# Step 1: Compute Euler's totient for n = p * q
def totient(p, q):
    return (p - 1) * (q - 1)

# Step 2: Choose a small public exponent e
def choose_e(phi_n):
    e = 3
    while gcd(e, phi_n) != 1:
        e += 2  # try next odd number
    return e

# Step 3: Compute modular inverse of e mod phi(n)
def modinv(e, phi_n):
    # Extended Euclidean Algorithm
    def extended_gcd(a, b):
        if b == 0:
            return (1, 0)
        else:
            q, r = divmod(a, b)
            s, t = extended_gcd(b, r)
            return (t, s - q * t)
    
    x, y = extended_gcd(e, phi_n)
    return x % phi_n

# Step 4: RSA Key Generation
def generate_keys(p, q):
    n = p * q
    phi_n = totient(p, q)         # Euler's totient function
    e = choose_e(phi_n)           # Public exponent
    d = modinv(e, phi_n)          # Private exponent
    return (e, d, n)

# Step 5: Encryption and Decryption using modular exponentiation
def encrypt(m, e, n):
    return pow(m, e, n)

def decrypt(c, d, n):
    return pow(c, d, n)

# Demo: use small primes for clarity
p, q = 61, 53
e, d, n = generate_keys(p, q)

message = 42
cipher = encrypt(message, e, n)
recovered = decrypt(cipher, d, n)

print(f"Original message: {message}")
print(f"Encrypted:        {cipher}")
print(f"Decrypted:        {recovered}")

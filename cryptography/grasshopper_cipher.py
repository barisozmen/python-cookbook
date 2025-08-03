# Taken from https://asecuritysite.com/symmetric/grasshopper
# First seen at Prof B Buchanan's twitter - https://x.com/billatnapier/status/1951972678757150851

import os
import binascii
import sys

############ Kuznyechik 'GrassHopper' Cipher Implementation 
############ Using Python 3.10.2 64-bit


class GrasshopperCipher:

    def __init__(self, key):
        # The value of pi
        self.pi = [252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 
                    233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 
                    249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79, 
                    5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31, 
                    235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204, 
                    181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135, 
                    21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177,
                    50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87, 
                    223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3, 
                    224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74, 
                    167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65, 
                    173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 
                    7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137, 
                    225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97,
                    32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 
                    89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182]
        # The inverse of pi
        self.pi_inv =  [165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158, 57, 85, 126, 82, 145, 
                        100, 3, 87, 90, 28, 96, 7, 24, 33, 114, 168, 209, 41, 198, 164, 63, 
                        224, 39, 141, 12, 130, 234, 174, 180, 154, 99, 73, 229, 66, 228, 21, 183, 
                        200, 6, 112, 157, 65, 117, 25, 201, 170, 252, 77, 191, 42, 115, 132, 213, 
                        195, 175, 43, 134, 167, 177, 178, 91, 70, 211, 159, 253, 212, 15, 156, 47, 
                        155, 67, 239, 217, 121, 182, 83, 127, 193, 240, 35, 231, 37, 94, 181, 30, 
                        162, 223, 166, 254, 172, 34, 249, 226, 74, 188, 53, 202, 238, 120, 5, 107, 
                        81, 225, 89, 163, 242, 113, 86, 17, 106, 137, 148, 101, 140, 187, 119, 60, 
                        123, 40, 171, 210, 49, 222, 196, 95, 204, 207, 118, 44, 184, 216, 46, 54, 
                        219, 105, 179, 20, 149, 190, 98, 161, 59, 22, 102, 233, 92, 108, 109, 173, 
                        55, 97, 75, 185, 227, 186, 241, 160, 133, 131, 218, 71, 197, 176, 51, 250,
                        150, 111, 110, 194, 246, 80, 255, 93, 169, 142, 23, 27, 151, 125, 236, 88, 
                        247, 31, 251, 124, 9, 13, 122, 103, 69, 135, 220, 232, 79, 29, 78, 4, 
                        235, 248, 243, 62, 61, 189, 138, 136, 221, 205, 11, 19, 152, 2, 147, 128, 
                        144, 208, 36, 52, 203, 237, 244, 206, 153, 16, 68, 64, 146, 58, 1, 38, 
                        18, 26, 72, 104, 245, 129, 139, 199, 214, 32, 10, 8, 0, 76, 215, 116]
        self.l_const = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]
        self.m = int("111000011", 2) # polynomial x^8+x^7+x^6+x+1
        self.k = int(key, 16)
        self.rkeys = self.keySchedule()

    # Function for XOR operation on 128-bit values
    def X(self,k,a):
        return k ^ a

    # Non-linear substitution function
    def S(self,a):
        b = 0
        for i in reversed(range(16)):
            b <<= 8
            b ^= self.pi[(a >> (8 * i)) & 0xff]
        return b

    # The inverse of the substitution function
    def S_inv(self,a):
        b = 0
        for i in reversed(range(16)):
            b <<= 8
            b ^= self.pi_inv[(a >> (8 * i)) & 0xff]
        return b

    # Binary multiplication function
    def binary_mul(self,a, b):
        if a == 0 or b == 0:
            return 0
        z = 0
        while a != 0:
            if a & 1 == 1:
                z ^= b
            b <<= 1
            a >>= 1
        return z

    # Function to get the number of bits in a number
    def nb_bits(self,a):
        return len(bin(a)) - 2 

    # Function to perform modulo operation with the polynomial x^8+x^7+x^6+x+1
    def mod_px(self,a):
        while(self.nb_bits(a) >= self.nb_bits(self.m)):
            d = self.nb_bits(a) - self.nb_bits(self.m)
            mshift = self.m << d
            a ^= mshift
        return a

    # Function for linear transformation
    def linear(self,a):
        l_const = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]
        leng = len(l_const)
        i=1 
        linear_transf = 0
        while a != 0:
            linear_transf ^= self.mod_px(self.binary_mul(a & 0xff,l_const[leng - i]))
            a >>= 8
            i+=1
        return linear_transf

    # Rotation function
    def R(self,a):
        return  (self.linear(a) << 120) ^ (a >> 8)

    # The inverse of the rotation function
    def R_inv(self,a):
        most_sign_bytes = (a >> 120) 
        b = a ^ (most_sign_bytes << 120)
        return (b << 8) ^ (self.linear((b << 8) ^ most_sign_bytes))

    # Recursive linear transformation
    def L_rec(self,i,a):
        return self.R(a) if i == 15 else self.R(self.L_rec(i+1,a))
    def L(self,a):
        return self.L_rec(0,a)

    # The inverse of the recursive linear transformation
    def L_inv_rec(self,i,a):
        return self.R_inv(a) if i == 15 else self.R_inv(self.L_inv_rec(i+1,a))
    def L_inv(self,a):
        return self.L_inv_rec(0,a)

    # Transformation function
    def F(self,k,a1,a0):
        return self.L(self.S(self.X(k,a1))) ^ a0, a1

    def keySchedule(self):
        """Key scheduling function"""
        round_keys = [] 
        k1 = self.k >> 128
        k2 = self.k ^ (k1 << 128)
        round_keys.append(k1)
        round_keys.append(k2)
        for i in range(4):
            for j in range(8):
                k1,k2 = self.F(self.L(8 * i + j + 1),k1,k2)
            round_keys.append(k1)
            round_keys.append(k2)
        return round_keys

    def encrypt(self, plaintext):
        """Encryption function"""
        plaintext = int(plaintext, base=16)
        for r in range(9):
            plaintext = self.L(self.S(self.X(self.rkeys[r], plaintext)))
        return self.X(self.rkeys[9], plaintext)

    def decrypt(self, ciphertext):
        """Decryption function"""
        for r in range(9,0 ,-1):
            ciphertext = self.S_inv(self.L_inv(self.X(self.rkeys[r], ciphertext)))
        return self.X(self.rkeys[0], ciphertext)


msg="Hello"


if (len(sys.argv)>1):
	msg=str(sys.argv[1])
plaintext = binascii.hexlify(msg.encode())


key = os.urandom(16).hex()


cipher = GrasshopperCipher(key)


ciphertext = cipher.encrypt(plaintext)

plaintxt_decrypt = cipher.decrypt(ciphertext)

dec=bytes.fromhex(hex(plaintxt_decrypt)[2:]).decode('utf-8')

print("Message: " + msg)
print("Key: " + key)

print("Ciphertext = " + str(hex(ciphertext)))

print("Plaintext = " + dec)


# ================================================
# A SAMPLE RUN
# ================================================
# Message: Hello
# Key: 1ddcf49d9606415cebab4b7ce94946df
# Ciphertext = 0x868fad8d59920496d82407be75435c9
# Plaintext: Hello

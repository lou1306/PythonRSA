"""
Luca Di Stefano --- 235068
Ing. Informatica e Automatica
"""

from MathLib import MathLib as ml, ContinuedFraction
from random import SystemRandom
from math import ceil
from fractions import gcd
import sys

class RSAMessage:
    """
    Provides methods for encryption/decryption of a message.
    """
    def __init__(self, string):
        if not(type(string) == str):
            raise Exception("Argument must be a string.")
        self.plaintext = string
        
    def __int__(self):
        """
        Implements conversion to int. This means that
        >>> int(msg)
        will return an integer which represents the (utf-8 encoded) string. 
        """
        return int.from_bytes(self.plaintext.encode(), sys.byteorder)
    
    def __repr__(self):
        return self.plaintext
    
    @classmethod
    def fromInt(cls, n):
        """
        Computes the uft-8 string represented by the integer n and
        returns it in a RSAMessage object.
        """
        s = n.to_bytes(ceil(n.bit_length()/8), sys.byteorder).decode()
        return RSAMessage(s)
    
    def encrypt(self, key):
        """
        Encrypts the plaintext using the provided key. 
        """
        m = int(self)
        if m.bit_length() > key.n.bit_length():
            raise Exception("m is too long.")
        return pow(m, key.e, key.n)
    
    @classmethod
    def decrypt(cls, c, key):
        """
        Decrypts the ciphertext represented by the integer c.
        The result is returned in a RSAMessage object.
        """
        if key.d == None:
            raise Exception("Private exponent not found.")
        m = pow(c, key.d, key.n)
        return cls.fromInt(m)
    
class RSAKey:
    """
    Contains methods for generating and handling RSA keys.
    """
    @classmethod
    def generate(cls, bits, e = 0):
        """
        Returns a key of requested length.
        The public exponent e can be set by the user
        (commonly used values: 3 and 65537)
        """
        # iterate until all conditions are satisfied
        while True:
            p = ml.prime(bits >> 1)
            q = ml.prime(bits >> 1)
            n = p * q
            # p-q should not be "small"
            if abs(p-q) > 10**10:
                phi = (p-1) * (q-1)
                while (gcd(phi, e) != 1):
                    # e < phi and is at most 3 bytes long
                    e = SystemRandom().randrange(2, min(phi, 1<<24))
                d = ml.inverseMod(e, phi)
                # d must be long enough to prevent attacks
                if d.bit_length() > n.bit_length()/4:
                    return RSAKey(n, e, d, p, q)
    
    @classmethod
    def weakGenerate(cls, bits):
        """
        Generates a key that is vulnerable to Wiener's attacks.
        """
        while True:
            p = ml.prime(bits >> 1)
            q = ml.prime(bits >> 1)
            n = p * q
            phi = (p-1) * (q-1)
            d = 0
            maxd = pow(n, 1/4) // 3
            while (gcd(phi, d) != 1):
                d = SystemRandom().randrange(2, maxd)
            e = ml.inverseMod(d, phi)
            # d must be long enough to prevent attacks
            #if d.bit_length() > n.bit_length()/4:
            return RSAKey(n, e, d, p, q)
    
    @classmethod
    def WienersAttack(cls, e, n):
        """
        Tries to recover d from (e,n).
        """
        cf = ContinuedFraction(e, n)
        for conv in cf.convergents():
            print(conv)
            k = conv.numerator
            d = conv.denominator
            if k != 0 and d % 2 != 0:
                if (e*d - 1) % k == 0:  # phi is an integer
                    phi = (e*d - 1) // k
                    b = n - phi + 1     # b is even (n+1 even - phi even)
                    if ml.isSquare(b**2 - 4*n):
                        deltaRoot = ml.intSqrt(b**2 - 4*n)
                        if deltaRoot % 2 == 0:  # deltaRoot is even
                            p = (b + deltaRoot) // 2
                            q = (b - deltaRoot) // 2
                            d = ml.inverseMod(e, phi)
                            return RSAKey(n, e, d, p, q)
        # The attack has failed
        return False
    
    def publicKey(self):
        return RSAKey(self.n, self.e, None, None, None)
    
    def __eq__(self, other):
        return type(other) == RSAKey and self.__dict__ == other.__dict__
    def __ne__(self, other):
        return type(other) != RSAKey or self.__dict__ != other.__dict__
    
    def __init__(self, n, e, d, p, q):
        self.n = n
        self.e = e
        self.d = d
        self.p = p
        self.q = q
    def __repr__(self):
        return "n = " + str(self.n) + "\n" + \
        "e = " + str(self.e) + "\n" + \
        "d = " + str(self.d)

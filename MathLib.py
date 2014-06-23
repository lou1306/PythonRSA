"""
Luca Di Stefano --- 235068
Ing. Informatica e Automatica
"""

from random import SystemRandom, Random
from fractions import gcd, Fraction

class MathLib:
    """
    Number of steps for the Fermat primality test.

    After p passes the Fermat test:
    P(p is prime or Carmichael) >= 1 - 2^(-F_steps)
    """
    F_steps = 100
    """
    Number of steps for the Miller_Rabin primality test.
    After p passes the Miller-Rabin test, there's still a chance that
    p is composite:
    P(p is composite) <= 4^(-MR_steps) 
    """
    MR_steps = 30 # P(p is composite) <= 4^(-30) = 8.67e-19 
    
    @classmethod
    def intSqrt(cls, n):
        """
        Computes the integer square root of n, i.e.
        the greatest x : x*x <= n
        """
        x = n
        y = (x + n // x) // 2
        while y < x:
            x = y
            y = (x + n // x) // 2
        return x
    
    @classmethod
    def isSquare(cls, n):
        """
        Checks if n is a perfect square
        """
        return cls.intSqrt(n)**2 == n 
    """
    (Probable) Prime number generator.
    1. Start from a random odd integer p of desired bit-length.
    2. Run a Fermat primality test.
    3. If it succeeds, run a Miller-Rabin primality test.
    4a. If both test succeed, p is probably a prime number.
    4b. If Miller-Rabin fails, go back to step 1.
        
    The probability that p is actually prime depends on the number of
    iterations of the Miller-Rabin test.
    """
    @classmethod
    def prime(cls, bits):
        # Odd 512-bit number. SystemRandom() is cryptographically secure.
        p = SystemRandom().randrange((2**(bits-1))+1, (2**bits)-1, 2)
        while True:
            # MillerRabin(p) is only executed if Fermat(p) == true 
            if cls.Fermat(p) and cls.MillerRabin(p):
                    return p
            else:
                p = SystemRandom().randrange((2**(bits-1))+1, (2**bits)-1, 2)


    @classmethod
    def Fermat(cls, n):
        """
        Fermat primality test.
        
        n is composite <=> There is an integer a in [1,n-1] such that
        a^(n-1) != 1 mod n.
        
        If Fermat(n) = False, n is certainly composite.
        If Fermat(n) = True, n is either a prime or a Carmichael number.
        """            
        if n > 2 and n & 1 == 0:
            return False
        for _ in range(0, cls.F_steps):
            a = Random().randrange(1, n)
            if pow(a, n-1, n) != 1:
                return False
        return True
    
    @classmethod
    def MillerRabin(cls, n):
        """
        Miller-Rabin primality test.
        Returns:
        False if n is composite;
        True if n is prime with probability 1-4^(-MR_steps).
        """    
        if n > 2 and n & 1 == 0:
            return False
        """
        n-1 = 2^s * r; r is odd
        """
        s = cls.factor2(n-1)
        r = (n-1) >> s
        for _ in range(0,cls.MR_steps):
            a = Random().randrange(2, n)
            y = pow(a, r, n)
            if y != 1 and y != n-1:
                j = 1
                while j <= s-1 and y != n-1:
                    y = pow(y, 2, n)
                    if y == 1:
                        return False
                    j += 1
                if y != n-1:
                    return False
        return True
    
    @classmethod
    def JS(cls,a,b):
        """
        Jacobi symbol (a/b)
        Time efficiency: O((log a)(log b))
        """
        if b % 2 == 0:
            raise Exception
        if b == 1:
            return 1
        a = a % b
        if a == 0:
            return 0
        """
                           a         c        2^s 
        a = c*(2^s) ==> ( --- ) = ( --- ) * ( --- )
                           b         b         b
                                     
          2^s       +1  if  s is even  OR             
        ( --- ) =       if  b = (1 or 7) mod 8;
           b        -1  otherwise.
           
        (b mod 8 can't be an even number, since b must be odd.)  
        Also,
        
            c        - ( b/c )  if  b = c = 3 mod 4;     
         ( --- ) =   
            b        + ( b/c )  otherwise.   
        """
        s = MathLib.factor2(a)
        c = a // (2**s)
        bmod8 = b % 8
        
        if s % 2 == 0 or bmod8 == 1 or bmod8 == 7:
            sign1 = 1
        else:
            sign1 = -1
        
        if b % 4 == 3 and c % 4 == 3:
            sign2 = -1
        else:
            sign2 = 1
            
        return cls.JS(b,c)*sign1*sign2
    
    @classmethod
    def factor2(cls,n):
        """
        Returns an integer s such that
        n = m * 2^s.
        O(log(n))
        """
        i = 0
        while n & 1 == 0 and n > 0:
            i += 1
            n >>= 1
        return i
      
    @classmethod
    def powerMod(cls, base, exp, m):
        """
        Computes base^exp mod m.
        Source:
            Handbook of Applied Cryptography
            by A. Menezes, P. van Oorschot and S. Vanstone
            Algorithm 2.143
        Time efficiency: O(log(exp))
        """
        result = 1
        while exp > 0:
            if exp % 2 == 1:
                result = result * base % m
            exp >>= 1
            base = base**2 % m
        return result

    @classmethod
    def inverseMod(cls, a, b):
        """
        Computes the integer x such that
        a*x = 1 mod b.
        """
        if gcd(a,b) != 1:
            return 0
        x2 = 1
        x1 = 0
        mod = b
        while b > 0:
            r = a % b
            x = x2 - (a//b) * x1
            a = b
            b = r
            x2 = x1
            x1 = x
        return x2 % mod
          
    @classmethod
    def gcd(cls, a, b):
        """
        Computes the Greatest Common Divisor of a and b (Euclid's algorithm).
        """   
        if a == b or b == 0 or a == 0:
            return a
        if a < b:
            t = a
            a = b
            b = t 
        while b > 0:
            r = a % b
            if r == 0:
                return b
            a = b
            b = r

class ContinuedFraction(Fraction): 
    def __init__(self, num, den):
        super(Fraction, self).__init__()
    
    def expand(self):
        fractPart = Fraction(1,1)
        x = Fraction(self)
        while fractPart.numerator != 0:
            intPart = int(x)
            fractPart = x - intPart
            if fractPart != 0:
                x = 1/fractPart
            yield intPart
    @classmethod
    def nextConvergent(self, n, h1, h2, k1, k2):
        if type(n) != int:
            raise Exception("n must be an integer.")
        return Fraction(n*h1 + h2, n*k1 + k2)
    
    def convergents(self):
        """
        Generates a list of convergents.
        """
        h1 = 1
        h2 = 0
        k1 = 0
        k2 = 1
        for i in self.expand():
            f = self.nextConvergent(i, h1, h2, k1, k2)
            h2 = h1
            h1 = f.numerator
            k2 = k1
            k1 = f.denominator
            yield f
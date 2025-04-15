class Tools:
    pi = 3.1415926535

    @staticmethod
    def fact(n):
        if n == 0:
            return 1
        else:
            return n * Tools.fact(n - 1)

    @staticmethod
    def cos(x):
        s = 0
        for i in range(10):
            s += (-1)**i * x**(2*i) / Tools.fact(2*i)
        return s

    @staticmethod
    def sin(x):
        s = 0
        for i in range(10):
            s += (-1)**i * x**(2*i + 1) / Tools.fact(2*i + 1)
        return s

    @staticmethod
    def sqrt(x):
        if x < 0:
            raise ValueError("La racine carrée d'un nombre négatif n'est pas définie.")
        guess = x / 2
        for _ in range(10):
            guess = (guess + x / guess) / 2
        return guess

    @staticmethod
    def abs(x):
        return x if x >= 0 else -x

    @staticmethod
    def deg2rad(deg):
        return deg * Tools.pi / 180

    @staticmethod
    def rad2deg(rad):
        return rad * 180 / Tools.pi

pi = Tools.pi
sin = Tools.sin
cos = Tools.cos
fact = Tools.fact
sqrt = Tools.sqrt
abs = Tools.abs
deg2rad = Tools.deg2rad
rad2deg = Tools.rad2deg

__all__ = ["pi", "sin", "cos", "fact", "sqrt", "abs", "deg2rad", "rad2deg"]
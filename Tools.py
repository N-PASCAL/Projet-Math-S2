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

pi = Tools.pi
sin = Tools.sin
cos = Tools.cos
fact = Tools.fact

__all__ = ["pi", "sin", "cos", "fact"]
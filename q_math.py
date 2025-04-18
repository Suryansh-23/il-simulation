def add(a: int, b: int) -> int:
    """
    Add two square roots of prices.
    """
    return a + b

def sub(a: int, b: int) -> int: 
    """
    Subtract two square roots of prices.
    """
    return a - b

def mul(a: int, b: int) -> int:
    """
    Multiply two square roots of prices.
    """
    return (a * b) >> 96

def div(a: int, b: int) -> int:
    """
    Divide two square roots of prices.
    """
    temp = a << 96
    
    if (temp >= 0 and b >= 0) or (temp < 0 and b < 0):
        temp += (b >> 1)
    else:
        temp -= (b >> 1)
    
    return temp // b

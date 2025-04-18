
from decimal import Decimal
from uv4 import TickMath

from q_math import *

SCALING_FACTOR = Decimal(2) ** 96
ONE = 79228162514264337593543950336

def to_pi_r(pi_0, pi_l, pi_u):
    if pi_0 <= pi_l:
        return pi_l
    elif pi_0 >= pi_u:
        return pi_u
    else:
        return pi_0
    
def q64_96_to_decimal(q_value: int) -> Decimal:
    """
    Convert a Q64.96 fixed-point number to a Decimal.
    
    Parameters:
        q_value (int): The Q64.96 number represented as an integer.
        
    Returns:
        Decimal: The corresponding decimal value.
    """
    return Decimal(q_value) / SCALING_FACTOR

def decimal_to_q64_96(d: Decimal) -> int:
    """
    Convert a Decimal or float to a Q64.96 fixed-point number.
    
    Parameters:
        decimal_value (Decimal or float): The decimal number to convert.
        
    Returns:
        int: The corresponding Q64.96 number as an integer.
    """
    # Multiply by the scaling factor and round to the nearest integer.
    return int(d * SCALING_FACTOR)

def qdel_x_from_del_l(del_l: float, tick_0: TickMath, tick_l: TickMath, tick_u: TickMath) -> int:
    del_l_q = decimal_to_q64_96(Decimal(del_l))
    
    l_q = tick_l.to_sqrt_price_x96()
    u_q = tick_u.to_sqrt_price_x96()
    p_0_q = tick_0.to_sqrt_price_x96()
    p_0_r_q = to_pi_r(p_0_q, l_q, u_q)
    
    inv_0 = div(ONE, p_0_r_q)
    inv_u  = div(ONE, u_q)
    
    return mul(del_l_q, sub(inv_0, inv_u))

def del_x_from_del_l(del_l: float, tick_0: TickMath, tick_l: TickMath, tick_u: TickMath) -> Decimal:
    return q64_96_to_decimal(qdel_x_from_del_l(del_l, tick_0, tick_l, tick_u))

def qdel_y_from_del_l(del_l: float, tick_0: TickMath, tick_l: TickMath, tick_u: TickMath) -> Decimal:
    pass

def qdel_L_from_real_x(real_x: float, tick_0: TickMath, tick_l: TickMath, tick_u: TickMath) -> Decimal:
    del_x = Decimal(real_x)
    del_x_q = decimal_to_q64_96(del_x)
    
    l_q = tick_l.to_sqrt_price_x96()
    u_q = tick_u.to_sqrt_price_x96()
    p_0_q = tick_0.to_sqrt_price_x96()
    p_0_r_q = to_pi_r(p_0_q, l_q, u_q)
    
    inv_0 = div(ONE, p_0_r_q)
    inv_u  = div(ONE, u_q)
    
    return div(del_x_q, sub(inv_0, inv_u))
    
def del_L_from_real_x(real_x: float, tick_0: TickMath, tick_l: TickMath, tick_u: TickMath) -> Decimal:
    return q64_96_to_decimal(qdel_L_from_real_x(real_x, tick_0, tick_l, tick_u))

def qil(qdel_l: int, tick_0: TickMath, tick_1: TickMath, tick_l: TickMath, tick_r: TickMath) -> int:
    p_0_q = tick_0.to_sqrt_price_x96()
    p_1_q = tick_1.to_sqrt_price_x96()
    
    p_0_r_q = to_pi_r(p_0_q, tick_l.to_sqrt_price_x96(), tick_r.to_sqrt_price_x96())
    p_1_r_q = to_pi_r(p_1_q, tick_l.to_sqrt_price_x96(), tick_r.to_sqrt_price_x96())
    
    lb = sub(p_0_r_q, p_1_r_q)
    rb_tmp = div(mul(p_1_q, p_1_q), mul(p_0_r_q, p_1_r_q))
    rb = sub(ONE, rb_tmp)
    
    return mul(qdel_l, mul(lb, rb))

def il(qdel_l: int, tick_0: TickMath, tick_1: TickMath, tick_l: TickMath, tick_r: TickMath) -> Decimal:
    return -q64_96_to_decimal(qil(qdel_l, tick_0, tick_1, tick_l, tick_r))

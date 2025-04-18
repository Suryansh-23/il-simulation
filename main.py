from decimal import Decimal
from uv4 import TickMath
import matplotlib.pyplot as plt

from calc import  decimal_to_q64_96, il, qdel_L_from_real_x, q64_96_to_decimal, del_x_from_del_l
from q_math import *

TICK_SPACING = 60

real_x, real_y = 4.09186, 12352.33291
price_0 = 3019
tick_0 = TickMath(TickMath(tick_spacing=TICK_SPACING).from_price(Decimal(price_0)))
tick_l, tick_u = TickMath(80100, TICK_SPACING), TickMath(80160, TICK_SPACING)   # [3009.71...,3027.82...)

print(f"Price Range: [{tick_l.to_price()}, {tick_u.to_price()}]")
print(f"Square Root Price Range: [{tick_l.to_sqrt_price_x96()}, {tick_u.to_sqrt_price_x96()}]")
print(f"Current Price: {price_0} | Square Root Price: {tick_0.to_sqrt_price_x96()}")

# print(f"Delta Liquidity: {del_L_from_real_x(real_x, tick_0, tick_l, tick_u)}")

price_1 = 3000
tick_1 = TickMath(TickMath(tick_spacing=TICK_SPACING).from_price(Decimal(price_1)))
qdel_l = qdel_L_from_real_x(real_x, tick_0, tick_l, tick_u)

print(f"Delta Liquidity: {q64_96_to_decimal(qdel_l)}")

loss = il(qdel_l, tick_0, tick_1, tick_l, tick_u)
print(f"Impermanent Loss: {loss}")

# print(f"IL for X: {del_x_from_del_l(loss, tick_0, tick_l, tick_u)}")        

def get_il(price_1, price_0, price_l, price_u):
    tick_0 = TickMath(TickMath(tick_spacing=TICK_SPACING).from_price(Decimal(price_0)))
    tick_1 = TickMath(TickMath(tick_spacing=TICK_SPACING).from_price(Decimal(price_1)))
    tick_l = TickMath(TickMath(tick_spacing=TICK_SPACING).from_price(Decimal(price_l)))
    tick_u = TickMath(TickMath(tick_spacing=TICK_SPACING).from_price(Decimal(price_u)))

    # qdel_l = qdel_L_from_real_x(real_x, tick_0, tick_l, tick_u)
    one = decimal_to_q64_96(1)
    return il(one, tick_0, tick_1, tick_l, tick_u)

def plot(price_0, price_l, price_u):
    # Generate price_1 values in a range around price_0
    range_width = price_0 * 0.05  # Set range to ±25% of price_0
    start_price = int(price_0 - range_width)
    end_price = int(price_0 + range_width)
    step = int((end_price - start_price) / 40)  # Create 40 data points
    
    price_1_values = range(start_price, end_price, max(step, 1))
    il_values = [get_il(p, price_0, price_l, price_u) for p in price_1_values]

    plt.figure(figsize=(10, 6))
    plt.plot(price_1_values, il_values)
    
    # Add vertical lines for reference prices
    plt.axvline(x=price_0, color='r', linestyle=':', label='Price 0')
    plt.axvline(x=price_l, color='g', linestyle=':', label='Lower Bound')
    plt.axvline(x=price_u, color='b', linestyle=':', label='Upper Bound')
    
    plt.xlabel('Price 1')
    plt.ylabel('Impermanent Loss')
    plt.title(f'IL Analysis for Position Range [{price_l:.2f}, {price_u:.2f}) with Initial Price {price_0:.2f}')
    plt.grid(True)
    plt.legend()
    plt.savefig('il.png')

if __name__ == "__main__":
    plot(1190, 1180, 1215)

# pi_l = q64_96_to_decimal(tick_l.to_sqrt_price_x96())
# pi_0 = q64_96_to_decimal(tick_0.to_sqrt_price_x96())
# del_l = decimal_to_q64_96(150_000)

# print((pi_0 - pi_l) * 150_000)
# print(q64_96_to_decimal(mul(tick_0.to_sqrt_price_x96() - tick_l.to_sqrt_price_x96(), del_l)))

# one = decimal_to_q64_96(1)
# tmp = div(one, tick_0.to_sqrt_price_x96()) - div(one, tick_u.to_sqrt_price_x96())
# del_l = decimal_to_q64_96(Decimal(150_000))

# print(q64_96_to_decimal(mul(tmp, del_l)))

# a = Decimal(120)
# b = Decimal(10)
# a_q = decimal_to_q64_96(a)
# b_q = decimal_to_q64_96(b)

# print(a/b)
# print(q64_96_to_decimal(div(a_q, b_q)))

# del_y = decimal_to_q64_96(Decimal(12352.33291083709617839496))
# print(q64_96_to_decimal(div(del_y, tick_0.to_sqrt_price_x96() - tick_l.to_sqrt_price_x96())))  

# del_x = decimal_to_q64_96(Decimal(4.09186496247326887556))
# one = decimal_to_q64_96(1)
# inv_tick_0 = div(one, tick_0.to_sqrt_price_x96())
# inv_tick_u = div(one, tick_u.to_sqrt_price_x96())

# print(q64_96_to_decimal(div(del_x, inv_tick_0 - inv_tick_u)))
def extended_euclidean_algorithm(m, n):
    """
    Extended Euclidean algorithm for two integers in base 10
    Input: m, n: two integers in base 10
    Output: d: the greatest common divisor of m and n in base 10; x, y: the coefficients of the identity d = mx + ny, in base 10
    """
    r_old = m
    r_new = n
    x_old = 1
    x_new = 0
    y_old = 0
    y_new = 1
    while r_new > 0:
        t = r_new
        q,r = divmod(r_old, t)
        r_new = r
        r_old = t
        tx = x_new
        x_new = x_old - q * tx
        x_old = tx
        ty = y_new
        y_new = y_old - q * ty
        y_old = ty
    return r_old, x_old, y_old

def inverse_modulo_n(x, n):
    """
    Inverse for an integer x modulo n in base b
    Input: x: an integer in base 10; n: an integer in base 10
    Output: i: the inverse of x in base 10
    """
    d, x, y = extended_euclidean_algorithm(x, n)
    if d != 1:
        return None
    else:
        return x % n

if __name__ == '__main__':
    # ---------- extended_euclidean_algorithm ----------
    d, x, y = extended_euclidean_algorithm(5, 0)
    assert d == 5
    assert x == 1
    assert y == 0

    d, x, y = extended_euclidean_algorithm(30, 12)  # gcd(30, 12)
    assert d == 6

    # ---------- inverse_modulo_n ----------
    inv = inverse_modulo_n(3, 7)
    # 3 * 5 = 15 ≡ 1 (mod 7)
    assert inv == 5

    # 不互素时返回 None
    assert inverse_modulo_n(2, 4) is None

    print("所有测试通过！")


def list_int_to_str(x, b):
    """
    Convert a list of digits in reverse order to an integer in base b
    Input: x: a list of digits in reverse order
    Output: n: the integer in base b
    """
    n = "("
    for i in range(len(x)-1, -1, -1):
        n += str(x[i])
    n += ")_" + str(b)
    return n

def _normalize(x):
    """Remove leading zeros from a list of digits in reverse order."""
    i = len(x) - 1
    while i > 0 and x[i] == 0:
        i -= 1
    return x[:i + 1]

def addition(x, y, b):
    """
    Addition algorithm for two integers
    Input: x, y: two integers in base b, represented as lists of digits in reverse order
    Output: z: the sum of x and y in base b, represented as a list of digits in reverse order
    """
    c = 0 # c is the carry digit
    z = [] # z is the sum of x and y in base b, represented as a list of digits in reverse order
    n1 = len(x)
    n2 = len(y)
    n = max(n1, n2)
    for i in range(n):
        s = c
        if i < n1:
            s += x[i]
        if i < n2:
            s += y[i]
        z.append(s % b)
        c = s // b
    if c > 0:
        z.append(c)
    return _normalize(z)

def multiplication_single_digit(x, y, b):
    """
    Multiplication algorithm for two integers
    Input: x: an integer in base b, represented as lists of digits in reverse order, y: a single digit in base b
    Output: z: the product of x and y in base b, represented as lists of digits in reverse order
    """
    c = 0
    z = []
    for i in range(len(x)):
        tmp = x[i] * y + c
        z.append(tmp % b)
        c = tmp // b
    if c > 0:
        z.append(c)
    return z

def multiplication(x, y, b):
    """
    Multiplication algorithm for two integers
    Input: x, y: two integers in base b, represented as lists of digits in reverse order
    Output: z: the product of x and y in base b, represented as lists of digits in reverse order
    """
    z = []
    for j in range(len(y)):
        x_pad = x[:]
        x_pad = [0]*j + x_pad
        z_tmp = multiplication_single_digit(x_pad, y[j], b)
        z = addition(z, z_tmp, b)
    return _normalize(z) if z else [0]

def repeated_squaring(x, y, b):
    """
    Repeated squaring algorithm for two integers
    Input: x: an integer in base b, represented as list of digits in reverse order; y: an integer in base 2, represented as list of digits in reverse order
    Output: z: the product of x and y in base b, represented as list of digits in reverse order
    """
    z = [1]
    p = x
    for i in range(len(y)):
        if y[i] == 1:
            z = multiplication(z, p, b)
        p = multiplication(p, p, b)
    return z

def subtraction(x, y, b):
    """
    Subtraction algorithm for two integers
    Input: x, y: two integers in base b, represented as lists of digits in reverse order
    Output: z: the difference of x and y in base b, represented as lists of digits in reverse order
    """
    if compare(x, y) < 0:
        # we only support subtraction when x >= y
        return None
    z = []
    borrow = 0
    for i in range(len(x)):
        xi = x[i]
        yi = y[i] if i < len(y) else 0
        s = xi - yi - borrow
        if s < 0:
            s += b
            borrow = 1
        else:
            borrow = 0
        z.append(s)
    return _normalize(z)

def compare(x, y):
    """
    Compare two integers in base b
    Input: x, y: two integers in base b, represented as lists of digits in reverse order
    Output: c: 0 if x = y, 1 if x > y, -1 if x < y
    """
    x = _normalize(x)
    y = _normalize(y)

    len_x = len(x)
    len_y = len(y)

    if len_x != len_y:
        return -1 if len_x < len_y else 1

    for k in range(len_x - 1, -1, -1):
        if x[k] != y[k]:
            return -1 if x[k] < y[k] else 1

    return 0

def quotient_remainder(m, n, b):
    """
    Algorithm for finding the quotient and remainder of dividing m by n
    Input: m: an integer in base b, represented as list of digits in reverse order; n: an integer in base b, represented as list of digits in reverse order
    Output: q, r: the quotient and remainder of m divided by n, represented as lists of digits in reverse order
    """
    m = _normalize(m)
    n = _normalize(n)

    r = m
    s = len(m)
    t = len(n)
    i = s-t
    q = [0]
    while compare(r, n) >= 0 :
        bi = [0] * i + [1]
        nbi = multiplication(n, bi, b)
        while compare(r, nbi) >= 0 :
            r = subtraction(r, nbi, b)
            q = addition(q, bi, b)
        if i > 0:
            i -= 1
    return q, r

def base_conversion_decimal_to_b(x, b):
    """
    Convert a decimal integer x to an integer in base b
    Input: x: a decimal integer represented as a list of digits in reverse order
    Output: n: the integer in base b, represented as a list of digits in reverse order
    """
    x = _normalize(x)
    n = []
    divisor = [0,1]
    while compare(x, [0]) > 0:
        q,r = quotient_remainder(x, divisor, b)
        n.append(r[0] if r else 0)
        x = q
    if not n:
        n = [0]
    return n

def base_conversion_b_to_decimal(x, b):
    """
    Convert an integer in base b to a decimal integer
    Input: x: an integer in base b, represented as a list of digits in reverse order
    Output: n: the decimal integer represented as a list of digits in reverse order
    """
    n = 0
    for i in range(len(x)-1,0,-1):
        n = (x[i] + n) * b 
    n = x[0] + n
    return n

def modulo(x, y, b):
    """
    Modulo operation for two integers in base b
    Input: x, y: two integers in base b, represented as lists of digits in reverse order
    Output: r: the remainder of x divided by y in base b, represented as lists of digits in reverse order
    """
    _,r = quotient_remainder(x, y, b)
    return r

def repeated_squaring_modulo_n(x, y, b, n):
    """
    Repeated squaring algorithm for two integers in base b, modulo n
    Input: x, y: two integers in base b, represented as lists of digits in reverse order
    Output: z: the product of x and y in base b, modulo n, represented as lists of digits in reverse order
    """
    z = [1]
    p = x
    for i in range(len(y)):
        if y[i] == 1:
            z = multiplication(z, p, b)
            z = modulo(z, n, b)
        p = multiplication(p, p, b)
        p = modulo(p, n, b)
    return z

def gcd(m, n, b):
    """
    Greatest common divisor algorithm for two integers in base b
    Input: m, n: two integers in base b, represented as lists of digits in reverse order
    Output: d: the greatest common divisor of m and n in base b, represented as lists of digits in reverse order
    """
    r_old = m
    r_new = n
    while compare(r_new, [0]) > 0:
        t = r_new
        _,r_new = quotient_remainder(r_old, t, b)
        r_old = t
    return r_old


def _int_to_list(num, b):
    if num < 0:
        num = -num
    if num == 0:
        return [0]
    digits = []
    while num > 0:
        digits.append(num % b)
        num //= b
    return digits



if __name__ == '__main__':
    # ---------- list_int_to_str ----------
    assert list_int_to_str([3, 2, 1], 10) == "(123)_10"
    assert list_int_to_str([1, 0, 1], 2) == "(101)_2"
    assert list_int_to_str([0], 10) == "(0)_10"

    # ---------- addition ----------
    assert addition([3, 2, 1], [6, 5, 4], 10) == [9, 7, 5]
    assert addition([9, 9, 9], [1], 10) == [0, 0, 0, 1]
    assert addition([1, 1, 0, 1], [1], 2) == [0, 0, 1, 1]
    assert addition([], [1, 2], 10) == [1, 2]

    # ---------- multiplication_single_digit ----------
    assert multiplication_single_digit([3, 2, 1], 4, 10) == [2, 9, 4]
    assert multiplication_single_digit([9, 9, 9], 9, 10) == [1, 9, 9, 8]
    assert multiplication_single_digit([1, 1, 0, 1], 1, 2) == [1, 1, 0, 1]

    # ---------- multiplication ----------
    assert multiplication([3, 2, 1], [6, 5, 4], 10) == [8, 8, 0, 6, 5]
    assert multiplication([1, 0, 1], [1, 1], 2) == [1, 1, 1, 1]
    assert multiplication([1, 1, 0, 1], [0], 2) == [0]

    # ---------- repeated_squaring ----------
    assert repeated_squaring([2], [0, 1], 10) == [4]            # 2^2 = 4
    assert repeated_squaring([3], [0, 0, 1], 10) == [1, 8]      # 3^4 = 81
    assert repeated_squaring([2], [0], 10) == [1]               # 2^0 = 1

    # ---------- subtraction ----------
    assert subtraction([6, 5, 4], [3, 2, 1], 10) == [3, 3, 3]
    assert subtraction([9, 9, 9], [1], 10) == [8, 9, 9]
    assert subtraction([0, 1], [1], 10) == [9]                  # 10 - 1 = 9
    assert subtraction([0, 0, 1], [1], 10) == [9, 9]            # 100 - 1 = 99

    # ---------- compare ----------
    assert compare([3, 2, 1], [3, 2, 1]) == 0
    assert compare([4, 2, 1], [3, 2, 1]) == 1
    assert compare([3, 2, 1], [4, 2, 1]) == -1
    assert compare([1], [0, 1]) == -1
    assert compare([1, 0], [1]) == 0                            # 忽略前导零

    # ---------- quotient_remainder ----------
    q, r = quotient_remainder([2], [5], 10)
    assert q == [0] and r == [2]

    q, r = quotient_remainder([7, 1], [5], 10)                  # 17 / 5
    assert q == [3] and r == [2]

    q, r = quotient_remainder([8, 4], [8, 1], 10)               # 48 / 18
    assert q == [2] and r == [2, 1]

    # ---------- base_conversion_decimal_to_b ----------
    assert base_conversion_decimal_to_b([0], 10) == [0]
    # 注意：该函数在数制 b 下做除法，因此对已经是数制 b 的输入相当于恒等
    assert base_conversion_decimal_to_b([0, 1], 2) == [0, 1]
    assert base_conversion_decimal_to_b([3, 2, 1], 10) == [3, 2, 1]

    # ---------- base_conversion_b_to_decimal ----------
    assert base_conversion_b_to_decimal([0, 1, 0, 1], 2) == 10
    assert base_conversion_b_to_decimal([3, 2, 1], 10) == 123
    assert base_conversion_b_to_decimal([0], 10) == 0

    # ---------- modulo ----------
    assert modulo([2], [5], 10) == [2]
    assert modulo([7, 1], [5], 10) == [2]                       # 17 mod 5 = 2

    # ---------- repeated_squaring_modulo_n ----------
    assert repeated_squaring_modulo_n([2], [0], 10, [5]) == [1]
    # 2^10 = 1024，1024 mod 1000 = 24
    # y = [0,1,0,1] 表示二进制 1010 = 10；n = [0,0,0,1] 表示十进制 1000
    res = repeated_squaring_modulo_n([2], [0, 1, 0, 1], 10, [0, 0, 0, 1])
    assert _normalize(res) == [4, 2]

    # ---------- gcd ----------
    assert gcd([5], [0], 10) == [5]
    assert gcd([0], [5], 10) == [5]
    assert gcd([8, 4], [8, 1], 10) == [6]                       # gcd(48, 18) = 6

    print("所有测试通过！")
   

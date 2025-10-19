class ALU:
    def add(self, x, y):
        while (x != 0):
            carry = y & x
            y = y ^ x
            x = carry << 1
        return y

    def sub(self, x, y):
        # Subtract using two's complement
        while (y != 0):
            borrow = (~x) & y
            x = x ^ y
            y = borrow << 1
        return x
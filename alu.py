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

    def mul(self, x, y):
        # Handle negatives
        neg = (x < 0) ^ (y < 0)
        x = abs(x)
        y = abs(y)

        result = 0
        while y > 0:
            if y & 1:  # If LSB of y is set
                result = self.add(result, x)
            x <<= 1
            y >>= 1

        return -result if neg else result

    def div(self, x, y):
        if y == 0:
            raise ZeroDivisionError("Division by zero")

        # Handle negatives
        neg = (x < 0) ^ (y < 0)
        x = abs(x)
        y = abs(y)

        quotient = 0
        remainder = 0

        for i in range(x.bit_length() - 1, -1, -1):
            remainder = (remainder << 1) | ((x >> i) & 1)
            if remainder >= y:
                remainder = self.sub(remainder, y)
                quotient |= (1 << i)

        return -quotient if neg else quotient

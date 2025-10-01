class BitwiseExample:
    def __init__(self, value):
        self.value = value

    def __ilshift__(self, other):
        self.value <<= other
        print(f"After <<= {other} :", self.value)
        return self

    def __irshift__(self, other):
        self.value >>= other
        print(f"After >>= {other} :", self.value)
        return self

    def __iand__(self, other):
        self.value &= other
        print(f"After &= {other}  :", self.value)
        return self

    def __ixor__(self, other):  
        self.value ^= other
        print(f"After ^= {other}  :", self.value)
        return self

    def __ior__(self, other):
        self.value |= other
        print(f"After |= {other}  :", self.value)
        return self

# Example usage
num = BitwiseExample(5)  # 0b101

num <<= 1  # Left Shift
num = BitwiseExample(5)  # Reset
num >>= 1  # Right Shift
num = BitwiseExample(5)  # Reset
num &= 3   # Bitwise AND
num = BitwiseExample(5)  # Reset
num ^= 3   # Bitwise XOR
num = BitwiseExample(5)  # Reset
num |= 3   # Bitwise OR

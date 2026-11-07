class Int_32_Bit:
    def __init__(self, value: int) -> None:
        self.value = value

    def get_value(self) -> int:
        return self.value

    def get_value_hex(self) -> str:
        return hex(self.value)

    def set_value(self, value: int) -> None:
        if value > 2147483647 or value < -2147483648:
            raise RuntimeError("Arithmetic Overflow")
        self.value = value
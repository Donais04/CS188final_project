class Int_32_Bit:
    MASK = 0xFFFFFFFF # ChatGPT taught me how bitmasks work

    def __init__(self, value: int = 0) -> None:
        self.value = value & self.MASK

    def get_value(self) -> int:
        return self.value

    def set_value(self, value: int) -> None:
        self.value = value & self.MASK
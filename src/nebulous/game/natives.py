from dataclasses import dataclass
from typing import ClassVar, Self

from datastream import DeserializingStream


@dataclass
class MUTF8String:
    MAX_LENGTH: ClassVar[int] = 0xFFFF

    length: int  # 2 bytes
    _value: str

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        # max length is implicitly implied by the way the JDK encodes strings
        if len(value) > MUTF8String.MAX_LENGTH:
            raise ValueError("String is too long")

        self.length = len(value)
        self._value = value

    def encode(self) -> bytes:
        return self.length.to_bytes(2, byteorder="big") + self._value.encode("utf-8")

    @classmethod
    def from_py_string(cls, value: str) -> Self:
        return cls(len(value), value)

    @classmethod
    def from_stream(cls, stream: DeserializingStream) -> Self:
        length = stream.read_uint16()
        value = stream.read(length).decode("utf-8", errors="backslashreplace")

        return cls(length, value)


@dataclass
class VariableLengthArray:
    """
    An array of bytes whose encoded length can vary in byte length.
    """
    size: int
    values: list[int]

    def encode(self) -> bytes:
        if len(self.values) > (1 << (8 * self.size)) - 1:
            raise ValueError("Array is too long")

        buf = bytearray()
        buf.extend(len(self.values).to_bytes(self.size, byteorder="big"))

        for value in self.values:
            buf.append(value & 0xFF)


        return bytes(buf)

    @classmethod
    def from_stream(cls, size: int, stream: DeserializingStream) -> Self:
        length = int.from_bytes(stream.read(size), signed=True)
        values = [stream.read_int8() for _ in range(length)]

        return cls(size, values)


@dataclass
class CompressedFloat:
    value: float
    max_range: float

    def compress(self) -> int:
        return int(((self.value - 0.0) * 65535.0) / (self.max_range - 0.0))

    def compress_1_clamp(self, min_v: float) -> int:
        return int(((self.value - min_v) * 255.0) / (self.max_range - min_v))

    @classmethod
    def decompress(cls, value: int, max_range: float) -> Self:
        return cls((((max_range - 0.0) * (value & 0xFFFF)) / 65535.0) + 0.0, max_range)

    @classmethod
    def from_stream(cls, max_range: float, stream: DeserializingStream) -> Self:
        return cls.decompress(stream.read_uint16(), max_range)

    @classmethod
    def from_3(cls, max_range, stream: DeserializingStream) -> Self:
        b24_16 = stream.read_uint8() << 16
        b15_8 = stream.read_uint8() << 8
        b7_0 = stream.read_uint8()

        a = b24_16 + b15_8 + b7_0

        return cls((((max_range - 0.0) * a) / 1.6777215e7) + 0.0, max_range)

    @classmethod
    def from_1_clamped(cls, min_v: float, max_v: float, stream: DeserializingStream) -> Self:
        value = stream.read_uint8()

        return cls((((max_v - min_v) * (value & 0xFF)) / 255.0) + min_v, max_v)


def xp2level(xp: int) -> int:
    if xp < 0:
        return 1

    return int((xp / 500) ** 0.5) + 1

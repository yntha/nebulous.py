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
        value = stream.read(length).decode("utf-8")

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

        return cls(length, values)


@dataclass
class CompressedFloat:
    value: float
    max_range: float

    def compress(self) -> int:
        return int(((self.value - 0.0) * 65535.0) / (self.max_range - 0.0))

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

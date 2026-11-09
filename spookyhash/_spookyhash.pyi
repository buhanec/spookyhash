"""Type stubs for SpookyHash Cython code."""

from typing import ClassVar

from typing_extensions import Self, disjoint_base

__all__ = ("hash32", "hash64", "hash128", "Hash", "Hash32", "Hash64", "Hash128")
__version__: str

def hash32(message: bytes | memoryview[bytes], seed: int = 0) -> int: ...


def hash64(message: bytes | memoryview[bytes], seed: int = 0) -> int: ...


def hash128(message: bytes | memoryview[bytes], seed1: int = 0, seed2: int = 0) -> bytes: ...


@disjoint_base
class Hash:
    def __new__(cls, seed1: int, seed2: int) -> Self: ...

    digest_size: ClassVar[int]

    def update(self, message: bytes | memoryview[bytes]) -> None: ...

    def digest(self) -> bytes: ...


class Hash32(Hash): ...


class Hash64(Hash): ...


class Hash128(Hash): ...

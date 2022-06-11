"""A Python wrapper for SpookyHash version 2."""

import struct
from abc import ABC, abstractmethod
from binascii import hexlify
from typing import ClassVar, TYPE_CHECKING, Tuple, Type, Union, cast

import _spookyhash

if TYPE_CHECKING:
    from typing import Self

__all__ = ('hash32', 'hash64', 'hash128', 'Hash32', 'Hash64', 'Hash128')
__version__ = '2.1.0'


# Utility function for homogenising data

def _char_arr(message: Union[bytes, memoryview, None]) -> Tuple[memoryview, int]:
    if message is None:
        return memoryview(b'').cast('c'), 0
    if not isinstance(message, memoryview):
        try:
            message = memoryview(message)
        except TypeError as e:
            raise TypeError(
                f"Expecting message to by bytes, memoryview, None, or a type "
                f"that can be interpreted as as memoryview (e.g. NumPy "
                f"arrays); instead found "
                f"{type(message).__module__}.{type(message).__name__}"
            ) from e
    if message.format != 'c' or not message.contiguous:
        message = message.cast('c')
    return message, len(message)


# Oneshot hash functions

def hash32(message: Union[bytes, memoryview], seed: int = 0) -> int:
    """
    Hash a single message in one call, produce 32-bit output.

    :param message: message to hash
    :param seed: 32-bit seed
    :return: 32-bit hash
    """
    return _spookyhash.hash32(*_char_arr(message), seed)


def hash64(message: Union[bytes, memoryview], seed: int = 0) -> int:
    """
    Hash a single message in one call, produce 64-bit output.

    :param message: message to hash
    :param seed: 64-bit seed
    :return: 64-bit hash
    """
    return _spookyhash.hash64(*_char_arr(message), seed)


def hash128_pair(
    message: Union[bytes, memoryview],
    seed1: int = 0,
    seed2: int = 0,
) -> Tuple[int, int]:
    """
    Hash a single message in one call, produce 128-bit output.

    :param message: message to hash
    :param seed1: 64-bit seed 1
    :param seed2: 64-bit seed 2
    :return: Pair of 64-bit hash values
    """
    digest = _spookyhash.hash128(*_char_arr(message), seed1=seed1, seed2=seed2)
    return cast(Tuple[int, int], struct.unpack('=QQ', digest))


def hash128(
    message: Union[bytes, memoryview],
    seed1: int = 0,
    seed2: int = 0,
) -> int:
    """
    Hash a single message in one call, produce 128-bit output.

    :param message: message to hash
    :param seed1: 64-bit seed 1
    :param seed2: 64-bit seed 2
    :return: 128-bit hash
    """
    val1, val2 = hash128_pair(message, seed1=seed1, seed2=seed2)
    return val2 << 64 | val1


# Incremental hash builders

class Hash(ABC):
    """Base class for incremental hash builders."""

    digest_size: ClassVar[int]
    _hash_cls: ClassVar[Type[_spookyhash.Hash]]

    def __init__(
        self,
        message: Union[bytes, memoryview, None] = None,
        seed1: int = 0,
        seed2: int = 0,
    ) -> None:
        """
        Initialise hash.

        :param message: Optional initial message fragment
        :param seed1: first seed
        :param seed2: second seed
        """
        self._hash = self._hash_cls(seed1, seed2)
        if message is not None:
            self.update(message)

    @property
    def digest_size(self) -> int:
        """
        Digest size.

        :return: Digest size
        """
        return self._hash.digest_size

    def update(self, message: Union[bytes, memoryview, None]) -> 'Self':
        """
        Incrementally update hash with message fragment.

        :param message: Message fragment
        :return: Self
        """
        if message is not None:
            self._hash.update(*_char_arr(message))
        return self

    def digest(self) -> bytes:
        """
        Compute digest.

        :return: Digest
        """
        return self._hash.digest()

    def hexdigest(self) -> str:
        """
        Compute hex digest.

        :return: Hex digest
        """
        return hexlify(self.digest()).decode('utf-8')

    @abstractmethod
    def final(self) -> int:
        """
        Compute the hash for the concatenation of all message fragments.

        :return: Hash
        """
        return NotImplemented


class Hash32(Hash):
    """32-bit incremental hash builder."""

    _hash_cls = _spookyhash.Hash32

    def __init__(
        self,
        message: Union[bytes, memoryview, None] = None,
        seed: int = 0,
    ) -> None:
        """
        Initialise 32-bit hash.

        :param message: Optional initial message fragment
        :param seed: 32-bit seed
        """
        super().__init__(message, seed, seed)

    def final(self) -> int:
        """
        Compute the hash for the concatenation of all message fragments.

        :return: Hash
        """
        return struct.unpack('=L', self.digest())[0]


class Hash64(Hash):

    _hash_cls = _spookyhash.Hash64

    def __init__(
        self,
        message: Union[bytes, memoryview, None] = None,
        seed: int = 0,
    ) -> None:
        """
        Initialise 64-bit hash.

        :param message: Optional initial message fragment
        :param seed: 64-bit seed
        """
        super().__init__(message, seed, seed)

    def final(self) -> int:
        """
        Compute the hash for the concatenation of all message fragments.

        :return: Hash
        """
        return struct.unpack('=Q', self.digest())[0]


class Hash128(Hash):

    _hash_cls = _spookyhash.Hash128

    def final_pair(self) -> Tuple[int, int]:
        """
        Compute the hash for the concatenation of all message fragments.

        Returns a pair of 64-bit integer to match other common implementations.

        :return: Pair of 64-bit integers representing the hash
        """
        return cast(Tuple[int, int], struct.unpack('=QQ', self.digest()))

    def final(self) -> int:
        """
        Compute the hash for the concatenation of all message fragments.

        :return: Hash
        """
        hash1, hash2 = self.final_pair()
        return hash2 << 64 | hash1

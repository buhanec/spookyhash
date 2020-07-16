from typing import Tuple

import binascii
import struct
from libc.stdint cimport uint32_t, uint64_t

cimport SpookyV2

__all__ = ('hash32', 'hash64', 'hash128', 'Hash32', 'Hash64', 'Hash128')
__version__ = '2.0.0'

# Oneshot hash functions

cpdef uint32_t _hash32(bytes message, uint32_t seed=0):
    return SpookyV2.Hash32(message, len(message), seed)

def hash32(message: bytes, seed: int = 0) -> int:
    """
    Hash a single message in one call, produce 32-bit output.

    :param message: message to hash
    :param seed: 32-bit seed
    :return: 32-bit hash
    """
    return _hash32(message, seed)

cpdef uint64_t _hash64(bytes message, uint64_t seed=0):
    return SpookyV2.Hash64(message, len(message), seed)

def hash64(message: bytes, seed: int = 0) -> int:
    """
    Hash a single message in one call, produce 64-bit output.

    :param message: message to hash
    :param seed: 64-bit seed
    :return: 64-bit hash
    """
    return _hash64(message, seed)

cpdef bytes _hash128(bytes message, uint64_t seed1=0, uint64_t seed2=0):
    cdef char digest[16]
    (<uint64_t*> &digest[0])[0] = seed1
    (<uint64_t*> &digest[8])[0] = seed2
    SpookyV2.Hash128(message, len(message), <uint64_t*> digest, <uint64_t*> (digest + 8))
    return digest[:16]

def hash128_pair(message: bytes, seed1: int = 0, seed2: int = 0) -> Tuple[int, int]:
    """
    Hash a single message in one call, produce 128-bit output.

    :param message: message to hash
    :param seed1: 64-bit seed 1
    :param seed2: 64-bit seed 2
    :return: Pair of 64-bit hash values
    """
    digest = _hash128(message, seed1=seed1, seed2=seed2)
    return struct.unpack('=QQ', digest)

def hash128(message: bytes, seed1: int = 0, seed2: int = 0) -> int:
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

cdef class _Hash:
    cdef SpookyV2.SpookyHash __hash
    cdef readonly int digest_size

    def __cinit__(_Hash self, *args, **kwargs):
        pass

    cpdef _Hash update(_Hash self, bytes message):
        self.__hash.Update(message, len(message))
        return self

    cpdef bytes digest(_Hash self):
        cdef uint64_t digest[2]
        self.__hash.Final(&digest[0], &digest[1])
        return (<char*> digest)[:self.digest_size]

    cpdef bytes hexdigest(_Hash self):
        return binascii.hexlify(self.digest())

    cpdef int final(_Hash self):
        raise NotImplementedError()

    property block_size:
        def __get__(_Hash self):
            return 16

cdef class Hash32(_Hash):
    def __init__(self, message: bytes = None, seed: int = 0) -> None:
        """
        Initialise 32-bit hash.

        :param message: Optional initial message fragment
        :param seed: 32-bit seed
        """
        pass

    def __cinit__(Hash32 self, bytes message=None, uint32_t seed=0):
        self.digest_size = 4
        self.__hash.Init(seed, seed)
        if message:
            self.__hash.Update(message, len(message))

    def final(Hash32 self) -> int:
        """
        Report the hash for the concatenation of all message fragments so far.
        """
        cdef uint64_t hash1, hash2
        self.__hash.Final(&hash1, &hash2)
        return <uint32_t> hash1

cdef class Hash64(_Hash):
    def __init__(self, message: bytes = None, seed: int = 0) -> None:
        """
        Initialise 64-bit hash.

        :param message: Optional initial message fragment
        :param seed: 64-bit seed
        """
        pass

    def __cinit__(Hash64 self, bytes message=None, uint64_t seed=0):
        self.digest_size = 8
        self.__hash.Init(seed, seed)
        if message:
            self.__hash.Update(message, len(message))

    def final(Hash64 self) -> int:
        """
        Report the hash for the concatenation of all message fragments so far.
        """
        cdef uint64_t hash1, hash2
        self.__hash.Final(&hash1, &hash2)
        return hash1

cdef class Hash128(_Hash):
    def __init__(self, message: bytes = None, seed1: int = 0, seed2: int = 0) -> None:
        """
        Initialise 128-bit hash.

        :param message: Optional initial message fragment
        :param seed1: 64-bit seed 1
        :param seed2: 64-bit seed 2
        """
        pass

    def __cinit__(Hash128 self, bytes message=None, uint64_t seed1=0, uint64_t seed2=0):
        self.digest_size = 16
        self.__hash.Init(seed1, seed2)
        if message:
            self.__hash.Update(message, len(message))

    def final_pair(Hash128 self) -> Tuple[int, int]:
        """
        Report the hash for the concatenation of all message fragments so far.

        Returns a pair of 64-bit integer to match other common implementations.
        """
        return struct.unpack('=QQ', self.digest())

    def final(Hash128 self) -> int:
        """
        Report the hash for the concatenation of all message fragments so far.
        """
        hash1, hash2 = self.final_pair()
        return hash2 << 64 | hash1

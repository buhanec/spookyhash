"""SpookyHash Cython code."""

from libc.stdint cimport uint8_t, uint32_t, uint64_t


cimport SpookyV2

__all__ = ('hash32', 'hash64', 'hash128', 'Hash', 'Hash32', 'Hash64', 'Hash128')
__version__ = '2.1.2'


# Oneshot hash functions

cpdef uint32_t hash32(
    const uint8_t[::1] message,
    uint32_t seed=0,
):
    cdef uint32_t ret
    with nogil:
        ret = SpookyV2.Hash32(
        <const char*>&message[0],
        <size_t>message.shape[0],
        seed)
    return ret


cpdef uint64_t hash64(
    const uint8_t[::1] message,
    uint64_t seed=0,
):
    cdef uint64_t ret
    with nogil:
        ret = SpookyV2.Hash64(
        <const char*>&message[0],
        <size_t>message.shape[0],
        seed)
    return ret


cpdef bytes hash128(
    const uint8_t[::1] message,
    uint64_t seed1=0,
    uint64_t seed2=0,
):
    cdef char digest[16]
    (<uint64_t*> &digest[0])[0] = seed1
    (<uint64_t*> &digest[8])[0] = seed2
    with nogil:
        SpookyV2.Hash128(
            <const char*>&message[0],
            <size_t>message.shape[0],
            <uint64_t*> digest,
            <uint64_t*> (digest + 8),
        )
    return digest[:16]


# Incremental hash builders

cdef class Hash:
    cdef SpookyV2.SpookyHash hash
    cdef readonly int digest_size

    def __cinit__(Hash self, *args, **kwargs):
        pass

    cpdef void update(Hash self, const uint8_t[::1] message):
        with nogil:
            self.hash.Update(
                <const char*>&message[0],
                <size_t>message.shape[0],
            )

    cpdef bytes digest(Hash self):
        cdef uint64_t digest[2]
        with nogil:
            self.hash.Final(&digest[0], &digest[1])
        return (<char*> digest)[:self.digest_size]


cdef class Hash32(Hash):

    def __cinit__(Hash32 self, uint32_t seed1, uint32_t seed2):
        if seed1 != seed2:
            raise ValueError('Expecting seed1 and seed2 to be the same')
        with nogil:
            self.hash.Init(seed1, seed1)
        self.digest_size = 4


cdef class Hash64(Hash):

    def __cinit__(Hash64 self, uint64_t seed1, uint64_t seed2):
        if seed1 != seed2:
            raise ValueError('Expecting seed1 and seed2 to be the same')
        with nogil:
            self.hash.Init(seed1, seed1)
        self.digest_size = 8


cdef class Hash128(Hash):

    def __cinit__(Hash128 self, uint64_t seed1, uint64_t seed2):
        with nogil:
            self.hash.Init(seed1, seed2)
        self.digest_size = 16

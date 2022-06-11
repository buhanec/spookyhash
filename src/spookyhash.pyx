"""SpookyHash Cython code."""

from libc.stdint cimport uint32_t, uint64_t


cimport SpookyV2

__all__ = ('hash32', 'hash64', 'hash128', 'Hash', 'Hash32', 'Hash64', 'Hash128')
__version__ = '2.1.0'


# Oneshot hash functions

cpdef uint32_t hash32(
    const char[::1] message,
    size_t length,
    uint32_t seed=0,
):
    return SpookyV2.Hash32(
        &message[0] if length else NULL,
        length,
        seed,
    )


cpdef uint64_t hash64(
    const char[::1] message,
    size_t length,
    uint64_t seed=0,
):
    return SpookyV2.Hash64(
        &message[0] if length else NULL,
        length,
        seed,
    )


cpdef bytes hash128(
    const char[::1] message,
    size_t length,
    uint64_t seed1=0,
    uint64_t seed2=0,
):
    cdef char digest[16]
    (<uint64_t*> &digest[0])[0] = seed1
    (<uint64_t*> &digest[8])[0] = seed2
    SpookyV2.Hash128(
        &message[0] if length else NULL,
        length,
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

    cpdef void update(Hash self, const char[::1] message, size_t length):
        self.hash.Update(
            &message[0] if length else NULL,
            length,
        )

    cpdef bytes digest(Hash self):
        cdef uint64_t digest[2]
        self.hash.Final(&digest[0], &digest[1])
        return (<char*> digest)[:self.digest_size]


cdef class Hash32(Hash):

    def __cinit__(Hash32 self, uint32_t seed1, uint32_t seed2):
        if seed1 != seed2:
            raise ValueError('Expecting seed1 and seed2 to be the same')
        self.hash.Init(seed1, seed1)
        self.digest_size = 4


cdef class Hash64(Hash):

    def __cinit__(Hash64 self, uint64_t seed1, uint64_t seed2):
        if seed1 != seed2:
            raise ValueError('Expecting seed1 and seed2 to be the same')
        self.hash.Init(seed1, seed1)
        self.digest_size = 8


cdef class Hash128(Hash):

    def __cinit__(Hash128 self, uint64_t seed1, uint64_t seed2):
        self.hash.Init(seed1, seed2)
        self.digest_size = 16

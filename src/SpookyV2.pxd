from libc.stdint cimport uint32_t, uint64_t

cdef extern from 'SpookyV2.h':
  cdef cppclass SpookyHash:
    void Init(uint64_t seed1, uint64_t seed2)
    void Update(const char *message, size_t length)
    void Final(uint64_t *hash1, uint64_t *hash2)

cdef extern from 'SpookyV2.h' namespace 'SpookyHash':
    void Hash128(const char *message, size_t length, uint64_t *hash1, uint64_t *hash2)
    uint64_t Hash64(const char *message, size_t length, uint64_t seed)
    uint32_t Hash32(const char *message, size_t length, uint32_t seed)

from binascii import hexlify
import struct

from hypothesis import example, given
from hypothesis.strategies import binary, integers, lists
import pytest

import spookyhash


FRAGMENTS = integers(0, 5).flatmap(lambda n: lists(binary(min_size=0, max_size=1000), max_size=n))


@pytest.mark.parametrize('fragments, seed, expected', [
    ([b'hello', b'world'],
     0x00000000,
     0x478a7df4)
])
def test_hash32_inc(fragments, seed, expected):
    initial, *fragments = fragments
    sh = spookyhash.Hash32(initial, seed=seed)
    for fragment in fragments:
        sh.update(fragment)
    assert sh.final() == expected


@given(fragments=FRAGMENTS,
       seed=integers(min_value=0, max_value=2**32 - 1))
@example(fragments=[],
         seed=0x00000000)
@example(fragments=[b'hello', b'world'],
         seed=0x00000000)
def test_hash32_inc_consistent(fragments, seed):
    if len(fragments) > 1:
        initial, *fragments = fragments
    else:
        initial = None
    sh = spookyhash.Hash32(initial, seed=seed)
    for fragment in fragments:
        sh.update(fragment)
    assert sh.digest_size == 4
    assert struct.unpack('=L', sh.digest())[0] == sh.final()
    assert sh.hexdigest() == hexlify(sh.digest()).decode('utf-8')


@pytest.mark.parametrize('fragments, seed, expected', [
    ([b'hello', b'world'],
     0x0000000000000000,
     0x4f6bdd7d478a7df4)
])
def test_hash64_inc(fragments, seed, expected):
    initial, *fragments = fragments
    sh = spookyhash.Hash64(initial, seed=seed)
    for fragment in fragments:
        sh.update(fragment)
    assert sh.final() == expected


@given(fragments=FRAGMENTS,
       seed=integers(min_value=0, max_value=2**64 - 1))
@example(fragments=[],
         seed=0x0000000000000000)
@example(fragments=[b'hello', b'world'],
         seed=0x0000000000000000)
def test_hash64_inc_consistent(fragments, seed):
    if len(fragments) > 1:
        initial, *fragments = fragments
    else:
        initial = None
    sh = spookyhash.Hash64(initial, seed=seed)
    for fragment in fragments:
        sh.update(fragment)
    assert sh.digest_size == 8
    assert struct.unpack('=Q', sh.digest())[0] == sh.final()
    assert sh.hexdigest() == hexlify(sh.digest()).decode('utf-8')


@pytest.mark.parametrize('fragments, seed1, seed2, expected1, expected2', [
    ([b'hello', b'world'],
     0x0000000000000000,
     0x0000000000000000,
     0x4f6bdd7d478a7df4,
     0x0d8396833f493bbf)
])
def test_hash128_inc(fragments, seed1, seed2, expected1, expected2):
    initial, *fragments = fragments
    sh = spookyhash.Hash128(initial, seed1=seed1, seed2=seed2)
    for fragment in fragments:
        sh.update(fragment)
    assert sh.final_pair() == (expected1, expected2)
    assert sh.final() == expected2 << 64 | expected1


@given(fragments=FRAGMENTS,
       seed1=integers(min_value=0, max_value=2**64 - 1),
       seed2=integers(min_value=0, max_value=2**64 - 1))
@example(fragments=[],
         seed1=0x0000000000000000,
         seed2=0x0000000000000000)
@example(fragments=[b'hello', b'world'],
         seed1=0x0000000000000000,
         seed2=0x0000000000000000)
def test_hash128_inc_consistent(fragments, seed1, seed2):
    if len(fragments) > 1:
        initial, *fragments = fragments
    else:
        initial = None
    sh = spookyhash.Hash128(initial, seed1=seed1, seed2=seed2)
    for fragment in fragments:
        sh.update(fragment)
    assert sh.digest_size == 16
    assert struct.unpack('=QQ', sh.digest()) == sh.final_pair()
    assert sh.final_pair()[1] << 64 | sh.final_pair()[0] == sh.final()
    assert sh.hexdigest() == hexlify(sh.digest()).decode('utf-8')


@pytest.mark.parametrize('message, seed, expected', [
    (b'hi', 0x00000000, 0x9aa6d50f),
    (b'helloworld', 0x00000000, 0x478a7df4),
])
def test_hash32_oneshot(message, seed, expected):
    assert spookyhash.hash32(message, seed=seed) == expected


@given(message=binary(min_size=0, max_size=5000),
       seed=integers(min_value=0, max_value=2**32 - 1))
@example(message=b'hi',
         seed=0x00000000)
@example(message=b'helloworld',
         seed=0x00000000)
def test_hash32_oneshot_consistent(message, seed):
    assert 0 <= spookyhash.hash32(message, seed=seed) < 2 ** 32


@pytest.mark.parametrize('message, seed, expected', [
    (b'hi', 0x0000000000000000, 0xcd5a772a9aa6d50f),
    (b'helloworld', 0x0000000000000000, 0x4f6bdd7d478a7df4),
])
def test_hash64_oneshot(message, seed, expected):
    assert spookyhash.hash64(message, seed=seed) == expected


@given(message=binary(min_size=0, max_size=5000),
       seed=integers(min_value=0, max_value=2**64 - 1))
@example(message=b'hi',
         seed=0x0000000000000000)
@example(message=b'helloworld',
         seed=0x0000000000000000)
def test_hash64_oneshot_consistent(message, seed):
    assert 0 <= spookyhash.hash64(message, seed=seed) < 2 ** 64


@pytest.mark.parametrize('message, seed1, seed2, expected1, expected2', [
    (b'hi',
     0x0000000000000000,
     0x0000000000000000,
     0xcd5a772a9aa6d50f,
     0x1d63a8dcb6d1ed50),
    (b'helloworld',
     0x0000000000000000,
     0x0000000000000000,
     0x4f6bdd7d478a7df4,
     0x0d8396833f493bbf),
])
def test_hash128_oneshot(message, seed1, seed2, expected1, expected2):
    assert spookyhash.hash128_pair(message, seed1=seed1, seed2=seed2) == (expected1, expected2)
    assert spookyhash.hash128(message, seed1=seed1, seed2=seed2) == expected2 << 64 | expected1


@given(message=binary(min_size=0, max_size=5000),
       seed1=integers(min_value=0, max_value=2**64 - 1),
       seed2=integers(min_value=0, max_value=2**64 - 1))
@example(message=b'hi',
         seed1=0x0000000000000000,
         seed2=0x0000000000000000)
@example(message=b'helloworld',
         seed1=0x0000000000000000,
         seed2=0x0000000000000000)
def test_hash128_oneshot_consistent(message, seed1, seed2):
    hash1, hash2 = spookyhash.hash128_pair(message, seed1=seed1, seed2=seed2)
    hash_full = spookyhash.hash128(message, seed1=seed1, seed2=seed2)

    assert hash_full == hash2 << 64 | hash1
    assert 0 <= hash1 < 2**64
    assert 0 <= hash2 < 2**64
    assert 0 <= hash_full < 2**128

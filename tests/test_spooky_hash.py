"""Test public API for Python wrapper for SpookyHash version 2."""

from __future__ import annotations

from binascii import hexlify
import struct

from hypothesis import example, given
from hypothesis.strategies import binary, integers, lists
import pytest

import spookyhash

FRAGMENTS = integers(0, 5).flatmap(lambda n: lists(binary(min_size=0, max_size=1000), max_size=n))


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@pytest.mark.parametrize(
    "fragments, seed, expected",
    [
        pytest.param([b"hello", b"world"], 0x00000000, 0x478A7DF4, id="hello-world"),
    ],
)
def test_hash32_inc(
    fragments: list[bytes],
    seed: int,
    expected: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    initial, *fragments = fragments
    sh = spookyhash.Hash32(data_type(initial), seed=seed)
    for fragment in fragments:
        sh.update(data_type(fragment))
    assert sh.final() == expected


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@given(fragments=FRAGMENTS, seed=integers(min_value=0, max_value=2**32 - 1))
@example(fragments=[], seed=0x00000000)
@example(fragments=[b"hello", b"world"], seed=0x00000000)
def test_hash32_inc_consistent(
    fragments: list[bytes],
    seed: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    if len(fragments) > 1:
        initial_bytes, *fragments = fragments
        initial = data_type(initial_bytes)
    else:
        initial = None
    sh = spookyhash.Hash32(initial, seed=seed)
    for fragment in fragments:
        sh.update(data_type(fragment))
    assert sh.digest_size == 4
    assert struct.unpack("=L", sh.digest())[0] == sh.final()
    assert sh.hexdigest() == hexlify(sh.digest()).decode("utf-8")


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@pytest.mark.parametrize(
    "fragments, seed, expected",
    [
        pytest.param(
            [b"hello", b"world"],
            0x0000000000000000,
            0x4F6BDD7D478A7DF4,
            id="hello-world",
        ),
    ],
)
def test_hash64_inc(
    fragments: list[bytes],
    seed: int,
    expected: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    initial, *fragments = fragments
    sh = spookyhash.Hash64(data_type(initial), seed=seed)
    for fragment in fragments:
        sh.update(data_type(fragment))
    assert sh.final() == expected


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@given(fragments=FRAGMENTS, seed=integers(min_value=0, max_value=2**64 - 1))
@example(fragments=[], seed=0x0000000000000000)
@example(fragments=[b"hello", b"world"], seed=0x0000000000000000)
def test_hash64_inc_consistent(
    fragments: list[bytes],
    seed: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    if len(fragments) > 1:
        initial_bytes, *fragments = fragments
        initial = data_type(initial_bytes)
    else:
        initial = None
    sh = spookyhash.Hash64(initial, seed=seed)
    for fragment in fragments:
        sh.update(data_type(fragment))
    assert sh.digest_size == 8
    assert struct.unpack("=Q", sh.digest())[0] == sh.final()
    assert sh.hexdigest() == hexlify(sh.digest()).decode("utf-8")


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@pytest.mark.parametrize(
    "fragments, seed1, seed2, expected1, expected2",
    [
        pytest.param(
            [b"hello", b"world"],
            0x0000000000000000,
            0x0000000000000000,
            0x4F6BDD7D478A7DF4,
            0x0D8396833F493BBF,
            id="hello-world",
        ),
    ],
)
def test_hash128_inc(
    fragments: list[bytes],
    seed1: int,
    seed2: int,
    expected1: int,
    expected2: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    initial, *fragments = fragments
    sh = spookyhash.Hash128(data_type(initial), seed1=seed1, seed2=seed2)
    for fragment in fragments:
        sh.update(data_type(fragment))
    assert sh.final_pair() == (expected1, expected2)
    assert sh.final() == expected2 << 64 | expected1


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@given(
    fragments=FRAGMENTS,
    seed1=integers(min_value=0, max_value=2**64 - 1),
    seed2=integers(min_value=0, max_value=2**64 - 1),
)
@example(
    fragments=[],
    seed1=0x0000000000000000,
    seed2=0x0000000000000000,
)
@example(fragments=[b"hello", b"world"], seed1=0x0000000000000000, seed2=0x0000000000000000)
def test_hash128_inc_consistent(
    fragments: list[bytes],
    seed1: int,
    seed2: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    if len(fragments) > 1:
        initial_bytes, *fragments = fragments
        initial = data_type(initial_bytes)
    else:
        initial = None
    sh = spookyhash.Hash128(initial, seed1=seed1, seed2=seed2)
    for fragment in fragments:
        sh.update(data_type(fragment))
    assert sh.digest_size == 16
    assert struct.unpack("=QQ", sh.digest()) == sh.final_pair()
    assert sh.final_pair()[1] << 64 | sh.final_pair()[0] == sh.final()
    assert sh.hexdigest() == hexlify(sh.digest()).decode("utf-8")


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@pytest.mark.parametrize(
    "message, seed, expected",
    [
        (b"hi", 0x00000000, 0x9AA6D50F),
        (b"helloworld", 0x00000000, 0x478A7DF4),
    ],
)
def test_hash32_oneshot(
    message: bytes,
    seed: int,
    expected: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    assert spookyhash.hash32(data_type(message), seed=seed) == expected


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@given(
    message=binary(min_size=0, max_size=5000),
    seed=integers(min_value=0, max_value=2**32 - 1),
)
@example(message=b"hi", seed=0x00000000)
@example(message=b"helloworld", seed=0x00000000)
def test_hash32_oneshot_consistent(
    message: bytes,
    seed: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    assert 0 <= spookyhash.hash32(data_type(message), seed=seed) < 2**32


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@pytest.mark.parametrize(
    "message, seed, expected",
    [
        (b"hi", 0x0000000000000000, 0xCD5A772A9AA6D50F),
        (b"helloworld", 0x0000000000000000, 0x4F6BDD7D478A7DF4),
    ],
)
def test_hash64_oneshot(
    message: bytes,
    seed: int,
    expected: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    assert spookyhash.hash64(data_type(message), seed=seed) == expected


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@given(
    message=binary(min_size=0, max_size=5000),
    seed=integers(min_value=0, max_value=2**64 - 1),
)
@example(message=b"hi", seed=0x0000000000000000)
@example(message=b"helloworld", seed=0x0000000000000000)
def test_hash64_oneshot_consistent(
    message: bytes,
    seed: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    assert 0 <= spookyhash.hash64(data_type(message), seed=seed) < 2**64


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@pytest.mark.parametrize(
    "message, seed1, seed2, expected1, expected2",
    [
        pytest.param(
            b"hi",
            0x0000000000000000,
            0x0000000000000000,
            0xCD5A772A9AA6D50F,
            0x1D63A8DCB6D1ED50,
            id="hi",
        ),
        pytest.param(
            b"helloworld",
            0x0000000000000000,
            0x0000000000000000,
            0x4F6BDD7D478A7DF4,
            0x0D8396833F493BBF,
            id="helloworld",
        ),
    ],
)
def test_hash128_oneshot(
    message: bytes,
    seed1: int,
    seed2: int,
    expected1: int,
    expected2: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    expected_tuple = (expected1, expected2)
    assert spookyhash.hash128_pair(data_type(message), seed1=seed1, seed2=seed2) == expected_tuple
    expected_int = expected2 << 64 | expected1
    assert spookyhash.hash128(data_type(message), seed1=seed1, seed2=seed2) == expected_int


@pytest.mark.parametrize("data_type", [bytes, memoryview])
@given(
    message=binary(min_size=0, max_size=5000),
    seed1=integers(min_value=0, max_value=2**64 - 1),
    seed2=integers(min_value=0, max_value=2**64 - 1),
)
@example(message=b"hi", seed1=0x0000000000000000, seed2=0x0000000000000000)
@example(message=b"helloworld", seed1=0x0000000000000000, seed2=0x0000000000000000)
def test_hash128_oneshot_consistent(
    message: bytes,
    seed1: int,
    seed2: int,
    data_type: type[bytes | memoryview[bytes]],
) -> None:
    hash1, hash2 = spookyhash.hash128_pair(data_type(message), seed1=seed1, seed2=seed2)
    hash_full = spookyhash.hash128(data_type(message), seed1=seed1, seed2=seed2)

    assert hash_full == hash2 << 64 | hash1
    assert 0 <= hash1 < 2**64
    assert 0 <= hash2 < 2**64
    assert 0 <= hash_full < 2**128


@pytest.mark.parametrize(
    "cls, seed, expected_digest",
    [
        pytest.param(spookyhash.Hash32, 0, "1909f56b", id="Hash32-0"),
        pytest.param(spookyhash.Hash32, 42, "e122bece", id="Hash32-42"),
        pytest.param(spookyhash.Hash64, 0, "1909f56bfc062723", id="Hash64-0"),
        pytest.param(spookyhash.Hash64, 42, "e122bece593170b6", id="Hash64-42"),
        pytest.param(spookyhash.Hash128, 0, "1909f56bfc062723c751e8b465ee728b", id="Hash128-0"),
        pytest.param(spookyhash.Hash128, 42, "e122bece593170b66895f137637f3ba5", id="Hash128-42"),
    ],
)
def test_none_init_and_upate(
    cls: type[spookyhash.Hash],
    seed: int,
    expected_digest: str,
) -> None:
    builder: spookyhash.Hash
    if cls is spookyhash.Hash128:
        builder = cls(None, seed1=seed, seed2=seed)
    elif cls is spookyhash.Hash32:
        builder = cls(None, seed=seed)
    else:
        assert cls is spookyhash.Hash64
        builder = cls(None, seed=seed)

    assert builder.update(None).hexdigest() == expected_digest


@pytest.mark.parametrize(
    "dtype",
    [
        "int8",
        "int16",
        "int32",
        "int64",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "float32",
        "float64",
    ],
)
def test_memoryview_np_hashes_underlying_buffer(dtype: str) -> None:
    np = pytest.importorskip("numpy")
    array = np.arange(100, dtype=dtype)
    expected = spookyhash.hash64(array.tobytes())

    assert spookyhash.hash64(array) == expected
    assert spookyhash.Hash64(array).final() == expected
    assert spookyhash.Hash64().update(array).final() == expected


def test_memoryview_np_multidimensional_buffer() -> None:
    np = pytest.importorskip("numpy")
    array = np.arange(100, dtype=np.int32).reshape(10, 10)
    expected = spookyhash.hash64(array.tobytes())

    assert spookyhash.hash64(array) == expected
    assert spookyhash.Hash64().update(array).final() == expected


@pytest.mark.parametrize(
    "hash_type, expected",
    [
        pytest.param(spookyhash.Hash32, 4, id="Hash32"),
        pytest.param(spookyhash.Hash64, 8, id="Hash64"),
        pytest.param(spookyhash.Hash128, 16, id="Hash128"),
    ],
)
def test_digest_size(hash_type: type[spookyhash.Hash], expected: int) -> None:
    assert hash_type.digest_size == expected
    assert hash_type().digest_size == expected

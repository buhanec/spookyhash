"""Test README examples work as expected."""

import pytest

import spookyhash


def test_oneshot_hashes():
    assert spookyhash.hash32(b'hello world') == 2617184861
    assert spookyhash.hash32(b'hello world', seed=0x12345678) == 3380090220

    assert spookyhash.hash64(b'hello world') == 14865987102431973981
    assert spookyhash.hash64(b'hello world', seed=123) == 5719863273689036421

    assert spookyhash.hash128(b'hello world') == 185933735475381961281710998418114941533
    assert spookyhash.hash128(b'hello world', seed1=123_000, seed2=456_000) == 144121310386202441278894605216246194925

    assert spookyhash.hash128_pair(b'hello world') == (14865987102431973981, 10079487997037711397)
    assert spookyhash.hash128_pair(b'hello world', seed1=123_000, seed2=456_000) == (12678109464562819821, 7812831891108919044)


def test_incremental_hashes():
    sh = spookyhash.Hash32()
    sh.update(b'hello')
    sh.update(b' ')
    sh.update(b'world')
    assert sh.final() == 2617184861
    assert sh.hexdigest() == '5d12ff9b'

    assert spookyhash.Hash64(b'hello ', seed=123).update(b'world').final() == 5719863273689036421

    assert spookyhash.Hash64(b'hello ', seed=123).update(b'world').hexdigest() == '85b609a05709614f'

    sh = spookyhash.Hash128(seed1=123_000, seed2=456_000)
    sh.update(b'hello world')
    assert sh.final() == 144121310386202441278894605216246194925
    assert sh.final_pair() == (12678109464562819821, 7812831891108919044)
    assert sh.hexdigest() == 'ede2c8f262b1f1af04f763f735c16c6c'


def test_memoryview_support_np():
    try:
        import numpy as np
    except ImportError:
        pytest.skip('numpy not available')
    assert spookyhash.Hash64(np.arange(100)).hexdigest() == '43ab5363ad362c74'


def test_memoryview_support():
    assert spookyhash.Hash64(memoryview(b'hello world')).hexdigest() == '5d12ff9b81984ece'

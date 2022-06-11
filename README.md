# spookyhash [<img src="https://img.shields.io/gitlab/pipeline/alen/spookyhash/main?gitlab_url=https%3A%2F%2Fgitlab.home.alen.sh%2F&label=Gitlab%20CI&style=flat-square" align="right">](https://gitlab.home.alen.sh/alen/spookyhash) [<img src="https://img.shields.io/travis/buhanec/spookyhash/main.svg?label=Travis+CI&style=flat-square" align="right">](https://travis-ci.org/buhanec/spookyhash) [<img src="https://img.shields.io/azure-devops/build/buhanec/aa771e37-5a75-4d92-8d99-d27975af994e/2/main?label=Azure%20DevOps&style=flat-square" align="right">](https://dev.azure.com/buhanec/spookyhash/_build)

A Python wrapper of Bob Jenkins' [SpookyHash version 2](http://burtleburtle.net/bob/hash/spooky.html). Offers 32- 64- and 128-bit oneshot and incremental hashes.   

# License

> Licensed under the MIT license. See the LICENSE file in the repository root for more details.

# Usage

## Installation

Available through [spookyhash - PyPI](https://pypi.org/project/spookyhash/) using `pip install spookyhash`.

## Oneshot Hashes

```python
>>> import spookyhash

>>> spookyhash.hash32(b'hello world')
2617184861
>>> spookyhash.hash32(b'hello world', seed=0x12345678)
3380090220

>>> spookyhash.hash64(b'hello world')
14865987102431973981
>>> spookyhash.hash64(b'hello world', seed=123)
5719863273689036421

>>> spookyhash.hash128(b'hello world')
185933735475381961281710998418114941533
>>> spookyhash.hash128(b'hello world', seed1=123_000, seed2=456_000)
144121310386202441278894605216246194925

>>> # For a more comparable result to other libraries
>>> spookyhash.hash128_pair(b'hello world')
(14865987102431973981, 10079487997037711397)
>>> spookyhash.hash128_pair(b'hello world', seed1=123_000, seed2=456_000)
(12678109464562819821, 7812831891108919044)
```

## Incremental Hashes

```python
>>> import spookyhash

>>> sh = spookyhash.Hash32()
>>> sh.update(b'hello')
>>> sh.update(b' ')
>>> sh.update(b'world')
>>> sh.final()
2617184861
>>> sh.hexdigest()
'5d12ff9b'

>>> spookyhash.Hash64(b'hello ', seed=123).update(b'world').final()
5719863273689036421

>>> spookyhash.Hash64(b'hello ', seed=123).update(b'world').hexdigest()
'85b609a05709614f'

>>> sh = spookyhash.Hash128(seed1=123_000, seed2=456_000)
>>> sh.update(b'hello world')
>>> sh.final()
144121310386202441278894605216246194925
>>> sh.final_pair()
(12678109464562819821, 7812831891108919044)
>>> sh.hexdigest()
'ede2c8f262b1f1af04f763f735c16c6c'
```

## `memoryview` Support

Includes `memoryview` compatible types, such as NumPy arrays.

```python
>>> import spookyhash
>>> import numpy as np

>>> spookyhash.Hash64(np.arange(100)).hexdigest()
'43ab5363ad362c74'

>>> spookyhash.Hash64(b'hello world').hexdigest()
'5d12ff9b81984ece'
```

# Platform Independence

If run on a big-endian system, the code would produce different hashes, but of equal quality.

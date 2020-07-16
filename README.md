# spookyhash

A Python wrapper of Bob Jenkins' [SpookyHash version 2](http://burtleburtle.net/bob/hash/spooky.html). Offers 32- 64- and 128-bit oneshot and incremental hashes.   

# License

> Licensed under the MIT license. See the LICENSE file in the repository root for more details.

# Usage

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

>>> spookyhash.Hash64(b'hello ', seed=123).update(b'world').final()
5719863273689036421

>>> sh = spookyhash.Hash128(seed1=123_000, seed2=456_000)
>>> sh.update(b'hello world')
>>> sh.final()
144121310386202441278894605216246194925
>>> sh.final_pair()
(12678109464562819821, 7812831891108919044)
```

# Platform Independence

If run on a big-endian system, the code would produce different hashes, but of equal quality.

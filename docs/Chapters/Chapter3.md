# Dictionaries and Sets
hashable immutable types (str, bytes, numeric). 

```py
tt = (1, 2,(30, 40))
print(hash(tt))
tl = (1, 2, [30, 40])

```
```py
a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two' : 2, 'three' : 3}
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
e = dict({'three': 3, 'one': 1, 'two': 2})
a == b == c == d == e

```
## dict comprehensions
- each element is a tuple of the form (code, country)

expretion explanation:
{key_expr: value_expr for item in iterable}

```py
DIAL_CODES = [
  (86, 'China'),
  (91, 'India'),
  (1, 'United States'),
  (62, 'Indonesia'),
  (55, 'Brazil'),
  (92, 'Pakistan'),
  (880, 'Bangladesh'),
  (234, 'Nigeria'),
  (7, 'Russia'),
  (81, 'Japan'),

country_code = {county: code for code, country in DIAL_CODES}
print(country_code)
country_code = {code : country.upper() for country, code in country_code.items(), if code < 66}
print(country_code_if)

```

## Handling Missing Keys with setdefault

```py
for line_no, (code, country) in enumerate(DIAL_CODES, 1): 
    print(f"line{line_no}: {country} (Code: {code})")
# enumerate this being used for printing a list with numbers that starts with 1.

```

```py
import collections
index = collection.defaultdict(list)
index['a'].append(1)
index['a'].append(2)
index['b'].append(3)
print(index)


```

```py
Tests for item retrieval using `d[key]` notation
::

d = StrKeyDict0(['2', 'two'], ('4', 'four'))
print(d['2'])


```

```py
Tests for item using `d.get(key)` notation::
print(d.get('2'))
Tests for the `in` operator::
print(2 in d)

```

## Variations of dict

1. collections.OrderedDict:
maintains key in insertion order, allowing iteration

```py
from collections import OrderedDict
od = OrderedDict
od['a'] = 1
od['b'] = 2
od['c'] = 3
print(od)

od.move_to_end('a')
print(od)

```

2. collections.ChainMap:
holds a list of mappings that can be search as one. The lookus is preformed on each mapping in order, and succeeds if the key is found in any of them.

```py
from collections import Chainmap
default_config = {'theme': 'dark', 'lang': 'en'}
user_config = {'lang': 'fr'}
cli_config = {'theme': 'light'}

combined = Chainmap(cli_config, user_config, default_config)
print(combined['theme'])
print(combined['lang'])
print(combined.maps[2]['theme']) # this will access the default config, as it's thierd in the order dict.


```

3. collections.Counter:
a mapping that holds an integer count of each key. Updating an existing key adds to its count. this can be used to count instances of hashable objects.

```py
from collections import Counter
words = ['apple', 'banana', 'apple', 'orange', 'banana', 'apple']
counter = Counter(words)
print(counter)
print(counter['apple'])

```

4. collections.UserDict
A wrapper around a regular dict is meant to be subclassed to create custum behavior.


```py
from collections import UserDict

class UppercaseKeyDict(UserDict)
  def __setitem__(self, key, value):
    key = str(key).upper()
    super().__setitem__(key, value)
d = UppercaseKeyDict()
d['hello'] = 'world'
print(d)
print(d['HELLO'])


```

## Immutable Mappings

1. MappingProxyType
it returs mappingproxy instance that is a read only but dynamic view of the original mapping. Updates can be seen in the mappingproxy but changes cannot be made throught it.

```py
from types import MappingProxyType
d = {1: 'A'}
d_proxy = MappingProxyType(d)
print(d_proxy)
print(d_proxy[1])
d_proxy[2] = 'x' # this will not work we can't change throught proxy
d[2] = 'B'
print(d_proxy)

```

## Set Theory
A set is a collection of unique objects. A basic use case is removing duplication:

```py
l = ['spam', 'spam', 'eggs', 'spam']
set(l)

```

```py
found = 0
for n in needles:
  if n in haystack:
    found += 1

```

## Count occurences 

```py
found = len(set(needles) & set(haystack))

```
## frozenset in py
it create a immutable set 

```py
print(frozenset(range(10)))
frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9})



```

```py
from unicodedata import name
{chr(i) for i in range(32, 256) if 'SING' in name(chr(i), '')}

```
## Hash in py

A number "int" that represent an object for a quick comaprison and lookup. It used for comparison in dict and set to find element fast (O(1)).

How It Works
- Compute `hash(search_key)` to get a bucket index.
- Check bucket:
  - Empty → Raise `KeyError`.
  - Has `found_key:found_value` → If `search_key == found_key`, return `found_value`; else, handle collision.
- Resolve collisions using different hash bits (`perturb` function) to find another bucket.
- Insert/update: Place new pair in empty bucket or overwrite matching key’s value.
- Resize table when crowded, rehashing items to keep collisions low.
- **Efficiency**: Average 1–2 collisions, making operations fast.

### O(1) Time Complexity
- **Why O(1)**: Hashing, bucket access, and average probe count (1–2) are constant time, independent of table size (\(n\)).
- **Math**: Time \( T = c_1 + c_2 \cdot E[\text{probes}] \), where all terms are constant.
- **Resizing**: Rare, amortized O(1) per insertion.
- **Worst Case**: O(\(n\)) if many collisions (rare).

### Key Points
- **Strengths**: Fast O(1) operations, supports hashable keys.
- **Limitations**: Needs immutable keys, memory overhead, rare O(\(n\)) worst case.
- Python’s hash tables are optimized for speed and reliability.
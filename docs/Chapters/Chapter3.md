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

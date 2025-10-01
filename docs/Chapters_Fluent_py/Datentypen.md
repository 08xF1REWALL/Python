
# 🧠 Python Datentypen – Übersicht & Vergleich

## 🔹 Standard-Datentypen

| Typ           | Veränderbar | Geordnet | Duplikate erlaubt | Inhaltstyp         | Beispiel               | Beschreibung                        |
|---------------|-------------|----------|--------------------|--------------------|-------------------------|-------------------------------------|
| `list`        | ✅ Ja        | ✅ Ja     | ✅ Ja               | beliebig           | `[1, 2, "a"]`            | Veränderbare Liste                  |
| `tuple`       | ❌ Nein      | ✅ Ja     | ✅ Ja               | beliebig           | `(1, 2)`                | Unveränderbare Liste                |
| `set`         | ✅ Ja        | ❌ Nein   | ❌ Nein             | beliebig           | `{1, 2}`                | Einfache Mengen, keine Duplikate    |
| `frozenset`   | ❌ Nein      | ❌ Nein   | ❌ Nein             | beliebig           | `frozenset([1, 2])`     | Unveränderbare Menge                |
| `dict`        | ✅ Ja        | ✅ Ja     | ❌ Nein (Keys)      | Schlüssel:Wert     | `{"a": 1}`              | Key-Value-Speicherung               |
| `defaultdict` | ✅ Ja        | ✅ Ja     | ❌ Nein             | Schlüssel:Wert     | `defaultdict(int)`      | dict mit Defaultwerten              |
| `OrderedDict` | ✅ Ja        | ✅ Ja     | ❌ Nein             | Schlüssel:Wert     | `OrderedDict()`         | dict mit garantierter Reihenfolge   |
| `bytes`       | ❌ Nein      | ✅ Ja     | ✅ Ja               | Bytes (0–255)      | `b"abc"`                | Unveränderbare Bytefolge            |
| `bytearray`   | ✅ Ja        | ✅ Ja     | ✅ Ja               | Bytes (0–255)      | `bytearray(b"abc")`     | Veränderbare Bytefolge              |
| `memoryview`  | ✅ Ja        | ✅ Ja     | ✅ Ja               | Binärdaten         | `memoryview(b"abc")`    | Speicheransicht auf Bytes           |
| `range`       | ❌ Nein      | ✅ Ja     | ✅ Ja               | Ganzzahlen         | `range(10)`             | Zahlenfolge                         |
| `array.array` | ✅ Ja        | ✅ Ja     | ✅ Ja               | numerisch (ein Typ)| `array('i', [1, 2])`    | Effiziente Zahlenspeicherung        |
| `deque`       | ✅ Ja        | ✅ Ja     | ✅ Ja               | beliebig           | `deque([1, 2])`         | Doppelt verkettete Liste            |
| `namedtuple`  | ❌ Nein      | ✅ Ja     | ✅ Ja               | benannte Felder    | `Point(x=1, y=2)`       | Tupel mit Attributnamen             |
| `Counter`     | ✅ Ja        | ❌ Nein   | ❌ Nein             | Elemente:Anzahl    | `Counter("aab")`        | Häufigkeitszähler                   |
| `ChainMap`    | ✅ Ja        | ✅ Ja     | ❌ Nein             | mehrere Mappings   | `ChainMap(d1, d2)`      | Kettenartige dict-Zusammenfassung   |
| `str`         | ❌ Nein      | ✅ Ja     | ✅ Ja               | Zeichen (Unicode)  | `"Hallo"`               | Zeichenkette                        |
| `int` / `float` | ❌ Nein    | —        | —                  | Zahlen             | `42` / `3.14`           | Ganze und Fließkommazahlen          |
| `complex`     | ❌ Nein      | —        | —                  | Komplexe Zahl      | `1 + 2j`                | Mathematik, komplexe Zahlen         |
| `bool`        | ❌ Nein      | —        | —                  | Wahrheitswert      | `True` / `False`        | Wahr oder falsch                    |
| `NoneType`    | ❌ Nein      | —        | —                  | —                  | `None`                  | Repräsentiert „nichts“              |

---

## 🔍 Typ-Erkennung in Python

| Methode               | Beispiel                          | Bedeutung                              |
|------------------------|------------------------------------|-----------------------------------------|
| `type(x)`             | `type([1,2]) → <class 'list'>`    | Zeigt exakten Typ                       |
| `isinstance(x, list)` | `isinstance(x, (list, tuple))`    | Prüft ob `x` Instanz eines Typs         |
| `collections.abc`     | `isinstance(x, Sequence)`         | Prüft auf Sequenzverhalten              |

---

## 🧩 Gruppierung nach Eigenschaften

### ✅ Veränderbare Typen (mutable)
- `list`, `set`, `dict`, `defaultdict`, `OrderedDict`, `bytearray`, `array.array`, `deque`, `Counter`, `ChainMap`

### ❌ Unveränderbare Typen (immutable)
- `tuple`, `frozenset`, `bytes`, `str`, `range`, `namedtuple`, `int`, `float`, `complex`, `bool`, `NoneType`

### ⚙️ Spezial-Typen für besondere Einsatzzwecke
- `memoryview` – Direktzugriff auf Speicher
- `array.array` – Typ-spezifische, speichereffiziente Arrays
- `deque` – Schnellere Listen für Queues/Stacks
- `namedtuple` – Tupel mit Namen für besseren Zugriff
- `Counter` – Zählt Vorkommen wie Multiset
- `ChainMap` – Kombiniert mehrere dicts

---

> 💡 **Tipp:** Nutze `collections` für spezialisierte Aufgaben, `array`/`numpy` für effiziente Zahlenoperationen, und `deque` für schnelle Datenstrukturoperationen (Stacks, Queues).

---

## 🧰 Listenmethoden in Python

| Methode              | Beschreibung                                                                 |
|----------------------|------------------------------------------------------------------------------|
| `append(x)`          | Fügt **ein Element** am Ende der Liste an                                    |
| `extend(iterable)`   | Fügt **mehrere Elemente** (z. B. Liste oder Tuple) ans Ende an               |
| `insert(index, x)`   | Fügt ein Element an einer bestimmten Stelle ein                              |
| `pop([index])`       | Entfernt ein Element (Standard: letztes) und gibt es zurück                  |
| `remove(x)`          | Entfernt das **erste Vorkommen** von `x`                                     |
| `clear()`            | Leert die gesamte Liste                                                      |
| `index(x)`           | Gibt den Index des **ersten Vorkommens** von `x` zurück                      |
| `count(x)`           | Zählt, wie oft `x` in der Liste vorkommt                                     |
| `sort()`             | Sortiert die Liste **in-place** (dauerhaft verändernd)                       |
| `reverse()`          | Kehrt die Reihenfolge der Elemente **in-place** um                           |
| `copy()`             | Gibt eine **flache Kopie** der Liste zurück                                  |

> 💡 Verwende `append()` für ein einzelnes Element und `extend()` für mehrere.  
> Beispiel:  
> - `liste.append([1, 2])` → `[[1, 2]]`  
> - `liste.extend([1, 2])` → `[1, 2]`

---

## 🔄 Typumwandlung

1. `int(x)` – Wandelt x in eine ganze Zahl um (z. B. `"42"` → `42`)
2. `float(x)` – Wandelt in eine Gleitkommazahl um (`"3.14"` → `3.14`)
3. `complex(x)` – Wandelt in eine komplexe Zahl um (`"3+4j"` → `(3+4j)`)

### 🔤 Zeichen und ASCII

1. `chr(x)` – Zahl → Zeichen (`65` → `'A'`)
2. `ord(x)` – Zeichen → Zahl (`'A'` → `65`)

### 🪄 Allgemeine Umwandlung

- `str(x)` – Beliebiger Wert zu String (`123` → `"123"`)
- `bool(x)` – Wert zu Boolean (`""` → `False`, `"Hallo"` → `True`)
- `bytes(x, encoding)` – Wandelt z. B. einen String in ein Byte-Objekt
- `list(x)`, `tuple(x)`, `set(x)` – Wandelt in eine Liste, ein Tupel oder eine Menge


### Mengen

#### Zuweisungsoperatoren 
📘 Kombinierte Zuweisungsoperatoren in Python

1. +=    Addition und Zuweisung
   x += y    →   x = x + y

2. -=    Subtraktion und Zuweisung
   x -= y    →   x = x - y

3. *=    Multiplikation und Zuweisung
   x *= y    →   x = x * y

4. /=    Division und Zuweisung
   x /= y    →   x = x / y

5. //=   Ganzzahl-Division und Zuweisung
   x //= y   →   x = x // y

6. %=    Modulo (Rest) und Zuweisung
   x %= y    →   x = x % y

7. **=   Potenzieren und Zuweisung
   x **= y   →   x = x ** y

8. &=    Bitweises UND und Zuweisung
   x &= y    →   x = x & y

9. |=    Bitweises ODER und Zuweisung
   x |= y    →   x = x | y

10. ^=   Bitweises XOR und Zuweisung
    x ^= y   →   x = x ^ y

11. <<=  Bitverschiebung nach links und Zuweisung
    x <<= y  →   x = x << y

12. >>=  Bitverschiebung nach rechts und Zuweisung
    x >>= y  →   x = x >> y



#### Operator
1. len(s)
2. x in s 
3. x not in s : 
4. s <= t wenn es bei der Menge s um eine teilmenge der menge t handet
5. s >= t wenn es bei der Menge s um eine teilmenge der menge t handet
6. s < t wenn es bei der Menge s um eine echte teilmenge der menge t handet
7. s > t wenn es bei der Menge s um eine echte teilmenge der menge t handet
8. s | t erzeugt eine menge die alle Elemente von s und t enthält
9. s & t erzeugt eine menge die die objekte enthält due sowohl element der s als auch der menge t sind
10. s - t erzeugt neue menge mit allen elementen von s außer debeb die auch in t enthalten sind
11. s ^ t erzeugt eine neue menge mit die alle objekte enthältm die entweder in s oder in t vorkommen 
12. s |= t
13. s &= t
14. s -= t
15. s ^= t

## Methoden 
1. s.issubset(t) s <= t
2. s.issuperset(t) s >= t
3. s.isdijoint(t) ob da eine leere schnitt menge gibt
4. s.union(t) s | t
5. s.intersection(t) s & t
6. s.difference(t) s - t
7. s.symmetric_difference(t) s ^ t
8. s.copy eruzeugt eine kopie von s.

## Veränderliche Mengen set
1. s.add(e)
2. s.clear() löscht alle Elementen der menge 
3. s.difference_update(t) s -= t
4. s.discard(e) löscht das element e aus der menge s. sollte e nicht vorhanden sein, wird ignoriert
5. s.intersection_update(t) s &= t
6. s.remove(e) löscht das element e aus der menge s 
7. s.symmetric_difference_update(t) s ^= t
8. s.update s |= t




## ⏰ Datum & Zeit in Python (`datetime`)

### 📦 Import

```python
from datetime import datetime, date, time, timedelta
```

### 🕱 Grundbausteine

| Konstruktor            | Beschreibung              | Beispiel                         |
| ---------------------- | ------------------------- | -------------------------------- |
| `datetime.now()`       | Aktuelles Datum & Uhrzeit | `2025-06-22 14:45:00.123456`     |
| `datetime.today()`     | Dasselbe wie `now()`      |                                  |
| `datetime.utcnow()`    | UTC-Zeit (nicht lokal)    |                                  |
| `datetime(...)`        | Manuell erstellen         | `datetime(2025, 1, 1, 12, 0, 0)` |
| `date.today()`         | Nur aktuelles Datum       | `2025-06-22`                     |
| `time(hour, min, sec)` | Nur Uhrzeit               | `time(14, 30, 0)`                |


* `fromtimestamp(timestamp)`
* `combine(date, time)`
* `strptime(date_string, format)`
* `datetime.timedelta`

### ⏱ Zeitspannen mit `timedelta`


## Regeln
*args: beliebige positionale Argumente
**kwargs: beliebige benannte/keyword Argumente


Tombola tests
=============

All concrete subclasses of ``Tombola`` must behave consistently.

Creating a ConcreteTombola
--------------------------

>>> balls = list(range(5))
>>> tb = ConcreteTombola(balls)
>>> sorted(tb.inspect())
[0, 1, 2, 3, 4]
    
Picking items
-------------

``pick()`` must return one of the items and remove it from the tombola.

>>> picked = tb.pick()
>>> picked in balls
True
>>> picked in tb.inspect()
False

After removing all remaining items, ``pick()`` should raise LookupError.

>>> for _ in range(4):
...     _ = tb.pick()
>>> tb.loaded()
False
>>> tb.inspect()
()
>>> tb.pick()
Traceback (most recent call last):
...
LookupError: pick from empty ...

Loading items
-------------

``load()`` should add items to the tombola.

>>> tb.load([10, 20, 30])
>>> sorted(tb.inspect())
[10, 20, 30]
>>> tb.loaded()
True

``inspect()`` should always return a sorted tuple without altering the contents.

>>> snapshot1 = tb.inspect()
>>> snapshot2 = tb.inspect()
>>> snapshot1 == snapshot2
True

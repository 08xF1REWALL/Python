# Sequence Hacking, Hashing and Slicing
## How Slicing works

```py
class Myseq:
    def __getitem__(self, index):
        return index

s = Myseq()
print(s[1])
print(s[1:4])
print(s[1:4:2, 9])


```
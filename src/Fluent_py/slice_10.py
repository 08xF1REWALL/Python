class Myseq:
    def __getitem__(self, index):
        return index

s = Myseq()
print(s[1])
print(s[1:4])
print(s[1:4:2, 9])
print(slice)
print(dir(slice))

slice(None, 10, 2).indices(5)
slice(-3, None, None).indices(5)


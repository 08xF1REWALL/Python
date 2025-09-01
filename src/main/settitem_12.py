class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)
dd = DoppelDict(one=1)
print(dd)


#Tests for item retrieval using `d[key]` notation ::

# Define StrKeyDict0 class
class StrKeyDict0(dict):
	def __missing__(self, key):
		print("selff:", self)
		print("keyy:", key)
		if isinstance(key, str):
			raise KeyError(key)
		return self[str(key)]

	def get(self, key, default=None):
		try:
			return self[key]
		except KeyError:
			return default

	def __contains__(self, key):
		return key in self.keys() or str(key) in self.keys()

# Initialize StrKeyDict0
d = StrKeyDict0([('2', 'two'), ('4', 'four')])
print(d['2'])  # Output: two
print(d[4])    # Output: four
print(d.get(4))  # Output: four
print(d.get(1, 'Not Found'))  # Output: Not Found
print(2 in d)

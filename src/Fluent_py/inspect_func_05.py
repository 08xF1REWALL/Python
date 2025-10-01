from inspect import signature

def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

sig = signature(greet)
print(sig)

for name, param in sig.parameters.items():
    print(param.kind, ':', name, '=', param.default)
    
# positionally pass like func("Alice")
# or by keyword (like func(name= "Alice"))

class MacroCommand:
	"""A command that executes a list of commands"""
	def __init__(self, commands):
		self.commands = list(commands)

	def __call__(self):
		for command in self.commands:
			command()

# Einfache Befehle (Funktionen)
def say_hello():
    print("Hallo!")

def say_goodbye():
    print("Auf Wiedersehen!")

def ask_question():
    print("Wie geht's?")

# Makrobefehl erstellen
macro = MacroCommand([say_hello, ask_question, say_goodbye])

# Makrobefehl ausführen
macro()

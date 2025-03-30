import collections  # Import collections module to create named tuples

# Create a named tuple to represent a card
Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    # Create a list of ranks and suits for the deck of cards
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    # Suits are spades, diamonds, clubs, and hearts
    suits = 'spades diamonds clubs hearts'.split()
    
    def __init__(self):
        # Create a list of cards using a list comprehension
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    
    def __len__(self):
        # Return the number of cards in the deck
        return len(self._cards)
    
    def __getitem__(self, position):
        # Allow indexing to access a card at a specific position
        return self._cards[position]

if __name__ == '__main__':
    # Create an instance of the FrenchDeck class
    deck = FrenchDeck()
    
    # Print the number of cards in the deck
    print(len(deck))
    
    # Print the first card in the deck
    print(deck[0])
    
    # Print the last card in the deck
    print(deck[-1])
    
    # Print a slice of the first 5 cards in the deck
    print(deck[:5])
    
    # Print a slice of the last 5 cards in the deck
    print(deck[-5:])	
import collections# Import collections module to create named tuples
from random import choice 
from random import shuffle # Import choice function from random module
# Create a named tuple to represent a card
Card = collections.namedtuple('Card', ['rank', 'suit'])
suit_values = {'spades': 3, 'hearts': 2, 'diamonds': 1, 'clubs': 0}# Define suit values for comparison

def spades_high(card):
   rank_value = FrenchDeck.ranks.index(card.rank)# Get the index of the card's rank
   return rank_value * len(suit_values) + suit_values[card.suit]# Calculate the value of the card based on rank and suit
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
    
    def set_card(deck, position, card):
        deck._cards[position] = card
        FrenchDeck.__setitem__ = set_card

if __name__ == '__main__':
    # Create an instance of the FrenchDeck class
    deck = FrenchDeck()
    
    print(choice(deck))# Print a random card from the deck
    # Print the number of cards in the deck
    print(len(deck))
    
    print(Card('K', 'hearts') in deck)# Print a specific card (Queen of hearts)
    
    print(Card('7', 'beasts') in deck)# Print a specific card (Queen of hearts)
    
    # Print the first card in the deck
    print(deck[0])
    
    # Print the last card in the deck
    print(deck[-1])
    
    # Print a slice of the first 5 cards in the deck
    print(deck[:5])
    
    # Print a slice of the last 5 cards in the deck
    print(deck[-5:])	
    for card in sorted(deck, key=spades_high):
        print(card)# Sort the deck of cards using the spades_high function and print each card
        
    l1 = list(range(10))
    shuffle(l1)
    print(l1)
    
    """deck1 = FrenchDeck()
    shuffle(deck1)
    print(deck1)
    """
    shuffle(deck)
    print(deck[:5])
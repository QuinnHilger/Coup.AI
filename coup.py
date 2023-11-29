import random
#File to make the coup game
#Player class
#Game class
class Player:
    def __init__(self, card1, card2, name):
        self.card1 = card1
        self.card2 = card2
        self.coins = 2
        self.name = name
    
    def display_info(self):
        print(f"Player's cards: {self.card1}, {self.card2}")
        print(f"Number of coins: {self.coins}")

class Game:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []  # Assuming you have a Player class (as defined in the previous answer)
        self.deck = []
        self.create_deck()
        self.turn = random.randint(0, num_players - 1)

    def create_deck(self):
        # Each type of card is repeated 3 times
        card_types = ['Captain', 'Duke', 'Assassin', 'Contessa', 'Inquisitor']
        deck = card_types * 3
        self.deck = deck

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def initial_deal(self):
        if len(self.deck) >= self.num_players * 2:
            for i in range(self.num_players):
                player_name = input(f"What is player {i+1}'s name? ")
                card1, card2 = self.deck[:2]
                new_player = Player(card1, card2, player_name)
                self.players.append(new_player)
                self.deck = self.deck[2:]
        else:
            print("Not enough cards in the deck to deal to all players.")
    
    def play_game(self):
        print("Let the game begin!\n")
        quit_game = False
        while True:
            current_player = self.players[self.turn]
            print()
            print(f"Player {self.players[self.turn].name}'s turn:")
            current_player.display_info()
            # Add your game logic here, e.g., asking for player input
            while True:
                correct_move = True
                move = input("What is your move? ").lower()
                if move == 'skip':
                    print("skipping move")
                elif move == 'quit game':
                    print("Thanks for playing")
                    quit_game = True
                elif move == 'income':
                    print("income")
                elif move == 'foreign aid':
                    print("foreign aid")
                elif move == 'tax':
                    print("tax")
                elif move == 'steal':
                    print("steal")
                elif move == 'assassinate':
                    print("assassinate")
                elif move == 'exchange':
                    print("exchange")
                elif move == 'inspect':
                    print("inspect")
                else:
                    print("invalid move, try again? ")
                    correct_move = False
                if correct_move:
                    break
            # Switch to the next player's turn
            self.turn = (self.turn + 1) % self.num_players
            if quit_game == True:
                break

def main():
    # Prompting the user
    print("Welcome to the game of Coup!")
    num_players = int(input("How many players will be playing? "))

    # Creating a Game object
    game = Game(num_players)

    # Shuffling the deck
    game.shuffle_deck()

    # Dealing cards to players
    game.initial_deal()

    # Asking if the user is ready to start playing
    ready_to_play = input("Are you ready to start playing? (yes/no) ").lower()

    if ready_to_play != '':
        # Playing the game
        playing_again = True
        while(playing_again):
            game.play_game()
            play_again = input("Do you want to play again? (yes/no) ").lower()
            if play_again != 'yes':
                playing_again = False

    else:
        print("Okay, maybe next time. Have a great day!")
    

if __name__ == "__main__":
    main()
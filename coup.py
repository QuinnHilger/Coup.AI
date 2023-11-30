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
        self.alive = True
    
    def display_info(self):
        print("Player's cards:")
        cards_string = ""
        if self.card1 != None and self.card2 != None:
            cards_string = self.card1 + ", " + self.card2
        elif self.card1 == None and self.card2 != None:
            cards_string = self.card2
        elif self.card1 != None and self.card2 == None:
            cards_string = self.card1
        print(cards_string)
        print(f"Number of coins: {self.coins}")

class Game:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []  # Assuming you have a Player class (as defined in the previous answer)
        self.deck = []
        self.create_deck()
        self.turn = random.randint(0, num_players - 1)
        self.players_dictionary = {}
        self.num_dead = 0

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
                self.players_dictionary[player_name] = new_player
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
                if current_player.coins > 9:
                    move = "coup"
                else:
                    move = input("What is your move? ").lower()
                if move == 'skip':
                    print("skipping move")
                elif move == 'quit game':
                    print("Thanks for playing")
                    quit_game = True
                elif move == 'income':
                    print(f"{current_player.name}'s taking income")
                    current_player.coins = current_player.coins + 1
                elif move == 'foreign aid':
                    #Blockable
                    print("foreign aid")
                    print(f"{current_player.name}'s collecting foreign aid")
                    #Block here
                    current_player.coins = current_player.coins + 2
                elif move == 'tax':
                    print("tax")
                    #Challengeable
                    print(f"{current_player.name}'s collecting foreign aid")
                    #Challenge Here
                    current_player.coins = current_player.coins + 3
                elif move == 'steal':
                    #Blockable and challengeable
                    print("steal")
                    invalid_response = True
                    while invalid_response:
                        print("Who would you like to steal from : ")
                        for name in self.players:
                            if name.name != current_player.name:
                                print(name.name)
                        steal_victum = input()
                        if steal_victum in self.players_dictionary and steal_victum != current_player.name:
                            if self.players_dictionary[steal_victum].coins == 0:
                                print("This player has no coins")
                                break
                            invalid_response = False
                    steal_victum_player = self.players_dictionary[steal_victum]
                    print(f"{current_player.name}'s is stealing from {steal_victum}")
                    #Block Here
                    #Challenge Here
                    if steal_victum_player.coins > 1:
                        print("Stole 2 coins")
                        steal_victum_player.coins = steal_victum_player.coins - 2
                        current_player.coins = current_player.coins + 2
                    elif steal_victum_player.coins == 1:
                        print("Stole 1 coin")
                        steal_victum_player.coins = steal_victum_player.coins - 1
                        current_player.coins = current_player.coins + 1
                elif move == 'assassinate':
                    print("assassinate")
                    if current_player.coins >= 3:
                        current_player.coins = current_player.coins - 3
                    else:
                        print("You do not have enough coins to assassin")
                        break
                        #Re loop the actions available
                    #Blockable and Challengeable
                    invalid_response = True
                    while invalid_response:
                        print("Who would you like to assassinate: ")
                        for name in self.players:
                            if name.name != current_player.name:
                                print(name.name)
                        assassin_victum = input()

                        if assassin_victum in self.players_dictionary and assassin_victum != current_player.name:
                
                            assassin_victum_player = self.players_dictionary[assassin_victum]
                            if assassin_victum_player.alive == True:
                                invalid_response = False
                            else:
                                print(f"{assassin_victum} is already dead")
                    #Challenge Here
                    response = input(f"{assassin_victum}, do you claim Contessa? (yes/no) ").lower()
                    if response == 'yes':
                        #challenge here
                        print(f"{assassin_victum} blocked the assassination attempt")
                    else:
                        if assassin_victum_player.card1 != None and assassin_victum_player.card2 != None:
                            #kill off a card
                            invalid_response = True
                            while invalid_response:
                                print(f"{assassin_victum}, which card do you want to kill off?")
                                killed_card = input(f"{assassin_victum_player.card1} or {assassin_victum_player.card2} ")
                                if killed_card != assassin_victum_player.card1 and killed_card != assassin_victum_player.card2:
                                    invalid_response = True
                                    print("Invalid player to kill")
                                else:
                                    invalid_response = False
                            if killed_card == assassin_victum_player.card1:
                                #Display this card as dead
                                assassin_victum_player.card1 = None
                            else:
                                assassin_victum_player.card2 = None
                        else:
                            #print which card is dead
                            print(f"{assassin_victum} is dead and out of the game")
                            assassin_victum_player.alive = False
                            self.num_dead = self.num_dead + 1
                            if self.num_dead == len(self.players) - 1:
                                print("Game Over")
                                print(f"{current_player.name} has won the game")
                                quit_game = True
                elif move == 'coup':
                    print("coup")
                    if current_player.coins >= 7:
                        current_player.coins = current_player.coins - 7
                    else:
                        print("You do not have enough coins to coup")
                        break
                        #Re loop the actions available
                    invalid_response = True
                    while invalid_response:
                        print("Who would you like to coup: ")
                        for name in self.players:
                            if name.name != current_player.name:
                                print(name.name)
                        assassin_victum = input()
                        if assassin_victum in self.players_dictionary and assassin_victum != current_player.name:
                            assassin_victum_player = self.players_dictionary[assassin_victum]
                            if assassin_victum_player.alive == True:
                                invalid_response = False
                            else:
                                print(f"{assassin_victum} is already dead")
                    assassin_victum_player = self.players_dictionary[assassin_victum]
                    if assassin_victum_player.card1 != None and assassin_victum_player.card2 != None:
                        #kill off a card
                        invalid_response = True
                        while invalid_response:
                            print(f"{assassin_victum}, which card do you want to kill off?")
                            killed_card = input(f"{assassin_victum_player.card1} or {assassin_victum_player.card2} ")
                            if killed_card != assassin_victum_player.card1 and killed_card != assassin_victum_player.card2:
                                invalid_response = True
                                print("Invalid player to kill")
                            else:
                                invalid_response = False
                        if killed_card == assassin_victum_player.card1:
                            #Display this card as dead
                            assassin_victum_player.card1 = None
                        else:
                            assassin_victum_player.card2 = None
                    else:
                        #print which card is dead
                        print(f"{assassin_victum} is dead and out of the game")
                        assassin_victum_player.alive = False
                        self.num_dead = self.num_dead + 1
                        if self.num_dead == len(self.players) - 1:
                            print("Game Over")
                            print(f"{current_player.name} has won the game")
                            quit_game = True
                elif move == 'exchange':
                    print("exchange")
                    #Challengeable
                    print(f"{current_player.name} wants to exchange with the deck")
                    print("The card that you selected off of the top is: ")
                    top_card = self.deck.pop(0)
                    print(top_card)
                    if current_player.card1 != None and current_player.card2 != None:
                        invalid_response = True
                        while(invalid_response):
                            print("Which card do you want to discard?")
                            discarded_card = input(f"{current_player.card1} or {current_player.card2} or {top_card} ")
                            if discarded_card == current_player.card1 or discarded_card == current_player.card2 or discarded_card == top_card:
                                invalid_response = False
                            else:
                                print("Invalid card selection, try again")
                        if discarded_card == top_card:
                            self.deck.append(top_card)
                        elif discarded_card == current_player.card1:
                            self.deck.append(current_player.card1)
                            current_player.card1 = top_card
                        else:
                            self.deck.append(current_player.card2)
                            current_player.card2 = top_card
                    elif current_player.card1 != None:
                        invalid_response = True
                        while(invalid_response):
                            print("Which card do you want to discard?")
                            discarded_card = input(f"{current_player.card1} or {top_card} ")
                            if discarded_card == current_player.card1 or discarded_card == top_card:
                                invalid_response = False
                            else:
                                print("Invalid card selection, try again")
                        if discarded_card == top_card:
                            self.deck.append(top_card)
                        elif discarded_card == current_player.card1:
                            self.deck.append(current_player.card1)
                            current_player.card1 == top_card
                    else:
                        invalid_response = True
                        while(invalid_response):
                            print("Which card do you want to discard?")
                            discarded_card = input(f"{current_player.card2} or {top_card} ")
                            if discarded_card == current_player.card2 or discarded_card == top_card:
                                invalid_response = False
                            else:
                                print("Invalid card selection, try again")
                        if discarded_card == top_card:
                            self.deck.append(top_card)
                        elif discarded_card == current_player.card2:
                            self.deck.append(current_player.card2)
                            current_player.card2 == top_card
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
#TO DO
#Inspect
#Block Steal
#Block Foreign Aid
#Challenge
#Display all cards on the table
def main():
    # Prompting the user
    print("Welcome to the game of Coup!")
    num_players = int(input("How many players will be playing? "))
    if num_players < 1:
        exit("invalid number of players")

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
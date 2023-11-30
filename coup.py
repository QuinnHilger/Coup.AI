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
    
    def lose_influence(self, player):
        if player.card1 != None and player.card2 != None:
            invalid_response = True
            while invalid_response:
                print(f"{player.name}, which card do you want to kill off?")
                killed_card = input(f"{player.card1} or {player.card2} ")
                if killed_card != player.card1 and killed_card != player.card2:
                    invalid_response = True
                    print("Invalid player to kill")
                else:
                    invalid_response = False
            if killed_card == player.card1:
                #Display this card as dead
                player.card1 = None
            else:
                player.card2 = None
        else:
            print(f"{player.name} is dead and out of the game")
            player.alive = False
            self.num_dead = self.num_dead + 1
            
    
    def challenge(self, current_player, claimed_character):
        response = input(f"Does anyone challenge {current_player.name} from claiming {claimed_character}? (yes/no) ")
        if response == 'yes':
            invalid_response = True
            while(invalid_response):
                print(f"Who is challenging {current_player.name}?")
                for name in self.players:
                    if name.name != current_player.name and self.players_dictionary[name].alive:
                        print(name.name)
                challenger = input()
                if challenger in self.players_dictionary and challenger != current_player.name:
                    challenger_player = self.players_dictionary[challenger]
                    if challenger_player.alive:
                        invalid_response = False
                    else:
                        print(f"{challenger} is dead")
                else:
                    print(f"{challenger} is not a valid player")
            #Challenge block here
            if claimed_character == 'steal block':
                if current_player.card1 == 'Captain':
                    print(f"{current_player.name} has Captain!")
                    self.deck.append('Captain')
                    current_player.card1 = self.deck.pop(0)
                    self.lose_influence(challenger_player)
                    return False
                elif current_player.card1 == 'Inquisitor':
                    print(f"{current_player.name} has Inquisitor!")
                    self.deck.append('Inquisitor')
                    current_player.card1 = self.deck.pop(0)
                    self.lose_influence(challenger_player)
                    return False
                elif current_player.card2 == 'Captain':
                    print(f"{current_player.name} has Captain!")
                    self.deck.append('Captain')
                    current_player.card2 = self.deck.pop(0)
                    self.lose_influence(challenger_player)
                    return False
                elif current_player.card2 == 'Inquisitor':
                    print(f"{current_player.name} has Inquisitor!")
                    self.deck.append('Inquisitor')
                    current_player.card2 = self.deck.pop(0)
                    self.lose_influence(challenger_player)
                    return False
                else:
                    print(f"{current_player.name} could not block the steal")
                    self.lose_influence(current_player)
                    return True
            elif current_player.card1 == claimed_character:
                print(f"{current_player.name} has {claimed_character}.")
                self.deck.append(claimed_character)
                current_player.card1 = self.deck.pop(0)
                self.lose_influence(challenger_player)
                return False
            elif current_player.card2 == claimed_character:
                print(f"{current_player.name} has {claimed_character}.")
                self.deck.append(claimed_character)
                current_player.card2 = self.deck.pop(0)
                self.lose_influence(challenger_player)
                return False
            else:
                print(f"{current_player.name} did not have {claimed_character}")
                self.lose_influence(current_player)
                return True
        else:
            return False
    
    def play_game(self):
        print("Let the game begin!\n")
        quit_game = False
        while True:
            current_player = self.players[self.turn]
            print()
            if not current_player.alive:
                continue
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
                    print("foreign aid")
                    print(f"{current_player.name} is attempting to collect foreign aid")
                    response = input("Does anybody want to block the foreign aid? (yes/no) ").lower()
                    if response == 'yes':
                        invalid_response = True
                        while(invalid_response):
                            print("Who is claiming to block the foreign aid? ")
                            for name in self.players:
                                if name.name != current_player.name:
                                    print(name.name)
                            blocker = input()
                            if blocker in self.players_dictionary and blocker != current_player.name:
                                blocker_player = self.players_dictionary[blocker]
                                if blocker_player.alive:
                                    invalid_response = False
                                else:
                                    print(f"{blocker} is dead")
                            else:
                                print(f"{blocker} is not a valid player")
                        if (self.challenge(blocker_player, "Duke")):
                            print(f"{current_player.name}'s collecting foreign aid")
                            current_player.coins = current_player.coins + 2
                        else:
                            print(f"{current_player.name} is blocked from collecting foreign aid.")
                    else:
                        print(f"{current_player.name}'s collecting foreign aid")
                        current_player.coins = current_player.coins + 2
                elif move == 'tax':
                    print("tax")
                    #Challengeable
                    print(f"{current_player.name}'s tax")
                    #Challenge Here
                    if (self.challenge(current_player, "Duke")):
                        print(f"{current_player.name} failed to collect tax")
                    else:
                        current_player.coins = current_player.coins + 3
                elif move == 'steal':
                    #Blockable and challengeable
                    print("steal")
                    invalid_response = True
                    while invalid_response:
                        print("Who would you like to steal from : ")
                        for name in self.players:
                            if name.name != current_player.name and name.alive:
                                print(name.name)
                        steal_victum = input()
                        if steal_victum in self.players_dictionary and steal_victum != current_player.name:
                            if self.players_dictionary[steal_victum].coins == 0:
                                print("This player has no coins")
                                correct_move = False
                                continue
                            invalid_response = False
                    steal_victum_player = self.players_dictionary[steal_victum]
                    print(f"{current_player.name}'s is stealing from {steal_victum}")
                    #Block Here
                    if(self.challenge(current_player, "Captain")):
                        print(f"{current_player.name} failed to steal")
                    else:
                        response = input(f"{steal_victum}, do you want to block? (yes/no) ")
                        test = True
                        if response == "yes":
                            #Challenge block
                            print(f"{steal_victum} is claiming to block the steal.")
                            test = self.challenge(steal_victum_player, "steal block")
                        if test:
                            if steal_victum_player.coins > 1:
                                print("Stole 2 coins")
                                steal_victum_player.coins = steal_victum_player.coins - 2
                                current_player.coins = current_player.coins + 2
                            elif steal_victum_player.coins == 1:
                                print("Stole 1 coin")
                                steal_victum_player.coins = steal_victum_player.coins - 1
                                current_player.coins = current_player.coins + 1
                        else:
                            print(f"{current_player.name} got blocked from stealing")
                elif move == 'assassinate':
                    print("assassinate")
                    if current_player.coins >= 3:
                        current_player.coins = current_player.coins - 3
                    else:
                        print("You do not have enough coins to assassin")
                        correct_move = False
                        continue
                        #Re loop the actions available
                    #Blockable and Challengeable
                    invalid_response = True
                    while invalid_response:
                        print("Who would you like to assassinate: ")
                        for name in self.players:
                            if name.name != current_player.name and name.alive:
                                print(name.name)
                        assassin_victum = input()

                        if assassin_victum in self.players_dictionary and assassin_victum != current_player.name:
                
                            assassin_victum_player = self.players_dictionary[assassin_victum]
                            if assassin_victum_player.alive == True:
                                invalid_response = False
                            else:
                                print(f"{assassin_victum} is already dead")
                    #Challenge Here
                    if (self.challenge(current_player, "Assassin")):
                        print(f"{current_player.name} failed to assassin.")
                    else:
                        response = input(f"{assassin_victum}, do you claim Contessa? (yes/no) ").lower()
                        test = True
                        if response == 'yes':
                            #challenge here
                            test = self.challenge(assassin_victum_player, "Contessa")
                        if test:
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
                        else:
                            print(f"{assassin_victum} blocked the assassination attempt")
                elif move == 'coup':
                    print("coup")
                    if current_player.coins >= 7:
                        current_player.coins = current_player.coins - 7
                    else:
                        print("You do not have enough coins to coup")
                        correct_move = False
                        continue
                        #Re loop the actions available
                    invalid_response = True
                    while invalid_response:
                        print("Who would you like to coup: ")
                        for name in self.players:
                            if name.name != current_player.name and name.alive:
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
                    if (self.challenge(current_player, "Inquisitor")):
                        print(f"{current_player.name} failed to exchange")
                    else:
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
                    invalid_response = True
                    while invalid_response:
                        print("Who would you like to inspect: ")
                        for name in self.players:
                            if name.name != current_player.name and name.alive:
                                print(name.name)
                        inspection_victum = input()
                        if inspection_victum in self.players_dictionary and inspection_victum != current_player.name:
                            inspection_victum_player = self.players_dictionary[inspection_victum]
                            if inspection_victum_player.alive == True:
                                invalid_response = False
                            else:
                                print(f"{inspection_victum} is dead")
                    inspection_victum_player = self.players_dictionary[inspection_victum]
                    if (self.challenge(current_player, "Inquisitor")):
                        print(f"{current_player.name} failed to inspect")
                    else:
                        if inspection_victum_player.card1 != None and inspection_victum_player.card2 != None:
                            invalid_response = True
                            chosen_card = None
                            while(invalid_response):
                                print("What card would you like to show? ")
                                print(f"{inspection_victum_player.card1} or {inspection_victum_player.card2}")
                                chosen_card = input()
                                if chosen_card == inspection_victum_player.card1 or chosen_card == inspection_victum_player.card2:
                                    invalid_response = False
                                else:
                                    print("Invalid input")
                        print(f"{inspection_victum} showed you {chosen_card}. Do you want them to keep it or exchange? (keep/exchange) ")
                        response = input()
                        if response == 'exchange':
                            print(f"{inspection_victum} is exchanging card for a new one")
                            self.deck.append(chosen_card)
                            if inspection_victum_player.card1 == chosen_card:
                                inspection_victum_player.card1 = self.deck.pop(0)
                            else:
                                inspection_victum_player.card2 = self.deck.pop(0)
                else:
                    print("invalid move, try again? ")
                    correct_move = False
                if correct_move:
                    break
            # Switch to the next player's turn
            if self.num_dead == len(self.players) - 1:
                print("Game Over")
                for player in self.players:
                    if player.alive:
                        print(f"{player} has won the game!")
                        break
                quit_game = True
            self.turn = (self.turn + 1) % self.num_players
            if quit_game == True:
                break
#TO DO
#Display all cards on the table
#Bugs:
#If BS calls on inspect and last card, inspect will still ask to see last card
#If BS on steal, it will still ask if someone wants to block after
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
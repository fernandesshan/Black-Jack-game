import random
import math

# tuples are used so that the values can't be changes
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True  # This controls if player is playing. It will be false is player is busted or player choose to stand


'''
----------- Card Class -----------
Contains properties of a single card
Used to 
- create a card instance having suit, rank and value (__init__)
- print the card's rank and suit (__str__)
'''


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[self.rank]

    def __str__(self):
        return f'{self.rank} of {self.suit}'


'''
----------- Deck Class -----------
Used to 
- create Deck of 52 cards (__init__)
- Shuffle the Deck of cards (shuffle)
- Deal 1 cards (deal)
- print number of cards in the Deck (__str__)

'''


class Deck:
    def __init__(self):
        # we don't take deck as parameter because we want it to be constant
        self.deck = []  # start with an empty deck list
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)  # create an instance of Card class
                self.deck.append(created_card)  # add the instance of Card to the deck of cards

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        # deals the last\top card in the deck
        return self.deck.pop()

    def __str__(self):
        # print total number of cards in deck
        return f' Cards in deck {len(self.deck)}'


'''
----------- Hand Class -----------
Used to 
- Initialize the cards in hand, values of cards in hand and Aces in hand (__init__)
- Add the card objects in hand & calculate the values of the card(add_card)
- Adjust Aces & Calculate the total values of the card (adjust_for_ace)
- Print the number of cards in hand (__str__)
'''


class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        # ace_count = 0
        # add card (popped from the deck) to hand
        self.cards.append(card)
        # if card is not Ace the add the value directly else add 11 and then adjust aces if any
        if card.rank != 'Ace':
            self.value += card.value
        else:
            self.value += card.value  # default Ace value of 11 will be added
            # ace_count += 1
            self.aces += 1
        # adjust the value of ace after adding the card values
        '''
        not adjusted in else loop because if 2 aces, 
        1st instance value was 11, 2nd instance value will be 1. 
        If 3rd card is Queen, 1st Ace can be adjusted only if we adjust Aces in the end and not in else loop
        '''

    def adjust_for_ace(self):
        while self.aces:
            # if busted then change Ace's value from 11 to 1
            if self.value > 21:
                self.value -= 10
                self.aces -= 1
            else:
                # this will break from the while loop when ace_count > 0 and value < 21
                break

    def __str__(self):
        # returns the number of cards in hand
        return f'has {len(self.cards)} cards'


'''
----------- Chips Class -----------
Used for 
- keeping track of total number of chips remaining, amount of bet played (__init__)
- print the current amount of chips remaining
'''


class Chips:
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0

    def __str__(self):
        return f"Chip balance: {self.total}\n"


'''
Used to (take_bet)
- check if the bet amount is a valid number
- check if player has sufficient funds to place bets
'''


def take_bet(players_chips):
    # Check if it has sufficient chips
    while True:
        check_bet = 0
        # check if the amount bet is a valid integer
        while not check_bet:
            try:
                # try to convert input to an integer
                check_bet = math.floor(float(input("\nEnter the amount you want to bet: \n")))
                print(f"You are want to bet {check_bet} chips")
            except:
                print("Incorrect amount. Please enter a valid integer")

        # Check if it has sufficient chips
        if check_bet <= players_chips.total:
            print("Your bet is places")
            # set the players bet amount
            players_chips.bet = check_bet
            break  # since bet is valid, break from while True
        else:
            check_bet = 0  # reset check_bet to again check for valid integer when playing again
            print(f"You have insufficient chips. Please lower your bet. Chips remaining: {players_chips.total}")


'''
Used to (hit_or_stand)
- Asks the user if they want to hit or stand
- If hit, the execute the hit method
- If stand, stop playing
'''


def hit_or_stand(deck, hand):
    hit = 0  # used to check if user used a valid input -> then later to decide if hit or stand
    global playing  # to control an upcoming while loop
    while hit not in ['h', 'H', 's', 'S']:
        hit = input("\nDo you want to hit(h) or stand(s): ")

        if hit in ['h', 'H']:
            # hit the deck
            hand.add_card(deck.deal())

            print("Player chose to Hit!\n")

        elif hit in ['s', 'S']:
            # player stands and now dealer will hit
            playing = False  # to control an upcoming while loop
            print("Player chose to Stand! Dealer's turn.\n")

        else:
            print("Invalid input. Select 'h' to hit or 's' to stand")


'''
(show some) used to
- shows all cards of player and only 1 card of dealer
'''


def show_some(player, dealer):
    print("\nPlayers cards are: ")
    for _ in range(len(player.cards)):
        print(player.cards[_])
    print("\nDealers cards are :")
    print("dealer's first card hidden")
    print(dealer.cards[1])  # 2nd card of dealer is shown


'''
(show all) used to
- shows all cards of player and dealer
'''


def show_all(player, dealer):
    print("\nPlayers cards are: ")
    for _ in range(len(player.cards)):
        print(player.cards[_])
    print("\nDealers cards are: ")
    for _ in range(len(dealer.cards)):
        print(dealer.cards[_])


# check_busted returns true if player's or dealer's (which is passes as an argument) card value is greater than 21

def check_busted(hand):
    return hand.value > 21


'''
(player_or_dealer_wins) used to
- add player win chips if dealer busted
- subtract player lose chips if player busted
- add player win chips if player is closer to 21 than dealer
- subtract player lose chips if dealer is closer to 21 than player
- else print it is a tie
'''


def player_or_dealer_wins(player, dealer, players_chips):
    global playing
    if check_busted(dealer):
        print(f"\nDealer BUSTED and his value is {dealer.value}, Player wins and his value is {player.value}")
        players_chips.total += players_chips.bet

    elif check_busted(player):
        print(f"\nPlayer BUSTED and his value is {player.value},Dealer wins and his value is {dealer.value}")
        players_chips.total -= players_chips.bet

    elif abs(player.value - 21) < abs(dealer.value - 21):
        print(f"\nPlayer wins and his value is {player.value}, Dealer loses and his value is {dealer.value}")
        players_chips.total += players_chips.bet

    elif abs(player.value - 21) > abs(dealer.value - 21):
        print(f"\nDealer wins and his value is {dealer.value}, Player loses and his value is {player.value}")
        players_chips.total -= players_chips.bet

    else:
        print(f"\nIt's a tie ! Dealer's value is {dealer.value} and player's value is {player.value}")


if __name__ == '__main__':
    # Print an opening statement
    print("---------- Welcome to black Jack ----------\n")
    # Set up the Player's chips
    player_chips = Chips()

    play_again = 1
    while play_again:  # 0 if player doesn't want to play again

        # Create & shuffle a new deck
        new_deck = Deck()
        new_deck.shuffle()

        # creating player and computer hand
        player_hand = Hand()
        computer_hand = Hand()
        # Deal two cards to each player
        for _ in range(2):
            player_hand.add_card(new_deck.deal())
            computer_hand.add_card(new_deck.deal())
        print('Player', player_hand)
        print('Computer', computer_hand)

        # Prompt the Player for their bet
        take_bet(player_chips)

        # # Show cards (but keep one dealer card hidden)
        # show_some(player_hand, computer_hand)

        while playing:  # recall this variable from our hit_or_stand function, False if player wants to stand

            # Show cards (but keep one dealer card hidden)
            show_some(player_hand, computer_hand)

            # Prompt for Player to Hit or Stand
            hit_or_stand(new_deck, player_hand)
            # Adjust for aces in player's hand if value is greater than 21
            player_hand.adjust_for_ace()
            # If player's hand exceeds 21, break out of playing loop
            if check_busted(player_hand):
                print(f"Player busted. Your total is {player_hand.value}")
                playing = False

        # If Player hasn't busted, play Dealer's hand until Dealer reaches soft 17
        if not check_busted(player_hand):
            print("Dealer is hitting . . . ")
            while computer_hand.value < 17:
                computer_hand.add_card(new_deck.deal())

                if check_busted(computer_hand):
                    print(f"Dealer busted. ")

        # Show all cards
        show_all(player_hand, computer_hand)

        # Run different winning scenarios
        player_or_dealer_wins(player_hand, computer_hand, player_chips)

        # Inform Player of their chips total
        print(player_chips)

        # Ask if player want to play again if player has sufficient chips
        if player_chips.total > 0:
            # while loop is used to check to get a valid yes, no value
            while True:
                again = input("Do you want to play again ? ")
                if again.lower() == 'y':
                    # reset variables to play again
                    playing = True
                    player_chips.bet = 0
                    bet = 0
                    break
                elif again.lower() == 'n':
                    play_again = 0
                    print("---------- Thanks for playing black Jack ! ----------\n")
                    break
                else:
                    print("Please choose 'y' or 'n'")

        else:
            print("You have insufficient chips to play again")
            play_again = 0
            print("---------- Thanks for playing black Jack ! ----------\n")

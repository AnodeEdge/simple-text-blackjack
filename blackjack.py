import random as rand


class Card:
    def __init__(self, rank, suit, value):
        self.suit = suit
        self.rank = rank
        self.value = value


class Deck:
    def __init__(self, sets=1):
        self.cards = []
        self.sets = sets

    def create_deck(self):
        # Creates a number of sets of 52 standard playing cards
        self.cards = []
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        cards = [('Two', 2), ('Three', 3), ('Four', 4), ('Five', 5), ('Six', 6), ('Seven', 7),
                 ('Eight', 8), ("Nine", 9), ("Ten", 10), ("Jack", 10), ('Queen', 10), ('King', 10), ('Ace', 11)]
        for _ in range(0, self.sets):
            for suit in suits:
                for rank, value in cards:
                    self.cards.append(Card(rank=rank, suit=suit, value=value))

    def show_deck(self):
        # Show cards in deck
        for card in self.cards:
            print(f"{card.rank} of {card.suit}")

    def shuffle(self):
        # Iterate over the deck starting at the end and swap card with a random card within the deck
        for position in reversed(range(0, len(self.cards))):
            random_position = rand.randrange(0, position + 1)
            self.cards[position], self.cards[random_position] = self.cards[random_position], self.cards[position]

    def deal_card(self):
        return self.cards.pop(0)


class Player:
    def __init__(self, dealer=False):
        self.hand = []
        self.dealer = dealer

    def show_hand(self, turn):
        if self.dealer == True:
            print("The Dealer has:")
        else:
            print("The Player has:")
        for count, card in enumerate(self.hand):
            if count == 0 and self.dealer == True and turn == 0:
                print("A face down card")
            else:
                print(f"{card.rank} of {card.suit}")
        if self.dealer == False:
            print(f'The count is {self.get_value()}')
        print("")

    def draw_card(self, card):
        self.hand.append(card)

    def get_value(self):
        total_value = 0
        for card in self.hand:
            total_value += card.value
        if total_value > 21:
            for card in self.hand:
                if card.rank == 'Ace':
                    total_value -= 10
                    break
        return total_value

    def is_bust(self):
        if self.get_value() > 21:
            is_bust = True
        else:
            is_bust = False
        return is_bust

    def is_blackjack(self):
        if len(self.hand) == 2 and self.get_value() == 21:
            return True
        else:
            return False


class Blackjack:
    # Handles game objects and functions
    def __init__(self):
        self.deck = Deck()
        self.dealer = Player(dealer=True)
        self.player = Player()
        self.turn = 0
        self.deck.create_deck()
        self.deck.shuffle()

    def draw(self, player):
        player.draw_card(self.deck.deal_card())

    def reshuffle(self):
        if (self.deck.sets * len(self.deck.cards)) < (self.deck.sets * 52 * 0.5):
            self.deck.create_deck()
            self.deck.shuffle()
            print("\n---*-Deck has been reshuffled-*---\n")

    def initialize_game(self):
        self.reshuffle()
        self.player.hand.clear()
        self.dealer.hand.clear()

        for _ in range(0, 2):
            self.draw(self.player)
            self.draw(self.dealer)

    def show_dealer_hand(self):
        print("The Dealer has: ")
        for count, card in enumerate(self.dealer.hand):
            if count == 0 and self.turn == 0:
                print("A face down card")
            else:
                print(f"{card.rank} of {card.suit}")
        if self.turn == 1:
            print(f"\nDealer has {self.dealer.get_value()} points")
        self.print_divider()

    def show_player_hand(self):
        print("The Player has: ")
        for count, card in enumerate(self.player.hand):
            print(f"{card.rank} of {card.suit}")
        print(f"\nPlayer has {self.player.get_value()} points")
        self.print_divider()

    def player_move(self):
        while True:
            player_decision = input("Hit or Stay: ")
            if player_decision.lower() == "hit":
                self.draw(self.player)
                return "hit"
            elif player_decision.lower() == "stay":
                return "stay"
            print("Try again")

    def dealer_move(self):
        if self.dealer.get_value() <= 16:
            self.draw(self.dealer)
            return "hit"
        return "stay"

    def check_for_blackjack(self):
        # Player and/or Dealer have Blackjack
        if self.player.is_blackjack() and self.dealer.is_blackjack():
            print("It's a Draw.")
            return True
        elif self.player.is_blackjack():
            print("Player wins with Blackjack")
            return True
        elif self.dealer.is_blackjack():
            print("Dealer wins with Blackjack")
            return True
        return False

    def check_for_bust(self):
        if self.player.is_bust():
            print("Player Busts, Dealer Wins")
            return True
        elif self.dealer.is_bust() and self.player.is_bust():
            print("Player and Dealer Bust, Dealer Wins")
            return True
        elif self.dealer.is_bust():
            print("Dealer Busts, Player Wins")
            return True
        return False

    def get_winner(self):
        # Compare points
        if self.player.get_value() == self.dealer.get_value():
            print("Its a Draw")
        elif self.player.get_value() > self.dealer.get_value():
            print(f"The Player wins with a score of {self.player.get_value()}")
        else:
            print(f"The Dealer wins with a score of {self.dealer.get_value()}")

    def print_divider(self):
        print("----------------------")

    def play_again(self):
        while True:
            play_again = input("Do you want to play again? (Y/N): ")
            if play_again.lower() == "y":
                return True
            elif play_again.lower() == "n":
                return False
            print("Try Again")

    def game_loop(self):
        while True:
            self.initialize_game()
            self.print_divider()
            self.show_dealer_hand()
            self.show_player_hand()
            self.turn += 1
            if self.check_for_blackjack() is False:
                player_move = "hit"
                dealer_move = "hit"
                while (player_move is "hit") or (dealer_move is "hit"):
                    if player_move is "hit":
                        player_move = self.player_move()
                        self.print_divider()
                    if dealer_move is "hit":
                        dealer_move = self.dealer_move()
                    self.show_dealer_hand()
                    self.show_player_hand()
                    if self.check_for_blackjack() is True or self.check_for_bust() is True:
                        break
                    if player_move is not "hit" and dealer_move is not "hit":
                        self.get_winner()
                        break

            self.turn = 0
            if not self.play_again():
                break


# --------------------------------------------------
print('\n ---Welcome to Blackjack!--- \n')
blackjack = Blackjack()
blackjack.game_loop()

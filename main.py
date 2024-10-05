import random

BLACK_JACK = 21
player_balance = 500
MINI_BET = 1


def generate_deck():
    suits = [u"\u2666", u"\u2665", u"\u2663", u"\u2660"]
    cards = [str(i) for i in range(2, 10)] + ["J", "K", "Q", "T", "A"]
    return [card + suit for suit in suits for card in cards]

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck
    

def deal_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

def handle_bet(balance):
    while True:
        try:
            bet = int(input(f"Place your bet (min {MINI_BET}): "))
            if bet < MINI_BET:
                print(f"The minimum bet is ${MINI_BET}.")
            elif bet > balance:
                print(f"Insufficient funds. Your balance is {balance}.")
            else:
                return bet
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def sum_of_cards(player_cards):
    total = 0
    ace = 0
    for card in player_cards:
        if card[0].isdigit():
            total += int(card[0])
        elif card[0] in ["J", "K", "Q", "T"]:
            total += 10
        else:
            total += 11
            ace += 1
    
    while total > BLACK_JACK and ace:
        total -= 10
        ace -= 1

    return total

def dealer_turn(dealer_cards, deck):

    dealer_total = sum_of_cards(dealer_cards)
    while dealer_total < 17:
        card = deal_card(deck)
        dealer_cards.append(card)
        dealer_total = sum_of_cards(dealer_cards)
        print(f"The dealer hits and was dealt {card}")
    print(f"The dealer's final hand: {(', ').join(dealer_cards)} with a total of {dealer_total}.")
    return dealer_total


def handle_black_jack(player_total, dealer_total, bet, balance):

    if player_total == BLACK_JACK and dealer_total != BLACK_JACK:
        print("BLACKJACK!")
        print(f"You have won {bet}")
        return balance + bet * 1.5
    elif dealer_total == BLACK_JACK:
        print(f"The dealer has blackjack. You lose!")
        return balance - bet
    else:
        return None
        

def handle_first_deal(deck):
    player_cards = [deal_card(deck), deal_card(deck)]
    dealer_cards = [deal_card(deck), deal_card(deck)]
    print(f'You are dealt {(",").join(player_cards)}')
    print(f"The dealer shows {dealer_cards[0]} and a hidden card")
    return player_cards, dealer_cards





def play_game(deck, bet, balance):
    "Game Loop Logic"
    player_cards, dealer_cards = handle_first_deal(deck)

    player_total = sum_of_cards(player_cards)
    dealer_total = sum_of_cards(dealer_cards)

    "Let's get Blackjack result"
    blackjack_result = handle_black_jack(player_total, dealer_total, bet, balance)

    if blackjack_result is not None:
        return blackjack_result


    while True:
        player_total = sum_of_cards(player_cards)
        if player_total > BLACK_JACK:
            print(f"You bust with {player_total}. You lose {bet}.")
            return balance - bet
        
        action = input("Would you like to hit or stay: ").lower()
        if action == "hit":
            card = deal_card(deck)
            player_cards.append(card)
            print(f'You are dealt {card} and your hand is {(", ").join(player_cards)}')
        elif action == "stay":
            break
        else:
            print("Invalid action. Please enter 'stay' or 'hit'.")
    
    # Handle_dealer_turn
    dealer_total = dealer_turn(dealer_cards, deck)

    if dealer_total > player_total:
        print(f"The dealer wins")
        return balance - bet
    elif dealer_total > BLACK_JACK or dealer_total < player_total:
        print(f"You won {bet}")
        return balance + bet
    else:
        print(f"It's a tie. Your bet is returned")
        return balance
    
            





def start_game():
    global player_balance
    while player_balance > 0:
        print("\n********---------**********")
        print("\nWelcome to Blackjack!")
        print(f"\nYour balance: ${player_balance}")
        play = input("\nWould you like to play a hand? (Y/N): ").lower()
        if play == 'y':
            deck = shuffle_deck(generate_deck())
            bet = handle_bet(player_balance)
            player_balance = play_game(deck, bet, player_balance)
        elif play == 'n':
            print("Thank you for playing!")
            break
        else:
            print("Invalid input. Please enter Y or N.")
    
    if player_balance <= 0:
        print("You've run out of money. Please restart to try again.")


start_game()
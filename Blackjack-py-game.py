import random
import re

suits = ["♡","♤","♧","♢"]
numbers = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
total = 0
wallet = 100

# Play game
def game():
    deck = []
    #Generate deck of 52 cards
    for suit in suits:
        for number in numbers:
            deck.append(number + suit)

    #Shuffle deck
    random.shuffle(deck)

    # Define player and dealer hands
    player_hand = []
    dealer_hand = []

    # Deal initial cards
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())
    player_hand.append(deck.pop())
    dealer_hand.append(deck.pop())

    # Define function to check if the string has numbers in it
    def has_numbers(card):
        return any(char.isdigit() for char in card)

    # Define function to calculate hand value
    def hand_value(hand):
        value = 0
        for card in hand:
            if has_numbers(card):
                value += int(re.findall(r'\d+', card)[0])
            elif any(number in card for number in ["J", "K", "Q"]):
                    value += 10
            elif "A" in card:
                if value > 10:
                    value += 1
                else:
                    value += 11
        return value

    # Define function to display cards
    def display_cards(hand, hide_last=False):
        if hide_last:
            print('Dealer cards: ' + dealer_hand[0] + ' [Hidden]')
        else:
            print('Dealer cards:', end=' ')
            for card in dealer_hand:
                print(card, end=' ')
        print('\nPlayer cards:', end=' ')
        for card in player_hand:
            print(card, end=' ')
        print('\n')


    global wallet
    flag = True

    print('Your current score: ' + str(wallet) + '\n')
    if wallet < 10:
        print("You are out of money, sorry! Restart the game")
        while True:
            restart = input("Restart the game? (y/n) ")
            if restart == "y":
                wallet = 100
                game()
            else:
                return

    while True:
        wage = input("Enter your wage (a number and at least 10): ")
        if wage.isdigit():
            wage = int(wage)
            if wage >=10 and wage <= wallet:                
                break
    print("Your wage is: " + str(wage))

    def display_results(condition):
        # Display resulting wage and the wallet after the round
        if condition == 'natural':
            print('You win ' + str(int(wage * 1.5)) + ' and you current wallet is ' + str(wallet))
            print('\n')
        elif condition == 'win':
            print('You win ' + str(wage) + ' and you current wallet is ' + str(wallet))
            print('\n')
        elif condition == 'lost':
            print('You lost ' + str(wage) + ' and you current wallet is ' + str(wallet))
            print('\n')

    while True:
        # Display cards
        display_cards(dealer_hand, hide_last=True)
        print('Player Score: ' + str(hand_value(player_hand)))
        print('\n')

        # Check for blackjack
        if hand_value(player_hand) == 21:
            if flag:
                print('Blackjack! Natural!')
                wallet += int(wage * 1.5)
                display_results('natural')
                break
            else:
                print('Blackjack! You win!')
                wallet += wage
                display_results('win')
                break
        flag = False
        
        # Ask player to hit or stand
        choice = input('Hit or stand? ')
        if choice.lower() == 'hit' or choice.lower() == 'h':
            player_hand.append(deck.pop())
            # Check for bust
            if hand_value(player_hand) > 21:
                display_cards(dealer_hand)
                print('Bust! You lose.')
                wallet -= wage
                display_results('lost')
                break
        elif choice.lower() == 'stand' or choice.lower() == 's':
            # Dealer's turn
            while hand_value(dealer_hand) < 17:
                dealer_hand.append(deck.pop())
            display_cards(dealer_hand)
            print('Player Score: ' + str(hand_value(player_hand)) + ' Dealer Score: ' + str(hand_value(dealer_hand)))
            # Check for bust
            if hand_value(dealer_hand) > 21:
                print('Dealer bust! You win!')                
                wallet += wage
                display_results('win')
                break
            # Compare hands
            if hand_value(player_hand) > hand_value(dealer_hand):
                print('You win!')
                wallet += wage
                display_results('win')
                break
            elif hand_value(player_hand) < hand_value(dealer_hand):
                print('You lose.')
                wallet -= wage
                display_results('lost')
                break
            else:
                print('Push.')
                break
        else:
            print('Invalid choice. Please enter "hit" or "stand".')

while True:
    play_game = input("Shall we play a game? (y/n) ")
    if play_game == 'y':
        game()
    elif play_game == 'n':
        print('Thank you for playing!')
        break
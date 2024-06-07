"""
Assignment #5: Blackjack

This program allows the user to play blackjack, with an implemented betting system!

To run this program, open a command prompt and run 'python3 assignment_5_Matt_Cunningham'
"""

import random
import time

def want_to_play(balance):
    """
    This function controls prompting the user for if they want to
    play a new game or quit the program. It uses the account balance
    as an argument to ensure the user has enough funds to play, and 
    returns their selection if no errors
    """
    if not balance == 0:
        while True:
            user_input = input("Enter 'S' to start a new game or 'Q' to quit the program: ")

            try:
                if not user_input:
                    raise ValueError("Error: You did not enter anything!\n")

                start_game_input = user_input.strip().upper()

                if start_game_input not in {"S", "Q"}:
                    raise ValueError(f"Error: '{user_input}' is not valid input!\n")
                else:
                    return start_game_input
            except ValueError as e:
                print(e)
    else:
        print("You have no funds remaining. Add more funds to continue playing.")
        print("Thank you!\n")
        quit()

def get_player_bet(balance):
    """
    This function gets the players input for their betting amount.
    It uses the account balance as a parameter to make sure their 
    input is between 1 and their balance. It then returns the bet value
    if no errors
    """
    while True:
        bet_input = input(f"Enter your bet in increments of 1 (between 1 and {balance}): $")

        try:
            if not bet_input:
                raise ValueError("Error: You did not enter anything!\n")

            if not bet_input.isdigit():
                raise ValueError(f"Error: {bet_input} is not a valid input!\n")
            else:
                bet = int(bet_input)

            if bet < 1.00:
                raise ValueError("Error: You must bet a minimum of 1.00!\n")
            elif bet > balance:
                raise ValueError(f"Error: You do not have {bet} funds available!\n")
            else:
                return bet
        except ValueError as e:
            print(e)

def hit_or_stand():
    """
    This function controls and returns the input for if the user
    will want to hit or stand.  
    """
    while True:
        user_input = input("Enter 'H' to hit or 'S' to stand: ")

        try:
            if not user_input:
                raise ValueError("Error: You did not enter anything!\n")

            move_input = user_input.strip().upper()

            if move_input not in {"H", "S"}:
                raise ValueError(f"Error: '{user_input}' is not valid input!\n")
            else:
                return move_input
        except ValueError as e:
            print(e)

def draw_cards(initial_draw=True):
    """
    This function is used to draw cards. It has a bool for
    the initial draw to draw the first 4 cards for each round,
    if the function is called with False, it will only return
    1 new card
    """
    if initial_draw:
        initial_cards = {
        "player_first": random.randint(1, 10), 
        "player_second": random.randint(1, 10), 
        "dealer_first": random.randint(1, 10), 
        "dealer_second": random.randint(1, 10)
        }
        return initial_cards
    else:
        new_card = random.randint(1, 10)
        return new_card

def players_turn(player_first, player_second, dealer_first, balance):
    """
    This function controls the players turn. It tells them their betting amount,
    the cards they drew, and the card the dealer drew as well as that the dealer 
    has a hidden card. It has logic to break the loop if the user busts or stands on
    21 and also calls the hit or stand function to get the users move. It adds the total
    card sum for each hit and returns it as well as the bet
    """
    total = player_first + player_second

    player_bet = get_player_bet(balance)
    print(balance)
    print(f"\nYou bet ${player_bet} with a 1:1 return ratio "
          f"(You will receive back ${player_bet * 2} if you win!)")
    print(f"You drew a {player_first} and a {player_second}, for a total of {total}")
    print(f"The dealer drew a {dealer_first} and a hidden card\n")

    while True:
        if total == 21:
            break
        elif total > 21:
            break
        else:
            print("Would you like to hit, or stand?")
            move = hit_or_stand()
            if move == "H":
                new_card = draw_cards(False)
                total += new_card
                print("\nYou hit")
                print(f"You draw a {new_card}. Your new total is {total}\n")
            else:
                break

    if total == 21 or move == "S":
        print(f"You stand with a total of {total}. It is now the dealers turn!")

    return total, player_bet


def dealers_turn(dealer_first, dealer_second):
    """
    This function acts similar to the player turn function,
    except no input is required. It draws cards as long as the total is 
    under 16, then stands if between 17 and 21, and busts if total is above
    21. It also uses a time.sleep to create an artificial effect as though
    we were waiting for a real life dealer to flip the cards. It returns the total
    for later use
    """
    total = dealer_first + dealer_second

    print(f"The dealer reveals their hidden card. "
          f"They have a {dealer_first} and a {dealer_second}, for a total of {total}\n")

    while True:
        if total <= 16:
            print("Waiting for the dealer to make their move...\n")
            time.sleep(3)
            new_card = draw_cards(False)
            total += new_card
            print("The dealer hits")
            print(f"The dealer draws a {new_card}. Their new total is {total}\n")

        elif 16 < total < 22:
            print(f"The dealer stands with a total of {total}\n")
            break
        elif total > 21:
            break

    return total

def end_game(outcome, round_info):
    """
    This function controls the messages for the end game based on
    the different win/loss scenarios. It also adds or removes from the users
    balance based on if they won or loss 
    """
    player_total = round_info["player_total"]
    player_bet = round_info["player_bet"]
    balance = round_info["balance"]
    dealer_total = round_info["dealer_total"]


    outcomes = {
        "player_bust": f"You bust with a {player_total}. The dealer wins!\n",
        "dealer_bust": (f"The dealer busts with a {dealer_total}. "
                        f"You win! ${player_bet} has been added to your account!\n"),
        "player_over_dealer": (f"Your {player_total} beats the dealer's {dealer_total}. "
                                f"You win! ${player_bet} has been added to your account!\n"),
        "dealer_over_player": (f"The dealer's {dealer_total} beats your {player_total}. "
                               "The dealer wins!\n"),
        "tiebreaker": (f"Your {player_total} matches the dealer's {dealer_total}. " 
                       "The dealer wins the tiebreak!\n")
    }

    print(outcomes[outcome])

    if outcome == "player_bust" or outcome == "dealer_over_player" or outcome == "tiebreaker":
        balance -= player_bet
    elif outcome == "dealer_bust" or outcome == "player_over_dealer":
        balance += player_bet

    print("Thanks for playing!\n")

    return balance




def play_game(balance):
    """
    This function contains the main game flow control for the 
    entire program. It brings all of the other functions together
    to make the program flow smoothly. It also takes and returns the balance
    as this is how I made it so that the balance could be saved/ updated after
    each round based on if the user won or lost
    """
    print(f"\nA new game of blackjack has began. Your betting balance is ${balance}\n")
    initial_draw_cards = draw_cards()
    player_first = initial_draw_cards["player_first"]
    player_second = initial_draw_cards["player_second"]
    dealer_first = initial_draw_cards["dealer_first"]
    dealer_second = initial_draw_cards["dealer_second"]


    player_total, player_bet = players_turn(player_first, player_second, dealer_first, balance)

    if player_total > 21:
        round_info = {"player_total": player_total, "player_bet": player_bet,
                      "balance": balance, "dealer_total": 0}
        balance = end_game("player_bust", round_info)
    else:
        dealer_total = dealers_turn(dealer_first, dealer_second)
        round_info = {"player_total": player_total, "player_bet": player_bet,
                      "balance": balance, "dealer_total": dealer_total}
        if dealer_total > 21:
            balance = end_game("dealer_bust", round_info)
        elif player_total > dealer_total:
            balance = end_game("player_over_dealer", round_info)
        elif player_total < dealer_total:
            balance = end_game("dealer_over_player", round_info)
        else:
            balance = end_game("tiebreaker", round_info)

    return balance



def main():
    """
    This is the main function. When program is first called,
    it sets the initial balance as $100. It then loops to keep the game
    running as long as the user doesn't quit or have their balance equal 
    $0 (this logic is actually set in the want_to_play() function 
    """
    balance = 100
    while True:
        start = want_to_play(balance)
        if start == "Q":
            print("\nSee you later!\n")
            quit()
        else:
            balance = play_game(balance)

if __name__ == "__main__":
    main()

import random
import json
import os
import sys
import JsonFileManager as json_fm
from controls import PlayerControls

# Define the directory for JSON files
JSON_DIR = "PLAYER_DATA"

# Create an instance of JsonFileManager
json_fm_instance = json_fm.JsonFileManager(JSON_DIR)
# Create an instance of PlayerControls
player_controls = PlayerControls(json_fm_instance.load_balance(), json_fm_instance.load_spin_count(), json_fm_instance.load_spin_count())

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {
    "@" : 5,
    "£" : 10,
    "$" : 20,
    "€" : 40,
    "§" : 25,
}

symbol_values = {
    "@" : 10,
    "£" : 5,
    "$" : 3,
    "€" : 2,
    "§" : 0,
}

# Define a list of quotes
quotes_win = [
    "You are on a roll! Keep going!",
    "You are so close to the jackpot, keep going!",
    "You are doing great! Keep going!",
    "You are on a winning streak! Keep going!",
    "You are on fire! Keep going!",
    "You are so lucky! Keep going!",
    "You are doing amazing! Keep going!",
    "With the multiplier, you could win even more!",
    "There is a chance to dubble your winnings!",
    "Up to 1000x your winnings with the multiplier!",
    "I know you would love to double that number!",
    "Spin to win!",
    "Roll the reels!",
    "Jackpot dreams and spinning reels.",
    "The sound of spinning reels, music to the ears.",
    "Dare to dream big, spin to win big.",
]

quotes_loss = [
    "I know you are thinking about quitting, but don't you want to double that number tho?",
    "Only a small setback, focus on the next spin!",
    "Every gambler quits just before they win big, don't be that guy!",
    "Can't stop on a loss, the next one is yours!",
    "The next one is yours, I can feel it!",
    "Don't stop now, the next one is a winner!",
    "Spin to win!",
    "Roll the reels!",
    "Winning streak ahead?",
    "Dare to dream big, spin to win big.",
    "A winning combination is just a spin away.",
    "Every setback is a setup for a comeback!",
    "Don't let a loss dim your winning spirit.",
    "It's not about how hard you fall, but how high you bounce back.",
    "Embrace setbacks as stepping stones to success.",
    "The greatest glory is not in never falling, but in rising every time we fall.",
    "Failure is not the opposite of success; it's part of the journey.",
    "Your past does not determine your future; keep spinning towards your goals.",
]


def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []

    # Check horizontal winning lines
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)

    # Check vertical winning lines
    for column in columns:
        symbol = column[0]
        for symbol_to_check in column:
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            if winning_lines:
                winning_lines.append(winning_lines[-1] + 1)
            else:
                winning_lines.append(1)

    # Check diagonal winning lines
    if columns[0][0] == columns[1][1] == columns[2][2]:
        winnings += values[columns[0][0]] * bet
        winning_lines.append(4)
    if columns[0][2] == columns[1][1] == columns[2][0]:
        winnings += values[columns[0][2]] * bet
        winning_lines.append(5)

    return winnings, winning_lines

def multi_win(winnings, winning_lines):
    
    #Increase the winnings by 20% for each extra winning line beyond the first.
    
    if len(winning_lines) > 1:
        extra_lines = len(winning_lines) - 1
        extra_winnings = extra_lines * 0.2 * winnings
        return int(winnings + extra_winnings)
    else:
        return int(winnings)
    

def random_multi_winnings(winnings):
   
    #Apply a random multiplier to the winnings based on specified probabilities.
   
    # Define probabilities for each multiplier
    probabilities = {
        1000:   0.00001,     # 0.001% chance to multiply winnings by 1000
        100:    0.0001,      # 0.01% chance to multiply winnings by 100
        10:     0.001,       # 0.1% chance to multiply winnings by 10
        2:      0.01,        # 1% chance to double the winnings
        1.5:    0.05,        # 5% chance to add 50% of the winnings
        1.3:    0.10,        # 10% chance to add 30% of the winnings
        1.1:    0.22,        # 22% chance to add 10% of the winnings
        0:      0.50,        # 50% chance to lose the winnings
        -0.1:   0.10,        # 10% chance to lose 10% of the winnings
        -0.5:   0.04         # 4% chance to lose 50% of the winnings
    }

    # Choose a multiplier based on probabilities
    multiplier = random.choices(list(probabilities.keys()), list(probabilities.values()))[0]

    # Apply the multiplier to the winnings
    if multiplier == 10:
        return int(winnings * 10)
    elif multiplier == 100:
        return int(winnings * 100)
    elif multiplier == 2:
        return int(winnings * 2)
    elif multiplier == 1.5:
        return int(winnings * 1.5)
    elif multiplier == 1.3:
        return int(winnings * 1.3)
    elif multiplier == 1.1:
        return int(winnings * 1.1)
    elif multiplier == -0.1:
        return int(winnings * 0.9)
    elif multiplier == -0.5:
        return int(winnings * 0.5)
    else:
        return 0  # If no multiplier is applied, user loses their winnings



def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []    # define columns as an empty list
    for _ in range(cols):  # generte columns for the amount of COLS we have
        column = []
        current_symbols = all_symbols[:]  #copy the list with [:]
        for row in range(rows): #generate rows for the amount of ROWS we have
            value = random.choice(current_symbols)  #randomly choose a symbol from the current_symbols list
            current_symbols.remove(value)   #remove the symbol from the current_symbols list
            column.append(value)    #append the symbol to the column list
            
        columns.append(column)   
    return columns



slot_machine_part_1 = """                .-------.
            oO{-(\033[33m\033[5mMACHINE\033[0m)-}Oo
            .==============. """

slot_machine_part_2 = """            |--------------| __
            | €€€ :::::::: |(  )
            | £££ :::::::: | ||
            | $$$ :::::::: |_||"""
            
slot_machine_part_4 = """            |      __  === |
            |_____[__]_____|
           /################
          /##################
         |####################|"""

def slot_machine_part_3(winnings):
    # Convert winnings to a string
    winnings_str = str(winnings)
    # Calculate the length of the winnings string
    winnings_length = len(winnings_str)
    # Calculate the number of spaces needed to fill the remaining length
    spaces_needed = 15 - winnings_length - 1  # Subtract 1 for the space between winnings and the padding
    # If the winnings string is longer than 15 characters, truncate it
    if winnings_length > 15:
        return winnings_str[:15]
    # If the winnings string is shorter than 15 characters, pad it with spaces
    else:
        asci_winnings = " " * 12 +"|" + (spaces_needed - 1) * " " + "\033[33m" + winnings_str + "\033[0m" +" |--'"
        print(asci_winnings)
        return asci_winnings


def print_slot_machine(columns):
    print(slot_machine_part_1)
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)  # Generate slot machine spin
    winnings, winning_lines = check_winnings(slots, MAX_LINES, MAX_BET, symbol_values)  # Calculate winnings
    for row in range(len(columns[0])):  # For each row in the first column
        print(" " * 12, end="|   ")  # Print 12 spaces and "|" at the beginning of each row
        for i, column in enumerate(columns):  # For each column in the columns list
            if i != len(columns) - 1:  # If the column is not the last column
                symbol = column[row]
                if symbol == "@":
                    print("\033[31m" + symbol + "\033[0m", end=" | ")  # Red color for symbol "@"
                elif symbol == "£":
                    print("\033[32m" + symbol + "\033[0m", end=" | ")  # Green color for symbol "£"
                elif symbol == "$":
                    print("\033[33m" + symbol + "\033[0m", end=" | ")  # Yellow color for symbol "$"
                elif symbol == "€":
                    print("\033[34m" + symbol + "\033[0m", end=" | ")  # Blue color for symbol "€"
                elif symbol == "§":
                    print("\033[35m" + symbol + "\033[0m", end=" | ")  # Magenta color for symbol "§"
            else:
                symbol = column[row]
                if symbol == "@":
                    print("\033[31m" + symbol + "\033[0m" + " ", end=" | ")  # Red color for symbol "@"
                elif symbol == "£":
                    print("\033[32m" + symbol + "\033[0m" + " ", end=" | ")  # Green color for symbol "£"
                elif symbol == "$":
                    print("\033[33m" + symbol + "\033[0m" + " ", end=" | ")  # Yellow color for symbol "$"
                elif symbol == "€":
                    print("\033[34m" + symbol + "\033[0m" + " ", end=" | ")  # Blue color for symbol "€"
                elif symbol == "§":
                    print("\033[35m" + symbol + "\033[0m" + " ", end=" | ")  # Magenta color for symbol "§"
        print()  # Print a new line
      

    
def deposit():
    while True:
        amount = input("Enter the amount you want to deposit: $")
        if amount.isdigit():
            amount = int(amount)
            if amount == 1069:
                print("\nCheeky basterd. I'll let that one slide.\n")
            elif amount > 1000 and amount != 1069:
                print("Don't get over your head. You get $1000 to start with.")
                amount = 1000
            elif amount <= 0:
                print("Please enter a positive amount.")
            break
        else:
            print("Please enter a valid amount.")
    return amount

def get_number_of_lines():
    lines = MAX_LINES
    return lines


def get_bet():
    while True:
        bet = input(f"How much do you want to bet? (${MIN_BET} and ${MAX_BET})? $")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            elif bet > MAX_BET:
                bet = MAX_BET
                break
            else:
                print(f"Please enter a bet between ${MIN_BET} and ${MAX_BET}.")
        else:
            print("Please enter a valid bet.")
    return bet

def check_balance(balance):
    while True:
        bet = get_bet()
        if bet > balance:
            print(f"You don't have enough money to make that bet. Your balance is ${balance}")
        else:
            break

def validate_bet(balance):
    while True:
        bet = get_bet()
        if bet > balance:
            print(f"You don't have enough money to make that bet. Your balance is ${balance}")
        else:
            return bet

def print_multiplier_message(winnings, new_winnings):
    if new_winnings > winnings:
        print("\033[35mProfits on top of profits!\033[0m")
        if new_winnings >= winnings * 100:
            print("\033[35mYou hit the jackpot! Your winnings are multiplied by 100!\033[0m")
        elif new_winnings >= winnings * 10:
            print("\033[35mYou got a massive win! Your winnings are multiplied by 10!\033[0m")
        elif new_winnings >= winnings * 2:
            print("\033[35mYou doubled your winnings with the multiplier!\033[0m")
        elif new_winnings >= winnings * 1.5:
            print("\033[35mYou increased your winnings by 50% with the multiplier!\033[0m")
        else:
            print("\033[35mYou made some profit with the multiplier!\033[0m")
    
def apply_multipliers(winnings):
    if winnings > 0:
        print("\033[36m" + random.choice(quotes_win) + "\033[0m")
        choice = input("Do you want to use a random multiplier on your winnings? (N to skip): ").upper()
        if choice != "N":
            json_fm_instance.update_multiplier_count()
            new_winnings = random_multi_winnings(winnings)
            print_multiplier_message(winnings, new_winnings)
            if new_winnings > 0:
                print("Adjusted winnings: \033[33m$" + str(new_winnings) + "\033[0m")
            else:
                print("Adjusted winnings: \033[33m$" + str(new_winnings) + "\033[0m")
        else:
            new_winnings = winnings
            print("\033[36m" + random.choice(quotes_loss) + "\033[0m")
    else:
        new_winnings = 0
        print("\033[36m" + random.choice(quotes_loss) + "\033[0m")
    return new_winnings


def check_spin_counter(start_spin_count):
    if json_fm_instance.spin_counter > 1000000:
        print("\033[36mA FOOKIN LEGEND, that's what you are!\033[0m\n")
    elif json_fm_instance.spin_counter > 250000:
        print("\033[36mHigh roller club member\033[0m\n")
    elif json_fm_instance.spin_counter > 100000:
        print("\033[36mOne of the VIP's\033[0m\n")
    elif json_fm_instance.spin_counter > 50000:
        print("\033[36mWe have a gambler here\033[0m\n")
    elif json_fm_instance.spin_counter > 10000:
        print("\033[36mWelcome back fren\033[0m\n")
    elif json_fm_instance.spin_counter > 5000:
        print("\033[36mWelcome back rookie\033[0m\n")
    elif json_fm_instance.spin_counter > 1000:
        print("\033[36mWelcome back newbie\033[0m\n")
    else:
        print("\033[36mStill new here i see\033[0m\n")


def check_session_spins(session_spins):
    if session_spins > 1000:
        print("\033[36mYou've spun the reels over 1000 times! FOOKIN LEGEND!!!\033[0m \n")
    elif session_spins > 500:
        print("\033[36mYou've spun the reels over 500 times! Thats the spirit!\033[0m \n")
    elif session_spins > 100:
        print("\033[36mYou've only spun the reels over 100 times. Thats below average!\033[0m \n")
    elif session_spins < 100:
        print("\033[36mNot even 100 spins. You can do better!\033[0m \n")

def spin(balance):
    json_fm_instance.update_spin_count()
    lines = get_number_of_lines()
    bet = validate_bet(balance)
    print(f"You are betting ${bet}")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)

    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_values)

    print_slot_machine(slots)
    print(slot_machine_part_2)  
    slot_machine_part_3(winnings)
    print(slot_machine_part_4)
    print()
    
    print("You won \033[33m$" + str(winnings) + "\033[0m")
    print("You won on line(s):", *winning_lines) 

    return apply_multipliers(winnings) - bet




def broke(balance):
    if balance == 0:
        json_fm_instance.update_broke_counter()
        json_fm_instance.save_balance(balance)
        print("\033[33mTime to go home fren\033[0m")
        print("We'll get that money anyway somehow")
        return True



def main():
    print("\nWelcome to the slot machine!\n")
    
    # Load spin count
    start_spin_count = json_fm_instance.load_spin_count()
    balance = json_fm_instance.load_balance()
    highscore = json_fm_instance.load_highscore()
    multiplier_count = json_fm_instance.load_multiplier_count()
    broke_counter = json_fm_instance.load_broke_counter()

    print(f"Total spins: \033[34m{start_spin_count}\033[0m")
    check_spin_counter(start_spin_count)
    json_fm_instance.print_highscore(highscore)

    spin_counter = start_spin_count  # Set the current spin count to the start spin count

    json_fm_instance.print_multiplier_count(multiplier_count)

    json_fm_instance.print_broke_counter(broke_counter)
    
    if balance is None or balance == 0:
        print("No balance found or balance is zero.")
        balance = deposit()
    else:
        json_fm_instance.print_balance(balance)
    
    while True:
        
        if broke(balance):  
            break
        
        answer = input("Press enter to play (Q to quit): ")
        
        if answer.lower() == "q":
            session_spins = spin_counter - start_spin_count
            print(f"\nYou made \033[34m{session_spins}\033[0m spins this session.")
            check_session_spins(session_spins)
            print(f"You checked out with \033[32m${balance}\033[0m. Thanks for playing!\n")
            json_fm_instance.save_balance(balance)
            player_controls.quit()
        else:    
            balance += spin(balance)
            if balance > highscore:
                highscore = balance
                json_fm_instance.save_highscore(highscore)
            spin_counter += 1  # Increment spin count
    
    # Save Json files
    json_fm_instance.save_spin_count(spin_counter)
    json_fm_instance.save_balance(balance)
    json_fm_instance.save_highscore(highscore)
    json_fm_instance.save_broke_counter(broke_counter)

if __name__ == "__main__":
    main()




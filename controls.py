import sys
import JsonFileManager as json_fm  
import time


class PlayerControls:
    def __init__(self, balance, json_fm_instance: json_fm.JsonFileManager, spin_counter, print_max_bets, print_multiplier_count, print_broke_counter):
        self.balance = balance
        self.json_fm_instance = json_fm_instance
        self.spin_counter = spin_counter
        self.print_max_bets = print_max_bets
        self.print_multiplier_count = print_multiplier_count
        self.print_broke_counter = print_broke_counter
        

    def print_help(self):
        print("\n\t Available controls:\n")
        print(" -help   : Show available controls and their descriptions.")
        print(" -quit   : Quit the game.")
        print(" -stats  : Show your statistics.")
        print(" -dealer : To ask the dealer for higher max bets.")
        print(" -allin  : Exactly what you think, going all in!\n")

    def control_check(self, user_input, start_spin_count):
        if user_input == "-help": 
            self.print_help()
        elif user_input == "-quit": 
            self.quit(start_spin_count, self.spin_counter, self.balance)
        elif user_input == "-stats":
            self.print_stats()
        elif user_input == "-dealer":
            self.dealer()
        elif user_input == "-allin":
            self.allin()
        else:
            return 

    def dealer(self):
        dealer_level = self.json_fm_instance.load_dealer_lv()

        if self.balance < 10000:
            print("\nYou need at least 10k balance to increase your maximum bets.\n")
        elif self.balance >= 10000 and dealer_level == 0:
            print("\nYour maximum bets are now increased to 1000.\n")
            self.json_fm_instance.update_dealer_lv_up()
        elif self.balance >= 50000 and dealer_level == 1:
            print("\nYour maximum bets are now increased to 5000.\n")
            self.json_fm_instance.update_dealer_lv_up()
        elif self.balance >= 100000 and dealer_level == 2:
            print("\nYour maximum bets are now increased to 10000.\n")
            self.json_fm_instance.update_dealer_lv_up()
        else:
            print("\nYou've reached the maximum dealer level. \n")
            
        

    def quit(self, balance, spin_counter, start_spin_count):
        session_spins = spin_counter - start_spin_count
        print(f"\nYou made \033[34m{session_spins}\033[0m spins this session.")
        #check_session_spins(session_spins) # personal message
        print(f"You checked out with \033[32m${balance}\033[0m. Don't forget to come back!\n")
        self.json_fm_instance.save_balance(balance)
        sys.exit() 

    def print_stats(self):
        print("\n Player statistics: \n")
        print(f"Balance: ${self.balance}")
        print(f"Total spins: {self.spin_counter}")
        self.json_fm_instance.print.maximum_bets(self.json_fm_instance.load_dealer_lv())
        self.json_fm_instance.print_multiplier_count(self.json_fm_instance.load_multiplier_count())
        self.json_fm_instance.print_broke_counter(self.json_fm_instance.load_broke_counter())
        

    def allin(self):
        input("Are you sure you want to go all in? (yes/no) ")
        if input() == "yes":
            print("Let's get the manager here to monitor your spin. \n")
            print_dots(3)
            print(f"\nYou will bet {self.balance}. May luck be on your side.\n")
            return True
        else: 
            print("Every shot you don't take is a guarantee miss.\n")
            return False

def print_dots(num_dots, delay=1):
    for _ in range(num_dots):
        print(".", end="", flush=True)  # Print a dot without newline and flush the output
        time.sleep(delay)  # Wait for the specified delay before printing the next dot
    print()  # Print a newline after all dots are printed



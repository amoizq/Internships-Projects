import time
import sys

class User:
    def __init__(self, user_id, pin, balance=0):
        # Initialize a new user with user ID, PIN, and an initial balance
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transactions = []  # List to store the user's transaction history

    def add_transaction(self, transaction):
        # Add a transaction to the user's transaction history
        self.transactions.append(transaction)

class ATM:
    def __init__(self):
        # Initialize the ATM with an empty dictionary of users and no current user logged in
        self.users = {}  # Dictionary to store user objects with user ID as the key
        self.current_user = None  # Variable to store the currently logged in user

    def add_user(self, user):
        # Add a user to the ATM's user dictionary
        self.users[user.user_id] = user

    def authenticate_user(self, user_id, pin):
        # Authenticate a user based on user ID and PIN
        user = self.users.get(user_id)  # Get the user object from the dictionary
        if user and user.pin == pin:  # Check if the user exists and the PIN is correct
            self.current_user = user  # Set the current user to the authenticated user
            return True
        return False  # Return False if authentication fails

    def transaction_history(self):
        # Display the current user's transaction history
        if not self.current_user.transactions:
            print("No transactions found.")  # If no transactions, print message
        else:
            for transaction in self.current_user.transactions:
                print(transaction)  # Print each transaction in the history

    def withdraw(self, amount):
        # Withdraw a specified amount from the current user's account
        if amount > self.current_user.balance:
            print("Insufficient funds.")  # Print message if insufficient balance
        else:
            self.current_user.balance -= amount  # Deduct the amount from the balance
            self.current_user.add_transaction(f"Withdraw: {amount} PKR")  # Add transaction to history
            print(f"Withdrew {amount} PKR. New balance: {self.current_user.balance} PKR")

    def deposit(self, amount):
        # Deposit a specified amount into the current user's account
        self.current_user.balance += amount  # Add the amount to the balance
        self.current_user.add_transaction(f"Deposit: {amount} PKR")  # Add transaction to history
        print(f"Deposited {amount} PKR. New balance: {self.current_user.balance} PKR")

    def transfer(self, target_user_id, amount):
        # Transfer a specified amount from the current user to another user
        target_user = self.users.get(target_user_id)  # Get the target user object
        if not target_user:
            print("Target user not found.")  # Print message if target user does not exist
        elif amount > self.current_user.balance:
            print("Insufficient funds.")  # Print message if insufficient balance
        else:
            self.current_user.balance -= amount  # Deduct the amount from the current user's balance
            target_user.balance += amount  # Add the amount to the target user's balance
            self.current_user.add_transaction(f"Transfer to {target_user_id}: {amount} PKR")  # Add transaction to history
            target_user.add_transaction(f"Received transfer from {self.current_user.user_id}: {amount} PKR")
            print(f"Transferred {amount} PKR to user {target_user_id}. New balance: {self.current_user.balance} PKR")

    def start(self):
        # Start the ATM system and handle user login
        while True:
            user_id = input("Enter User ID: ")  # Prompt user for their ID
            pin = input("Enter PIN: ")  # Prompt user for their PIN
            if self.authenticate_user(user_id, pin):
                print("Login successful.")  # If authenticated, print success message
                self.main_menu()  # Show the main menu
            else:
                print("Invalid User ID or PIN.")  # Print error message if authentication fails

    def main_menu(self):
        # Display the main menu and handle user choices
        while True:
            print("\nMain Menu")
            print("1. Transaction History")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Transfer")
            print("5. Quit")
            choice = input("Choose an option: ")  # Prompt user to choose an option
            if choice == '1':
                self.transaction_history()  # Show transaction history
            elif choice == '2':
                amount = float(input("Enter amount to withdraw: "))  # Prompt for amount
                self.withdraw(amount)  # Perform withdrawal
            elif choice == '3':
                amount = float(input("Enter amount to deposit: "))  # Prompt for amount
                self.deposit(amount)  # Perform deposit
            elif choice == '4':
                target_user_id = input("Enter target User ID: ")  # Prompt for target user ID
                amount = float(input("Enter amount to transfer: "))  # Prompt for amount
                self.transfer(target_user_id, amount)  # Perform transfer
            elif choice == '5':
                while True:
                    confirm = input("Are you sure you want to quit? (Yes/No): ").strip().capitalize()
                    # Ask for confirmation to quit
                    if confirm == 'Yes':
                        print("Exiting", end="")
                        for _ in range(5):
                            print(".", end="", flush=True)  # Show loading dots
                            time.sleep(1)
                        print("\nThank you for using the ATM. To use the ATM again, please restart the program.")
                        raise SystemExit  # Exit the program
                    elif confirm == 'No':
                        break  # Break the inner loop and go back to the main menu
                    else:
                        print("Invalid response. Please type 'Yes' or 'No'.")
            else:
                print("Invalid option, please try again.")  # Handle invalid menu option

# Example setup: create an ATM instance and add users to it
atm = ATM()
atm.add_user(User("Moiz", "1234", 5000))  # Add a user with ID 'user1' and initial balance of 5000 PKR
atm.add_user(User("Qureshi", "5678", 2000))  # Add a user with ID 'user2' and initial balance of 2000 PKR

# Start the ATM system
try:
    atm.start()
except SystemExit:
    print("Program exited successfully.")
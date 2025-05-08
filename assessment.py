import os
import random
import json

# User Functions
class User:
    # Get user data from the database with the username
    @staticmethod
    def get_user(username):
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
                return users.get(username)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    # Create a user and store the user data in the DB
    @staticmethod
    def create_user(username):
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}
        
        users[username] = {"highscore": 0}
        
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)
        
        return users[username]

# Quiz Math Functions
class MathQuiz:
    # The types of math equations 
    TYPES = ['+', '-', '*', '/']
    
    # Create a equation and give back the answer with the given operation
    @staticmethod
    def create_equation(operation):
        if operation == '+':
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 100)
            return num1, num2, num1 + num2
        
        elif operation == '-':
            num1 = random.randint(50, 200)
            num2 = random.randint(1, 50)
            return num1, num2, num1 - num2
        
        elif operation == '*':
            num1 = random.randint(1, 12)
            num2 = random.randint(1, 12)
            return num1, num2, num1 * num2
        
        elif operation == '/':
            num1 = random.randint(1, 100)
            num2 = random.randint(1, 10)
            result = num1 // num2
            return num1, num2, result

    # Start the Quiz
    @staticmethod
    def start_quiz(username):
        user_data = User.get_user(username) or User.create_user(username)
        highscore = user_data.get('highscore', 0)
        score = 0

        # Ask the user what type of math they wanna quiz theyre self on    
        while True:
            symbol = input("What type of math would you like to quiz yourself on (+, -, *, /)? ").strip()
            if symbol not in MathQuiz.TYPES:
                print("Please enter a valid math symbol.")
                continue
            
            # Create a equation and ask the user for the answer
            while True:
                num1, num2, correct_answer = MathQuiz.create_equation(symbol)

                try:
                    # Create a input
                    user_answer = int(input(f"{num1} {symbol} {num2} = ? : "))

                    # Checking if the answer is right
                    if user_answer == correct_answer:
                        # If correct
                        score += 1
                        print(f"Correct! Current score: {score}")
                    else:
                        # If incorrect
                        print(f"Wrong! Correct answer was {correct_answer}.")
                        break

                except ValueError:
                    print("Please enter a valid number.")

            # Highscore function
            if score > highscore:
                highscore = score
                user_data["highscore"] = highscore

                try:
                    with open("users.json", "r") as file:
                        users = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError):
                    users = {}

                users[username] = user_data

                with open("users.json", "w") as file:
                    json.dump(users, file, indent=4)

            # Ask user if they wanna play again
            play_again = input("Do you want to play again? (yes/no): ").lower()
            if play_again != 'yes':
                break

# UI For the quiz
class UI:
    @staticmethod
    def startup():
        os.system('cls')
        print("Hello! Welcome to The NPBHS 2025 Math Quiz v1.0")
        
        # Ask user for username
        username = input("Please Enter Your Username: ").strip()
        user_data = User.get_user(username)
        
        # If no user then create user
        if user_data is None:
            user_data = User.create_user(username)
            print("Welcome! It seems this is your first time using our Math Quiz. Your account has been created.")
        else:
            print(f"Welcome Back, {username}! Your Highscore Is {user_data.get('highscore', 0)}")
        
        MathQuiz.start_quiz(username)

# Start the App
if __name__ == "__main__":
    UI.startup()

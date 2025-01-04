import random

def game_logic(chances):
    lucky_number = random.randint(1, 100)
    attempts = 1
    while chances != 0:
        number = int(input('Enter your guess: '))
        if number == lucky_number:
            print(f'Congratulations! You guessed the correct number in {attempts} attempts.')
            return
        else:
            if lucky_number > number:
                print(f'Incorrect! The number is greater than {number}.')
            else:
                print(f'Incorrect! The number is less than {number}.')
        chances -= 1
        attempts += 1
        
        print(f'Chances Remaining: {chances}')
        print()



def main():
    print()
    print('Welcome to the Number Guessing Game!')
    print("I'm thinking of a number between 1 and 100.")
    print()

    print('Please select the difficulty level:')
    print('1. Easy (10 chances)')
    print('2. Medium (5 chances)')
    print('3. Hard (3 chances)')
    print()

    while True:
        choice = int(input('Enter your choice: '))
        if choice not in [1, 2, 3]:
            print('Not a Valid Input. Try Again.')
        
        else:
            difficulty = ''
            chances = 0
            if choice == 1:
                difficulty = 'Easy'
                chances = 10
            elif choice == 2:
                difficulty = 'Medium'
                chances = 5
            else:
                difficulty = 'Hard'
                chances = 3

            print(f'Great! You have selected the {difficulty} difficulty level.')
            print()
            print("Let's start the game!")
            print()
            game_logic(chances)
            break
            

if __name__ == '__main__':
    main()
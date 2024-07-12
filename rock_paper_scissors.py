import random

human = input("Enter your choice: ")

print("Human: ", human)

computer = random.choice(["rock", "paper", "scissors"])

print("Computer: ", computer)

if human == computer:
    print("Draw")

elif human == "rock" and computer == "paper":
    print("Computer wins!")
elif human == "scissors" and computer == "rock":
    print("Computer wins!")
elif human == "paper" and computer == "scissors":
    print("Computer wins!")

elif human == "paper" and computer == "rock":
    print("Human wins!")
elif human == "rock" and computer == "scissors":
    print("Human wins!")
elif human == "scissors" and computer == "paper":
    print("Human wins!")

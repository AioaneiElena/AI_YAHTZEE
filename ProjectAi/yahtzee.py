import random
import gamescheck
from gamescheck import game_functions


def InitialState():
    return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

def isFinalState(state):
    if state==(1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1):
        return True
    else:
        return False

def InialGame():
    games = [
        "Ones", "Twos", "Threes", "Fours", "Fives",
        "Sixes", "Three of kind", "Four of kind", "Full house", "Small straight",
        "Large straight", "Chance", "YAHTZEE"
    ]

    games_scores = [[game, -1, -1] for game in games]


def RollDice(dices):
    for i in range(len(dices[0])):
        if dices[0][i]==0:
            dices[1][i] = random.randint(1, 6)

def PrintTable(games_scores):
    for game in games_scores:
        print(f"{game[0]}    |     {game[1]}        |      {game[2]}")

def PrintWinningPointsGames(dices,games_scores,player):
    for game in games_scores:
        if(game[player+1]==-1):
            score = game_functions[game[0]](dices)
            if(score != 0):
                print(f"{game[0]} : {score}")
game_numbers = {
    "Ones": 1,
    "Twos": 2,
    "Threes": 3,
    "Fours": 4,
    "Fives": 5,
    "Sixes": 6,
    "Three of a kind": 7,
    "Four of a kind": 8,
    "Full House": 9,
    "Small Straight": 10,
    "Large Straight": 11,
    "Chance": 12,
    "YAHTZEE": 13
}

def Transition(state, player, game_number):
    state[0]= not player
    state[(player+1)* game_number]=1


def Turn(state, games_scores):
    dices = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    count =0

    if state[0]==0:
        while(count< 3):
            print("Your turn:")
            RollDice(dices)
            print("Roll dices: ", dices[1])
            PrintTable(games_scores)
            print("Winning points' games: ")
            PrintWinningPointsGames(dices,games_scores,state[0])
            response = input("Do you want to select a game? y/n")
            if response == "y":
                response = input("Write the name of the game: ")
                score = game_functions[response](dices)
                games_scores[response][1]= score
                state = Transition (state,1,game_numbers[response])
                count =3
            else:
                response=input("Choose the dices you want to keep: ")
                dices_to_keep = list(map(int, response.split()))
                for dice in dices_to_keep:
                    dices[0][dice]=1

    else:
        print("Computer's turn:")
        while (count < 3):
            RollDice(dices)

InialGame()
print ( Turn(InitialState(),games_scores)


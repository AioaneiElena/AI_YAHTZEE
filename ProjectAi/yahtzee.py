import random
import gamescheck
from gamescheck import game_functions

bonus_score_p0=0
bonus_score_p1=0
ok_p0=0
ok_p1=0

def InitialState():
    return (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)


def isFinalState(state):
   if all(s == 1 for s in state[:-4]):
       print("Player 1 score: ", state[27])
       print("Player 2 score: ", state[28])
       if state[27]>state[28]:
           print("Player 1 wins!")
       elif state[28]>state[27]:
           print("Player 2 wins!")
       else:
           print("It's a tie!")
       return True
   return False


def InialGame():
    games = [
        "Ones", "Twos", "Threes", "Fours", "Fives",
        "Sixes", "Three of a kind", "Four of a kind", "Full House", "Small Straight",
        "Large Straight", "Chance", "YAHTZEE"
    ]

    games_scores = [[game, -1, -1] for game in games]
    games_scores.append(["Bonus", 0, 0])
    games_scores.append(["Total", 0, 0])
    return games_scores


def RollDice(dices):
    for i in range(len(dices[0])):
        if dices[0][i] == 0:
            dices[1][i] = random.randint(1, 6)


def PrintTable(games_scores):
    for game in games_scores:
        print(f"\033[92m{game[0]} | {game[1]} | {game[2]}\033[0m")


def PrintWinningPointsGames(dices, games_scores, player):
    for game in games_scores:
        if (game[player + 1] == -1):
            score = game_functions[game[0]](dices)
            if (score != 0):
                print(f"\033[93m{game[0]} : {score}\033[0m")


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


def Transition(state, player, game_number, score):
    state_list = list(state)
    state_list[(player + 1) * game_number] = 1
    state_list[0] = int(not player)
    state_list[player + 27] += score
    if game_number<=6:
        state_list[player + 29] += score
    print(tuple(state_list))
    return tuple(state_list)


def Validation(state, player, game_number):
    if state[(player + 1) * game_number] == 1:
        return False
    return True

def DiceValidation(dices, dices_to_let):
    for dice in dices_to_let:
        if dices[0][dice]==0:
            print("Invalid dice")
            return False
    return True

def UpdateScore(player, game_name, dices ):
    global ok_p0
    global bonus_score_p0
    global ok_p1
    global bonus_score_p1
    if player==0:
        game_index = game_numbers[game_name]
        print(game_index)
        score = game_functions[game_name](dices)
        games_scores[game_index - 1][1] = score
        if game_index <= 6:
            bonus_score_p0 += score
            print(bonus_score_p0)
            if bonus_score_p0 >= 63 and ok_p0 == 0:
                games_scores[13][1] = 35
                games_scores[14][1] += 35
                ok_p0 = 1
        games_scores[14][1] += score
        return score
    else:
        game_index = game_numbers[game_name] - 1
        score = game_functions[game_name](dices)
        games_scores[game_index][2] = score
        if game_index <= 6:
            bonus_score_p1 += score
            if bonus_score_p1 >= 63 and ok_p1 == 0:
                games_scores[13][2] = 35
                games_scores[14][2] += 35
                ok_p1 = 1
        games_scores[14][2] += score
        return score


def PlayerChoose(games_scores):
    dices = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    count = 0

    while count < 3:

        RollDice(dices)
        print("Roll dices: ", dices[1])
        PrintTable(games_scores)
        print("Winning points' games: ")
        PrintWinningPointsGames(dices, games_scores, 0)

        response = input("Do you want to select a game? y/n :").strip()
        if response.lower() == "y":
            game_name = input("Write the name of the game: ").strip()
            while game_name not in game_numbers:
                print("Invalid game name. Please try again.")
                game_name = input("Write the name of the game: ").strip()
            score= UpdateScore(0,game_name,dices)
            return game_name, score

        else:

            response = input("Choose the dices you want to keep: ")
            dices_to_keep = list(map(int, response.split()))
            for dice in dices_to_keep:
                dices[0][dice] = 1
            response = input("Choose the dices you want to let go: ")
            dices_to_let = list(map(int, response.split()))
            while not DiceValidation(dices, dices_to_let):
                response = input("Choose the dices you want to let go: ")
                dices_to_let = list(map(int, response.split()))
            for dice in dices_to_let:
                dices[0][dice] = 0
            count+=1

    game_name = input("You can't roll again. Write the name of the game: ").strip()
    while game_name not in game_numbers:
        print("Invalid game name. Please try again.")
        game_name = input("Write the name of the game: ").strip()
    score = UpdateScore(0, game_name, dices)
    return game_name, score


def ComputerChoose(games_scores):
    dices = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    count = 0

    while count < 3:
        RollDice(dices)
        print("Computer rolls: ", dices[1])
        available_games = [game for game in games_scores if game[2] == -1]

        if available_games and random.choice([True, False]):  # 50% șansă
            selected_game = random.choice(available_games)
            game_name = selected_game[0]
            score=UpdateScore(1, game_name, dices)
            print(f"Computer chooses {game_name} and scores {score}")
            return game_name, score

        else:
            dices_to_keep = random.sample(range(5), k=random.randint(0, 5))
            print(f"Computer keeps dices: {dices_to_keep}")
            for dice in dices_to_keep:
                dices[0][dice] = 1
            dices_to_let = random.sample(range(5), k=random.randint(0, 5))
            while not DiceValidation(dices, dices_to_let):
                dices_to_let = random.sample(range(5), k=random.randint(0, 5))
            print(f"Computer lets dices: {dices_to_let}")
            for dice in dices_to_let:
                dices[0][dice] = 0
            count += 1

    selected_game = random.choice(available_games)
    game_name = selected_game[0]
    score = UpdateScore(1, game_name, dices)
    print(f"Computer chooses {game_name} and scores {score}")
    return game_name, score

def WelcomeInterface():
    print("""Yahtzee Rules
The objective of YAHTZEE is to get as many points as possible by rolling five dice and getting certain combinations of dice.

Gameplay
In each turn a player may throw the dice up to three times. A player doesn't have to roll all five dice on the second and third throw of a round, he may put as many dice as he wants to the side and only throw the ones that don't have the numbers he's trying to get. For example, a player throws and gets 1,3,3,4,6. He decides he want to try for the large straight, 1,2,3,4,5. So, he puts 1,3,4 to the side and only throws 3 and 6 again, hoping to get 2 and 5.

In this game you click on the dice you want to keep. They will be moved down and will not be thrown the next time you press the 'Roll Dice' button. If you decide after the second throw in a turn that you don't want to keep the same dice before the third throw then you can click them again and they will move back to the table and be thrown in the third throw.""")
    if input("Do you want to play the game? y/n")=="y":
        return True
    else:
        print("Bye! :(")
        return False

def Game(state, games_scores):
    while not isFinalState(state):

        if state[0] == 0:
            print("\033[94mYour turn:\033[0m")
            game_name, score = PlayerChoose(games_scores)

        else:

            print("\033[94mComputer's turn:\033[0m")
            game_name, score = ComputerChoose(games_scores)

        if Validation(state, state[0], game_numbers[game_name]):
            state = Transition(state, state[0], game_numbers[game_name], score)


if WelcomeInterface():
    games_scores = InialGame()
    print(Game(InitialState(), games_scores))

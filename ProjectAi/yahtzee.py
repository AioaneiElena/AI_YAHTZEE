import random
import gamescheck
from gamescheck import game_functions


def InitialState():
    return (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
    

def isFinalState(state):
    return all(s == 1 for s in state[:-2])

def InialGame():
    games = [
        "Ones", "Twos", "Threes", "Fours", "Fives",
        "Sixes", "Three of a kind", "Four of a kind", "Full House", "Small Straight",
        "Large Straight", "Chance", "YAHTZEE"
    ]

    games_scores = [[game, -1, -1] for game in games]
    games_scores.append(["Total", 0, 0])
    return games_scores


def RollDice(dices):
    for i in range(len(dices[0])):
        if dices[0][i]==0:
            dices[1][i] = random.randint(1, 6)

def PrintTable(games_scores):
    for game in games_scores:
        print(f"{game[0]} | {game[1]} | {game[2]}")

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

def Transition(state, player, game_number, score):
    state_list = list(state)
    state_list[(player+1)* game_number]=1
    state_list[0]= int(not player)
    print(score)
    print(player) 
    state_list[player+27] += score
    print(tuple(state_list))
    return tuple(state_list)

def Validation(state, player, game_number):
    if state[(player+1)* game_number] == 1:
        return False
    return True

def PlayerChoose(games_scores):
    dices = [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]]
    count = 0 

    while count< 3:
        
        RollDice(dices)
        print("Roll dices: ", dices[1])

        PrintTable(games_scores)

        print("Winning points' games: ")
        PrintWinningPointsGames(dices,games_scores,0)

        response = input("Do you want to select a game? y/n :").strip() 
        if response.lower() == "y":

            game_name = input("Write the name of the game: ").strip() 

            if game_name in game_numbers:
                game_index = game_numbers[game_name]
                score = game_functions[game_name](dices)
                games_scores[game_index][1] = score  

                return game_name, score
                
            else:
                print("Invalid game name. Please try again.")

        else:

            response=input("Choose the dices you want to keep: ")
            dices_to_keep = list(map(int, response.split()))
            for dice in dices_to_keep:
                dices[0][dice]=1
        
    game_name = input("You can't roll dices again. Please choose a game: ").strip() 

    if game_name in game_numbers:
        game_index = game_numbers[game_name]
        score = game_functions[game_name](dices)
        games_scores[game_index][1] = score  

        return game_name, score
        
    else:
        print("Invalid game name. Please try again.")

    

    

def ComputerChoose(games_scores):

    dices = [[0, 0, 0, 0, 0],[0, 0, 0, 0, 0]]
    count =0

    while count < 3:
        RollDice(dices)
        print("Computer rolls: ", dices[1])

        available_games = [game for game in games_scores if game[2] == -1]

        if available_games and random.choice([True, False]):  # 50% șansă
            selected_game = random.choice(available_games)
            game_name = selected_game[0]
            game_index = game_numbers[game_name] - 1

            score = game_functions[game_name](dices)
            games_scores[game_index][2] = score  
            
            print(f"Computer chooses {game_name} and scores {score}")
            return game_name, score
        
        else:
            dices_to_keep = random.sample(range(5), k=random.randint(0, 5)) 
            print(f"Computer keeps dices: {dices_to_keep}")
            for dice in dices_to_keep:
                dices[0][dice] = 1
            count += 1 
        
    selected_game = random.choice(available_games)
    game_name = selected_game[0]
    game_index = game_numbers[game_name] - 1

    score = game_functions[game_name](dices)
    games_scores[game_index][2] = score  
    
    print(f"Computer chooses {game_name} and scores {score}")
    return game_name, score
        


def Game(state, games_scores):
   
    while not isFinalState(state):

        if state[0]==0:
            print("Your turn:")
            game_name, score = PlayerChoose(games_scores)
            
        else:
            
            print("Computer's turn:")
            game_name, score = ComputerChoose(games_scores)

        if Validation(state,state[0],game_numbers[game_name]):
                state = Transition(state, state[0], game_numbers[game_name],score)
            






games_scores=InialGame()
print ( Game(InitialState(),games_scores))


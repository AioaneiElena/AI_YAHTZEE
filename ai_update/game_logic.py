from gamescheck import *
from training_alg import *

bonus_score_p0=0
bonus_score_p1=0
ok_p0=0
ok_p1=0
yahtzee_trainer = YahtzeeTraining()
Q_table = yahtzee_trainer.q_table


def InitialState():
    return (0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)


def InitialGame():
    
    yahtzee_trainer.train(episodes=900000)
    games = [
        "Ones", "Twos", "Threes", "Fours", "Fives",
        "Sixes", "Three of a kind", "Four of a kind", "Full House", "Small Straight",
        "Large Straight", "Chance", "YAHTZEE"
    ]

    games_scores = [[game, -1, -1] for game in games]
    games_scores.append(["Bonus", 0, 0])
    games_scores.append(["Total", 0, 0])
    return games_scores


def isFinalState(state):
   if all(s != -1 for s in state[:]):
       total_p0=total(state,0)
       total_p1=total(state,1)
       print("Player 1 score: ", total_p0)
       print("Player 2 score: ", total_p1)
       if total_p0>total_p1:
           print("Player 1 wins!")
       elif total_p1>total_p0:
           print("Player 2 wins!")
       else:
           print("It's a tie!")
       return True
   return False

def RollDice(dices):
    for i in range(len(dices[0])):
        if dices[0][i] == 0:
            dices[1][i] = random.randint(1, 6)


def PrintTable(games_scores):
    for game in games_scores:
        print(f"{game[0]} | {game[1]} | {game[2]}")


def PrintWinningPointsGames(dices, games_scores, player):
    for game in games_scores:
        if (game[player + 1] == -1):
            score = game_functions[game[0]](dices)
            if (score != 0):
                print(f"{game[0]} : {score}")


def Transition(state, player, game_number, score):
    state_list = list(state)
    state_list[13 * player + game_number] = score
    state_list[0] = int(not player)
    print(tuple(state_list))
    return tuple(state_list)

def Validation(state, player, game_number):
    if state[13 * player + game_number] != -1:
        return False
    return True

def DiceValitation(dices, dices_to_let):
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
        score = game_functions[game_name](dices)
        games_scores[game_index - 1][1] = score
        if game_index <= 6:
            bonus_score_p0 += score
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

def state_to_index(state):
    state_index = int("".join(map(str, state)), 2)
    return state_index

def DetermineHelpfulDices(game_name, dices):
    dices[0] = [0, 0, 0, 0, 0]

    if game_name == "Ones":
        for i in range(5):
            if dices[1][i] == 1:
                dices[0][i] = 1

    elif game_name == "Twos":
        for i in range(5):
            if dices[1][i] == 2:
                dices[0][i] = 1

    elif game_name == "Threes":
        for i in range(5):
            if dices[1][i] == 3:
                dices[0][i] = 1

    elif game_name == "Fours":
        for i in range(5):
            if dices[1][i] == 4:
                dices[0][i] = 1

    elif game_name == "Fives":
        for i in range(5):
            if dices[1][i] == 5:
                dices[0][i] = 1

    elif game_name == "Sixes":
        for i in range(5):
            if dices[1][i] == 6:
                dices[0][i] = 1

    elif game_name == "Three of a kind":
        counts = [dices[1].count(i) for i in range(1, 7)]
        for i in range(5):
            if counts[dices[1][i] - 1] >= 2:
                dices[0][i] = 1

    elif game_name == "Four of a kind":
        counts = [dices[1].count(i) for i in range(1, 7)]
        for i in range(5):
            if counts[dices[1][i] - 1] >= 2:
                dices[0][i] = 1

    elif game_name == "Full House":
        counts = [dices[1].count(i) for i in range(1, 7)] 
        pairs_or_more = [value for value, count in enumerate(counts, start=1) if count >= 2] 

        if len(pairs_or_more) > 0:
            first_pair = pairs_or_more[0]
            for i in range(5):
                if dices[1][i] == first_pair:
                    dices[0][i] = 1

        if len(pairs_or_more) > 1:
            second_pair = pairs_or_more[1]
            for i in range(5):
                if dices[1][i] == second_pair:
                    dices[0][i] = 1


    elif game_name == "Small Straight":
        needed_values_sets = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
        kept_values = set()
        best_sequence = set()
        for needed_values in needed_values_sets:
            current_sequence = needed_values.intersection(dices[1])
            if len(current_sequence) > len(best_sequence):
                best_sequence = current_sequence
        for i in range(5):
            if dices[1][i] in best_sequence and dices[1][i] not in kept_values:
                dices[0][i] = 1
                kept_values.add(dices[1][i])
            else:
                dices[0][i] = 0

 


    elif game_name == "Large Straight":
        needed_values = {1, 2, 3, 4, 5} if 6 not in dices[1] else {2, 3, 4, 5, 6}  
        kept_values = set()  

        for i in range(5):
            if dices[1][i] in needed_values and dices[1][i] not in kept_values:
                dices[0][i] = 1  
                kept_values.add(dices[1][i])  
            else:
                dices[0][i] = 0 



    elif game_name == "YAHTZEE":
        counts = [dices[1].count(i) for i in range(1, 7)]
        for i in range(5):
            if counts[dices[1][i] - 1] >= 3:
                dices[0][i] = 1

    print(f"Updated kept dices for {game_name}: {dices[0]}")

def total(state, player):
    sum_player = 0

    if player == 0:
        for i in range(1,14):
            sum_player = sum_player+state[i]
    else:
        for i in range(14,27):
            sum_player = sum_player+state[i]

    return sum_player

def ComputerChooseAI(games_scores):
    
    count = 0
    dices = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    selected_game = None  

    games_played = [0 if game[2] == -1 else 1 for game in games_scores[:13]]

    while count < 3:
       
        RollDice(dices) 
        dices_state= yahtzee_trainer.initialize_state(dices[1])
        print(f"Computer rolls: {dices[1]}")

        if count == 0:
            available_games = [game for game in games_scores[:13] if game[2] == -1]
            if available_games:
                selected_game=yahtzee_trainer.choose_action(dices_state)
                print(f"HELLLLLLOOOO SELECTED GAME IS: {selected_game}")
                
                games_not_disponible = []

                while games_played[selected_game] != 0:
                    games_not_disponible.append(selected_game)
                    selected_game = yahtzee_trainer.choose_next_action(dices_state, games_not_disponible)
                    print(f"Selected game (post-adjustment): {selected_game}")

                selected_game+=1
                game_name = index_to_game_name[selected_game]


                

                print(f"Computer chooses the game {game_name} based on Q-table.")
                DetermineHelpfulDices(game_name, dices) 
                if all(die == 1 for die in dices[0]):
                    count = 3
                

        else:

            DetermineHelpfulDices(game_name, dices)
            if all(die == 1 for die in dices[0]):
                    count = 3
            else:
                print(f"Computer continues with kept dices for {game_name}: {dices[0]}")

        count += 1

    game_name,
    score = UpdateScore(1, game_name, dices)
    print(f"Computer finalizes the game {game_name} and scores {score}")
    return game_name, score



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
            while not DiceValitation(dices, dices_to_let):
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



def Game(state, games_scores):
    while not isFinalState(state):

        if state[0] == 0:
            print("Your turn:")
            game_name, score = PlayerChoose(games_scores)

        else:

            print("Computer's turn:")
            game_name, score = ComputerChooseAI(games_scores)

        if Validation(state, state[0], game_numbers[game_name]):
            state = Transition(state, state[0], game_numbers[game_name], score)



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


if WelcomeInterface():
    games_scores = InitialGame()
    print(Game(InitialState(), games_scores))



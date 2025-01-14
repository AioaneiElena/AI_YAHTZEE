from gamescheck import *
from training_alg import *
import tkinter as tk
import random


bonus_score_p0=0
bonus_score_p1=0
ok_p0=0
ok_p1=0
yahtzee_trainer = YahtzeeTraining()
Q_table = yahtzee_trainer.q_table



# Creează fereastra principală
root = tk.Tk()
root.title("YAHTZEE")

# Dimensiuni pentru fereastră
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 650

# Configurează dimensiunile și culoarea de fundal
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.configure(bg="green")

# Creează un Frame pentru tabel și margine neagră
table_frame = tk.Frame(
    root,
    bg="black"  # Fundal negru pentru margini
)
table_frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Creează un Frame pentru personaje
characters_frame = tk.Frame(
    root,
    bg="green"  # Fundal verde
)
characters_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)

# Funcție pentru desenarea unui zar
def draw_dice(frame, value):
    
    # Șterge zarurile existente
    for widget in dice_frame.winfo_children():
        widget.destroy()

    size = 50  # Dimensiunea zarului
    margin = 5  # Marginea internă
    dot_size = 10  # Dimensiunea bulinuțelor

    canvas = tk.Canvas(frame, width=size, height=size, bg="red", highlightthickness=0)
    canvas.pack(side=tk.LEFT, padx=5)

    positions = {
        1: [(25, 25)],
        2: [(10, 10), (40, 40)],
        3: [(10, 10), (25, 25), (40, 40)],
        4: [(10, 10), (10, 40), (40, 10), (40, 40)],
        5: [(10, 10), (10, 40), (40, 10), (40, 40), (25, 25)],
        6: [(10, 10), (10, 25), (10, 40), (40, 10), (40, 25), (40, 40)],
    }

    # Desenează bulinuțele
    for x, y in positions[value]:
        canvas.create_oval(
            x - dot_size // 2,
            y - dot_size // 2,
            x + dot_size // 2,
            y + dot_size // 2,
            fill="white"
        )
def display_characters(frame):
    # Adaugă un padding stânga pentru a muta personajele spre dreapta
    padding_left = 180  # Spațiu suplimentar

    # Personajul Player 2 (partea de sus)
    player2_frame = tk.Frame(frame, bg="green")
    player2_frame.pack(side=tk.TOP, pady=(5, 5), padx=(padding_left, 0))  # Adaugă padding stânga

    player2_label = tk.Label(
        player2_frame,
        text="😎",  # Reprezentare simplă a personajului
        bg="green",
        fg="white",
        font=("Arial", 45)
    )
    player2_label.pack(anchor="center")  # Centrare pe orizontală

    player2_text = tk.Label(
        player2_frame,
        text="Player 2",
        bg="green",
        fg="white",
        font=("Arial", 14, "bold")
    )
    player2_text.pack(anchor="center")  # Centrare pe orizontală

    # Spacer pentru separare
    spacer = tk.Frame(frame, height=200, bg="green")  # Înălțimea poate fi ajustată
    spacer.pack()


    # Personajul Player 1 (partea de jos)
    player1_frame = tk.Frame(frame, bg="green")
    player1_frame.pack(side=tk.BOTTOM, pady=(10,10), padx=(padding_left, 0))  # Adaugă padding stânga

    # Etichetă pentru mesajul "Choose a game!"
    global message_label
    message_label = tk.Label(
        player1_frame,
        text="",
        bg="green",
        fg="yellow",
        font=("Arial", 14, "bold")
    )
    message_label.pack()
    # Zarurile vor fi afișate aici când butonul este apăsat
    global dice_frame
    dice_frame = tk.Frame(player1_frame, bg="green", width=300, height=70)
    dice_frame.pack(side=tk.TOP, pady=(5, 10))
    dice_frame.pack_propagate(False)  # Previne propagarea dimensiunilor

    # Contor pentru numărul de apăsări
    roll_counter = tk.IntVar(value=0)

    def switch_dice():
        # Șterge zarurile de la Player 1
        for widget in dice_frame.winfo_children():
            widget.destroy()

        # Creează zarurile pentru Player 2
        player2_dice_frame = tk.Frame(player2_frame, bg="green", width=300, height=70)
        player2_dice_frame.pack(side=tk.TOP, pady=(5, 10))
        player2_dice_frame.pack_propagate(False)  # Previne propagarea dimensiunilor

        for _ in range(5):
            dice_value = random.randint(1, 6)  # Valoare zar între 1 și 6
            draw_dice(player2_dice_frame, dice_value)

    # Butonul pentru dat cu zarurile
    roll_button = tk.Button(
        player1_frame,
        text="Roll dices",
        bg="white",
        fg="black",
        font=("Arial", 14, "bold"),
        command=RollDice
    )
    roll_button.pack(side=tk.TOP, pady=(5, 10))

    player1_label = tk.Label(
        player1_frame,
        text="🙂",  # Reprezentare simplă a personajului
        bg="green",
        fg="white",
        font=("Arial", 45)
    )
    player1_label.pack(anchor="center")  # Centrare pe orizontală

    player1_text = tk.Label(
        player1_frame,
        text="Player 1",
        bg="green",
        fg="white",
        font=("Arial", 14, "bold")
    )
    player1_text.pack(anchor="center")  # Centrare pe orizontală

# Funcție pentru a afișa tabelul cu casete
def display_table(frame, scores):
    # Creează antetul tabelului
    headers = ["Game", "Player 1", "Player 2"]
    for col, header in enumerate(headers):
        label = tk.Label(
            frame,
            text=header,
            bg="white",
            fg="black",
            height=2,
            borderwidth=1,
            relief="solid"  # Bordură solidă
        )
        label.grid(row=0, column=col, sticky="nsew")

    # Configurarea lățimii coloanelor 2 și 3
    frame.grid_columnconfigure(1, weight=1, minsize=60)  # Coloana 2 (Player 1)
    frame.grid_columnconfigure(2, weight=1, minsize=60)  # Coloana 3 (Player 2)
    frame.grid_columnconfigure(0, weight=1, minsize=120)  # Coloana 1 (Game)

    # Adaugă fiecare rând din scoruri în tabel
    for row, game in enumerate(scores, start=1):
        for col, value in enumerate(game):
            label = tk.Label(
                frame,
                text=str(value),
                bg="white",
                fg="black",
                height=2,
                borderwidth=1,
                relief="solid"  # Bordură solidă
            )
            label.grid(row=row, column=col, sticky="nsew")


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

        
    display_characters(characters_frame)
    display_table(table_frame, games_scores)
    return games_scores


def isFinalState(state):  #completare cu functie care printeaza interfata finala (castigator)
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


def WelcomeGame(games_scores):
        
    

    # Pornește bucla principală a interfeței
    root.mainloop()



if __name__ == "__main__":
   
    games_scores = InitialGame()
    WelcomeGame(games_scores)
    print(Game(InitialState(), games_scores))


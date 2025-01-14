import tkinter as tk
import random

# Exemplu de scoruri pentru a popula tabelul
games_scores = [
    ["Ones", -1, -1],
    ["Twos", -1, -1],
    ["Threes", -1, -1],
    ["Fours", -1, -1],
    ["Fives", -1, -1],
    ["Sixes", -1, -1],
    ["Three of a kind", -1, -1],
    ["Four of a kind", -1, -1],
    ["Full House", -1, -1],
    ["Small Straight", -1, -1],
    ["Large Straight", -1, -1],
    ["Chance", -1, -1],
    ["YAHTZEE", -1, -1],
    ["Bonus", 0, 0],
    ["Total", 0, 0],
]

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

# Funcție pentru afișarea personajelor
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

    def roll_dices():
        # Actualizează contorul
        roll_counter.set(roll_counter.get() + 1)

        # Dacă s-au făcut trei ture, afișează mesajul și dezactivează butonul
        if roll_counter.get() > 3:
            message_label.config(text="Choose a game!")
            roll_button.config(state=tk.DISABLED)
            # După 3 secunde, schimbă zarurile de la Player 1 la Player 2
            root.after(3000, switch_dice)  # După 3 secunde (3000 ms)
            return

        # Șterge zarurile existente
        for widget in dice_frame.winfo_children():
            widget.destroy()

        # Generează și afișează cinci zaruri
        for _ in range(5):
            dice_value = random.randint(1, 6)  # Valoare zar între 1 și 6
            draw_dice(dice_frame, dice_value)

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
        command=roll_dices
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

# Afișează personajele și tabelul
display_characters(characters_frame)
display_table(table_frame, games_scores)

# Pornește bucla principală a interfeței
root.mainloop()

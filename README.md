# 🎲 Yahtzee AI – Smart Dice Game with Q-Learning & Chat Assistant

**Yahtzee AI** is a Python-based desktop game that brings the classic Yahtzee experience to life with a modern twist: a built-in AI opponent trained via Q-learning. The game supports 1v1 gameplay, Player vs AI, personalized move recommendations, user statistics, and an interactive chatbot that teaches the rules and strategies of Yahtzee.

---
This project was developed as part of an academic assignment at the Faculty of Computer Science,
"Alexandru Ioan Cuza" University of Iași.

Collaborative project by:

🧑‍💻 Elena Aioanei

👩‍💻 Ana Petrașuc

## 🚀 Features

- 🎮 Play against another player or an AI opponent trained with Q-learning  
- 🧠 The AI uses a trained Q-table to choose optimal actions based on game state  
- 💬 Integrated chatbot that explains game rules, scoring combinations, and strategies  
- 💡 Personalized HINT system suggests the best move based on your current dice  
- 📊 Game statistics stored in a local JSON file (scores, averages, progress)  
- 🪟 Graphical interface built with `tkinter` – simple, responsive, and interactive

---

## 🧠 AI Training (Q-Learning)

The AI agent is trained using a classical **Q-learning** algorithm, with the following parameters:

- State space: all combinations of dice rolls (5 dice × 6 sides)  
- Action space: 13 scoring categories  
- Reward: based on normalized expected score for each action  
- Exploration: epsilon-greedy strategy with decay  
- Training: ~900,000 simulated episodes before gameplay

---

## 🛠️ Technologies Used

- 🐍 Python 3.11  
- 🎲 `tkinter` for GUI  
- 📚 `numpy`, `itertools`, `json`, `random` for logic and simulation  
- 🧠 Custom Q-table implementation (no external RL libraries)  

---

## 📦 Installation

To run the game locally:

### 1. Clone the repository
```bash
git clone https://github.com/username/yahtzee-ai.git
cd yahtzee-ai
```

### 2. Run the game
Make sure you have Python 3.10+ installed, then run:
```bash
python main.py
```
## Photos
<img width="1218" height="600" alt="Screenshot 2025-07-17 025400" src="https://github.com/user-attachments/assets/6c817df5-7988-447d-9962-1f9fa0e2191f" />
<img width="1219" height="595" alt="Screenshot 2025-07-17 025414" src="https://github.com/user-attachments/assets/425bf4fd-5eb6-4f09-87c0-26c83ac5d517" />
<img width="1216" height="600" alt="Screenshot 2025-07-17 025407" src="https://github.com/user-attachments/assets/c083172e-93c7-4e0f-9161-94c7b3a6d52c" />
<img width="1218" height="625" alt="Screenshot 2025-07-17 025427" src="https://github.com/user-attachments/assets/817df476-33c3-428f-9d8f-0b9347df5a09" />


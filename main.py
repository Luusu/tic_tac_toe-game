import random
from tkinter import *
from PIL import Image, ImageTk

# --- Global Setup ---
user = 1
players = 1
board = [0] * 9
positions = [(80, 100), (200, 100), (320, 100),
             (80, 220), (200, 220), (320, 220),
             (80, 340), (200, 340), (320, 340)]
buttons = []
images = {}

# --- Initialize Tkinter Window ---
root = Tk()
root.title("Tic Tac Toe")
root.geometry("500x500")
root.resizable(False, False)

# --- Load Images ---
images['wood'] = ImageTk.PhotoImage(Image.open("imgs/wood.jpg"))
images['circle'] = ImageTk.PhotoImage(Image.open("imgs/circle.jpg"))
images['cross'] = ImageTk.PhotoImage(Image.open("imgs/cross.jpg"))
images['white'] = ImageTk.PhotoImage(Image.open("imgs/white.jpg"))

# --- UI Frames ---
main_frame = Frame(root)
select_frame = Frame(root)
canvas = Canvas(select_frame, width=500, height=500)
canvas.create_image(0, 0, anchor=NW, image=images['wood'])
canvas.pack()

# --- Turn Display ---
turn_label = Label(main_frame, text="User 1's turn", font=("bold", 15), bg="brown", fg="yellow")
turn_label.place(x=200, y=60)

# --- Game Control Functions ---
def update_turn_label():
    turn_label.config(text=f"User {user}'s turn", fg="yellow" if user == 1 else "#5feb38")

def disable_all_buttons():
    for btn in buttons:
        btn.config(state=DISABLED)

def check_winner():
    wins = [(0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != 0:
            return board[a]
    return 0

def end_game(winner):
    disable_all_buttons()
    msg = f"!! Congrats User {winner} won the match !!"
    Label(root, text="Match Finished", font=("bold", 15), fg="#5feb38", bg="brown").place(x=150, y=60)
    Label(root, text=msg, font=("bold", 15), fg="red", bg="#b6ff69", width=44).place(x=5, y=460)
    Button(root, text="ReMatch", command=rematch, bg="#ff2e2e", fg="white", font=("bold", 20)).place(x=100, y=240)
    Button(root, text="Exit", command=root.quit, bg="#ff2e2e", fg="white", font=("bold", 20)).place(x=270, y=240)

def clicked(pos):
    global user
    if board[pos] != 0:
        return
    board[pos] = user
    buttons[pos].config(image=images['circle' if user == 1 else 'cross'], state=DISABLED)

    winner = check_winner()
    if winner:
        end_game(winner)
        return

    if all(board):
        Label(root, text="It's a Draw!", font=("bold", 15), fg="blue").place(x=150, y=460)
        return

    user = 2 if user == 1 else 1
    update_turn_label()

    if players == 1 and user == 2:
        root.after(500, ai_move)

def ai_move():
    empty = [i for i in range(9) if board[i] == 0]
    if not empty:
        return
    pos = random.choice(empty)
    clicked(pos)

def rematch():
    global board, user
    board = [0] * 9
    user = 1
    update_turn_label()
    for i, btn in enumerate(buttons):
        btn.config(state=NORMAL, image=images['white'])
    for widget in root.place_slaves():
        if isinstance(widget, Label) and ("Congrats" in widget.cget("text") or "Draw" in widget.cget("text")):
            widget.destroy()

def start_game(mode):
    global players
    players = mode
    select_frame.pack_forget()
    main_frame.pack()
    update_turn_label()

# --- Mode Selection ---
Label(select_frame, text="Select The Mode", font=("bold", 18), fg="red").place(x=90, y=10)
Button(select_frame, text="User Vs User", font=("bold", 20), bg="blue", fg="yellow",
       command=lambda: start_game(2)).place(x=50, y=150)
Button(select_frame, text="User Vs Computer", font=("bold", 20), bg="blue", fg="yellow",
       command=lambda: start_game(1)).place(x=50, y=330)
select_frame.pack()

# --- Game Board Setup ---
Label(main_frame, text="Tic Tac Toe", font=("bold", 20)).place(x=90, y=10)
canvas_main = Canvas(main_frame, width=500, height=500)
canvas_main.create_image(0, 0, anchor=NW, image=images['wood'])
canvas_main.pack()

for i in range(9):
    x, y = positions[i]
    btn = Button(main_frame, image=images['white'], width=110, height=110, bg="white",
                 command=lambda i=i: clicked(i))
    btn.place(x=x, y=y)
    buttons.append(btn)

root.mainloop()

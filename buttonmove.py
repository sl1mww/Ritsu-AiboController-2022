from curses import BUTTON2_CLICKED
from tkinter import *

root = Tk()
root.title("Move Hana!")

def button_move():
    return

button_w = Button(root, text="W", padx=30, pady=20, command=button_move)
button_s = Button(root, text="S", padx=30, pady=20, command=button_move)
button_a = Button(root, text="A", padx=30, pady=20, command=button_move)
button_d = Button(root, text="D", padx=30, pady=20, command=button_move)

button_w.grid(row=1, column=2)
button_s.grid(row=2, column=2)
button_a.grid(row=2, column=1)
button_d.grid(row=2, column=3)

root.mainloop()
import tkinter as tk
from tkinter import font

root = tk.Tk()

# List all available fonts
print(font.families())

# Use Hagrid Bold
label = tk.Label(root, text="Hello with Hagrid Bold!", font=("Hagrid Text Trial ", 20))
label.pack()

root.mainloop()

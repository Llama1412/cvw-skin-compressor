import tkinter as tk
from tkinter import filedialog, StringVar

from hasher import execute


def get_fields():
    print("Base Path: {}\nPrefix: {}".format(base_skin.get(), prefix.get()))
    execute(base_skin.get(), prefix.get())


def browse(which):
    if which == "base":
        folder_name = filedialog.askdirectory(title="Select Base Skin Directory")
        b_string.set(folder_name)


master = tk.Tk()
tk.Label(master, text="Base Skin").grid(row=0)
tk.Label(master, text="Prefix").grid(row=1)

b_string = StringVar()
p_string = StringVar()
base_skin = tk.Entry(master, textvariable=b_string)
prefix = tk.Entry(master, textvariable=p_string)

base_skin.grid(row=0, column=1)
prefix.grid(row=1, column=1)

button_base_skin = tk.Button(master, text="📁", command=lambda: browse("base"))
button_base_skin.grid(row=0, column=2)

tk.Button(master, text='Submit', command=get_fields).grid(row=3, column=1, sticky=tk.W, pady=4)

tk.mainloop()

#!/usr/bin/env python3

from math import pi, sin
from os.path import basename, splitext
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class About(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, class_=parent.name)
        self.config()

        btn = tk.Button(self, text="Konec", command=self.close)
        btn.pack()

    def close(self):
        self.destroy()


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "Foo"

    def __init__(self):
        super().__init__(className=self.name)

        self.func = tk.StringVar()

        self.title(self.name)

        self.func_frame = tk.LabelFrame(self, text="Graf z funkce")
        self.sin = tk.Radiobutton(
            self.func_frame, text="sin", variable=self.func, value="sin"
        )
        self.log = tk.Radiobutton(
            self.func_frame, text="log", variable=self.func, value="log"
        )
        self.exp = tk.Radiobutton(
            self.func_frame, text="exp", variable=self.func, value="exp"
        )
        self.start = MyEntry(self.func_frame)
        self.end = MyEntry(self.func_frame)

        self.sin.grid(row=0)
        self.log.grid(row=1)
        self.exp.grid(row=2)
        self.start.grid(row=0, column=1)
        self.end.grid(row=1, column=1)
        self.func_frame.grid()

        self.file_frame = tk.LabelFrame(self, text="Graf ze souboru")
        self.file_name = tk.Entry(self.file_frame)
        self.file_select = tk.Button(self.file_frame, text="Vybrat soubor")

        self.file_name.grid()
        self.file_select.grid(row=1)
        self.file_frame.grid(row=1)

    def _draw(self):
        self.draw_frame = tk.LabelFrame(self, text="Vykreslit graf")

    def about(self):
        window = About(self)
        window.grab_set()

    def quit(self, event=None):
        super().quit()


x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()

app = Application()
app.mainloop()

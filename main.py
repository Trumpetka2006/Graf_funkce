#!/usr/bin/env python3

from os.path import basename, splitext
from pydoc import importfile, text
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import re

from tkinter import ttk, N, E, S, W, messagebox


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
        self.x_name = tk.Entry()
        self.y_name = tk.Entry()

        self.val_f_tupple = (self.register(self.validate), "%P")

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
        self.start = MyEntry(
            self.func_frame, validate="all", validatecommand=self.val_f_tupple
        )
        self.end = MyEntry(
            self.func_frame, validate="all", validatecommand=self.val_f_tupple
        )

        self.sin.grid(row=0)
        self.log.grid(row=1)
        self.exp.grid(row=2)
        self.start.grid(row=0, column=1)
        self.end.grid(row=1, column=1)
        self.func_frame.grid()

        self.file_frame = tk.LabelFrame(self, text="Graf ze souboru")
        self.file_name = tk.Entry(self.file_frame)
        self.file_select = tk.Button(self.file_frame, text="Vybrat soubor")

        self.file_name.grid(sticky=E + W)
        self.file_select.grid(row=1, sticky=E + W)
        self.file_frame.grid(row=1, sticky=E + W)

        self._axes().grid(row=2, column=0, sticky=E + W)

        self._draw().grid(row=0, column=1, columnspan=2, sticky=N + S + E + W)

    def _draw(self):
        draw_frame = tk.LabelFrame(self, text="Vykreslit graf")
        draw_func = tk.Button(
            draw_frame, text="Vykreslit z funkce", command=self.func_calc
        )
        draw_file = tk.Button(draw_frame, text="Vykreslit ze souboru")

        draw_func.grid(sticky=W + E)
        draw_file.grid(row=1, sticky=W + E)
        return draw_frame

    def _axes(self):
        axes_frame = tk.LabelFrame(self, text="Název os")
        x_lb = tk.Label(axes_frame, text="Osa X:")
        self.x_name = tk.Entry(axes_frame)
        y_lb = tk.Label(axes_frame, text="Osa Y:")
        self.y_name = tk.Entry(axes_frame)

        x_lb.grid()
        self.x_name.grid(row=0, column=1)
        y_lb.grid(row=1)
        self.y_name.grid(row=1, column=1)
        return axes_frame

    def func_calc(self):
        funcs = {"sin": np.sin, "log": np.log, "exp": np.exp}
        try:
            start = int(self.start.get())
            end = int(self.end.get())
        except ValueError:
            self.warning("Nebyl zadán platný rozsah!")
            return
        if end < start:
            self.warning("Start musí být menší než End! ")
            return
        if self.func.get() not in ["sin", "log", "exp"]:
            self.warning("Nebyla vybrána funkce")
            return
        print("succes")
        x = np.linspace(start, end, 200)
        y = funcs[self.func.get()](x)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        plt.show()

    def validate(self, P: str):
        return bool(re.match(r"^-?\d*$", P))

    def warning(self, message: str):
        messagebox.showerror(title="Chyba!", message=message)

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

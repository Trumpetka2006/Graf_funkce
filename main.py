#!/usr/bin/env python3

from logging import warning
import os
from os.path import basename, exists, splitext
from pydoc import importfile, text
from textwrap import fill
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import re

from tkinter import END, ttk, N, E, S, W, messagebox, filedialog


class MyEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.placeholder = placeholder
        self.placeholder_color = "gray"
        self.normal_color = self["fg"]

        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)

        self._on_focus_out()
        self.configure(fg=self.placeholder_color)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    def _on_focus_out(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)

    def _on_focus_in(self, event=None):
        if self.get() == self.placeholder:
            self.delete(0, END)
            self.configure(fg=self.normal_color)

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
    name = "Graf funkce"

    def __init__(self):
        super().__init__(className=self.name)

        self.func = tk.StringVar()
        self.x_name = tk.Entry()
        self.y_name = tk.Entry()
        self.file_path = tk.StringVar()

        self.plot_start = tk.StringVar(value="START")
        self.plot_end = tk.StringVar(value="END")

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
            self.func_frame,
            validate="all",
            validatecommand=self.val_f_tupple,
            textvariable=self.plot_start,
            placeholder="START",
        )
        self.end = MyEntry(
            self.func_frame,
            validate="all",
            validatecommand=self.val_f_tupple,
            textvariable=self.plot_end,
            placeholder="END",
        )

        self.sin.grid(row=0)
        self.log.grid(row=1)
        self.exp.grid(row=2)
        self.start.grid(row=0, column=1)
        self.end.grid(row=1, column=1)
        self.func_frame.grid()

        self.file_frame = tk.LabelFrame(self, text="Graf ze souboru")
        self.file_name = tk.Entry(
            self.file_frame, state="readonly", textvariable=self.file_path
        )
        self.file_select = tk.Button(
            self.file_frame, text="Vybrat soubor", command=self.open_file
        )

        self.file_name.pack(fill="x")
        self.file_select.pack(fill="x")
        self.file_frame.grid(row=1, sticky=E + W)

        self._axes().grid(row=2, column=0, sticky=E + W)

        self._draw().grid(row=0, column=1, columnspan=2, sticky=N + S + E + W)

    def _draw(self):
        draw_frame = tk.LabelFrame(self, text="Vykreslit graf")
        draw_func = tk.Button(
            draw_frame, text="Vykreslit z funkce", command=self.func_calc
        )
        draw_file = tk.Button(
            draw_frame, text="Vykreslit ze souboru", command=self.file_calc
        )

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

    def name_axes(self):
        plt.xlabel("Osa X")
        plt.ylabel("Osa Y")

        if self.x_name.get() != "":
            plt.xlabel(self.x_name.get())
        if self.y_name.get() != "":
            plt.ylabel(self.y_name.get())

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
        x = np.linspace(start, end, 200)
        y = funcs[self.func.get()](x)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        self.name_axes()
        plt.show()

    def file_calc(self):
        if not exists(self.file_path.get()):
            self.warning("Soubor neexistuje")
            return
        x = []
        y = []
        with open(self.file_path.get(), "r") as file:
            while True:
                line = file.readline()
                if line == "":
                    break
                num = line.split()
                try:
                    x.append(float(num[0]))
                    y.append(float(num[1]))
                except ValueError:
                    self.warning("Neznámý formát souboru!")
                    return
            file.close()
        fig, ax = plt.subplots()
        ax.plot(x, y)
        self.name_axes()
        plt.show()

    def validate(self, P: str):
        return bool(re.match(r"^-?\d*$", P))

    def warning(self, message: str):
        messagebox.showerror(title="Chyba!", message=message)

    def open_file(self):
        self.file_path.set(filedialog.askopenfilename())

    def about(self):
        window = About(self)
        window.grab_set()

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()

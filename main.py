import tkinter as tk
from tkinter import ttk
import random

from finish_card import finalize_card_styling


def change_val(var, delta):
    new_val = var.get() + delta
    if new_val >= 0:
        var.set(new_val)


class StreamDiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DM's Dice Stream")
        self.root.geometry("900x700")

        self.dice_types = [4, 6, 8, 10, 12, 20, 100]
        self.dice_vars = {}
        self.total_sum = 0

        style = ttk.Style()
        style.configure("Big.TButton", font=("Segoe UI", 12, "bold"))
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("TRadiobutton", font=("Segoe UI", 10))

        # top section / results screen
        self.stage_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief="sunken")
        self.stage_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # total banner
        self.total_banner_frame = tk.Frame(self.stage_frame, bg="#333", height=60)
        self.total_banner_frame.pack(side=tk.TOP, fill=tk.X)
        self.total_banner_frame.pack_propagate(False)

        self.total_label = tk.Label(self.total_banner_frame, text="READY", font=("Segoe UI", 20, "bold"), fg="white", bg="#333")
        self.total_label.pack(expand=True)

        # dice container
        self.results_inner = tk.Frame(self.stage_frame, bg="#f0f0f0")
        self.results_inner.place(relx=0.5, rely=0.55, anchor="center")

        control_frame = ttk.Frame(root, padding="15")
        control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # daisy me rolling
        mode_frame = ttk.Frame(control_frame)
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        self.roll_mode = tk.StringVar(value="Normal")
        modes = ["Normal", "Advantage", "Disadvantage"]

        radio_container = ttk.Frame(mode_frame)
        radio_container.pack(anchor="center")

        # makes the mode buttons
        for m in modes:
            ttk.Radiobutton(radio_container, text=m, variable=self.roll_mode, value=m).pack(side=tk.LEFT, padx=20)

        # dice inputs
        dice_row_frame = ttk.Frame(control_frame)
        dice_row_frame.pack(fill=tk.X, pady=10)
        dice_row_frame.columnconfigure(tuple(range(7)), weight=1)

        for idx, sides in enumerate(self.dice_types):
            self.create_die_control(dice_row_frame, sides, idx)

        # THEY HATING
        roll_btn = ttk.Button(control_frame, text="ROLL DICE", style="Big.TButton", command=self.roll_dice)
        roll_btn.pack(fill=tk.X, pady=(15, 5), ipady=5)

    def create_die_control(self, parent, sides, col_idx):
        container = ttk.Frame(parent)
        container.grid(row=0, column=col_idx, sticky="ew")

        lbl = ttk.Label(container, text=f"d{sides}", font=("Segoe UI", 11, "bold"))
        lbl.pack(anchor="center")

        input_row = ttk.Frame(container)
        input_row.pack(anchor="center", pady=5)

        var = tk.IntVar(value=0)
        self.dice_vars[sides] = var

        btn_minus = ttk.Button(input_row, text="-", width=3, command=lambda: change_val(var, -1))
        btn_minus.pack(side=tk.LEFT)

        entry = ttk.Entry(input_row, textvariable=var, width=4, justify='center', font=("Segoe UI", 11))
        entry.pack(side=tk.LEFT, padx=2)

        btn_plus = ttk.Button(input_row, text="+", width=3, command=lambda: change_val(var, 1))
        btn_plus.pack(side=tk.LEFT)

    def roll_dice(self):
        for widget in self.results_inner.winfo_children():
            widget.destroy()
        self.total_sum = 0

        mode = self.roll_mode.get()
        dice_to_roll = []

        for sides in self.dice_types:
            qty = self.dice_vars[sides].get()
            for _ in range(qty):
                dice_to_roll.append(sides)

        if not dice_to_roll:
            self.total_label.config(text="SELECT DICE FIRST", fg="#ffcc00")
            return

        max_cols = 5 if len(dice_to_roll) > 5 else len(dice_to_roll)
        row_val = 0
        col_val = 0

        for sides in dice_to_roll:
            # see maggda its random it just picks a random number it is NOT rigged
            r1 = random.randint(1, sides)
            r2 = random.randint(1, sides)

            if mode == "Normal":
                kept = r1
            elif mode == "Advantage":
                kept = max(r1, r2)
            elif mode == "Disadvantage":
                kept = min(r1, r2)

            self.total_sum += kept
            self.create_visual_card(self.results_inner, sides, r1, r2, mode, row_val, col_val)

            col_val += 1
            if col_val >= max_cols:
                col_val = 0
                row_val += 1

    def perform_roll_animation(self, label_widget, card_frame, sides, r1, r2, mode, steps_remaining):
        # use recursion to update cards
        # calls finish_card when done
        if steps_remaining > 0:
            random_val = random.randint(1, sides)
            label_widget.config(text=str(random_val).zfill(len(str(sides))), fg="black")

            # very dramatic yes yes if almost done
            delay = 50 if steps_remaining > 3 else 200

            # longest line known to man
            self.root.after(delay, lambda: self.perform_roll_animation(
                label_widget, card_frame, sides, r1, r2, mode, steps_remaining - 1
            ))
        else:
            finalize_card_styling(card_frame, sides, r1, r2, mode)

    def create_visual_card(self, parent, sides, r1, r2, mode, r, c):
        # fuck trying to animate adv mode
        card = tk.Frame(parent, bg="white", bd=2, relief="raised", padx=10, pady=5)
        card.grid(row=r, column=c, padx=8, pady=8)

        card.header_label = tk.Label(card, text=f"d{sides}", bg="white", fg="black", font=("Segoe UI", 10))
        card.header_label.pack(side=tk.TOP)  # toplevel leel

        card.effect_label = tk.Label(card, text="", bg="white", fg="white", font=("Segoe UI", 1, "bold"))
        card.effect_label.pack(side=tk.TOP)

        nums_frame = tk.Frame(card, bg="white")
        nums_frame.pack(side=tk.TOP, pady=2)
        card.nums_frame = nums_frame

        f_style = ("Segoe UI", 24, "bold")

        if mode == "Normal":
            lbl = tk.Label(nums_frame, text="?", font=f_style, fg="black", bg="white")
            lbl.pack()
            self.perform_roll_animation(lbl, card, sides, r1, r2, mode, steps_remaining=10)
            self.total_label.config(text=f"TOTAL: {self.total_sum}", fg="white")
        else:
            finalize_card_styling(card, sides, r1, r2, mode)
            self.total_label.config(text=f"TOTAL: {self.total_sum}", fg="white")


if __name__ == "__main__":
    root = tk.Tk()
    app = StreamDiceApp(root)
    root.mainloop()

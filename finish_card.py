import tkinter as tk

def finalize_card_styling(card, sides, r1, r2, mode):
    for widget in card.nums_frame.winfo_children():
        widget.destroy()

    if mode == "Normal":
        kept, dropped = r1, None
    elif mode == "Advantage":
        kept, dropped = max(r1, r2), min(r1, r2)
    elif mode == "Disadvantage":
        kept, dropped = min(r1, r2), max(r1, r2)

    # --- colours ---
    BG_GOLD = "#FFD700"
    BG_RED = "#8B0000"
    BG_BLACK = "#000000"
    BG_LIGHT_BLUE = "#b3e5fc"
    BG_WHITE = "white"
    BG_PINK = "#FF00A6"
    BG_DOUBLE_CRIT = "#4813b0"

    FG_WHITE = "white"
    FG_BLACK = "black"
    FG_GREEN = "#2e7d32"
    FG_RED = "#c62828"
    FG_GREY = "#bdbdbd"
    FG_GREY_LIGHT = "#cfd8dc"

    bg_color = BG_WHITE
    fg_primary = FG_BLACK
    fg_secondary = FG_GREY
    effect_text = ""

    def fg_colour_picker():
        if mode == "Advantage":
            return FG_GREEN
        elif mode == "Disadvantage":
            return FG_RED
        else:
            return FG_BLACK
    if sides == 20:
        if (mode == "Advantage" and kept == 1) or (mode == "Disadvantage" and dropped == 1):
            bg_color = BG_BLACK
            fg_primary = FG_WHITE
            fg_secondary = FG_GREY_LIGHT
            effect_text = "unlucky..."
        elif kept == 20 and dropped == 20:
            bg_color = BG_DOUBLE_CRIT
            fg_primary = fg_colour_picker()
            fg_secondary = fg_colour_picker()
            effect_text = "DOUBLE CRIT!!!"
        elif (kept == 20 and dropped == 1) or (kept == 1 and dropped == 20):
            bg_color = BG_PINK
            fg_primary = fg_colour_picker()
            fg_secondary = "white"
            effect_text = "no words..."
        elif mode == "Advantage" and dropped == 1 and kept != 20:
            bg_color = BG_LIGHT_BLUE
            fg_primary = FG_GREEN
            effect_text = "saved"
        elif kept == 20:
            bg_color = BG_GOLD
            fg_primary = fg_colour_picker()
            effect_text = "critical!"
        elif kept == 1:
            bg_color = BG_RED
            fg_primary = FG_WHITE
            fg_secondary = FG_GREY_LIGHT

    if bg_color == BG_WHITE:
        fg_primary = fg_colour_picker()

    card.config(bg=bg_color)

    header_fg = FG_WHITE if bg_color in [BG_RED, BG_BLACK, BG_DOUBLE_CRIT] else FG_BLACK
    card.header_label.config(bg=bg_color, fg=header_fg)

    if effect_text:
        card.effect_label.config(text=effect_text, bg=bg_color, fg=header_fg, font=("Segoe UI", 8, "bold"))
        card.effect_label.pack(side=tk.TOP)
    else:
        card.effect_label.pack_forget()

    card.nums_frame.config(bg=bg_color)

    f_kept_style = ("Segoe UI", 24, "bold")
    f_drop_style = ("Segoe UI", 16)

    if mode == "Normal":
        tk.Label(card.nums_frame, text=str(r1).zfill(len(str(sides))), font=f_kept_style, fg=fg_primary, bg=bg_color).pack()
    else:
        c1 = fg_primary if r1 == kept else fg_secondary
        c2 = fg_primary if r2 == kept else fg_secondary
        if r1 == r2: c2 = fg_secondary

        f1 = f_kept_style if c1 == fg_primary else f_drop_style
        f2 = f_kept_style if c2 == fg_primary else f_drop_style

        tk.Label(card.nums_frame, text=str(r1), font=f1, fg=c1, bg=bg_color).pack(side=tk.LEFT, padx=4)
        tk.Label(card.nums_frame, text=str(r2), font=f2, fg=c2, bg=bg_color).pack(side=tk.LEFT, padx=4)

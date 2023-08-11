from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE = "Chinese"
FLASHCARD_TIMER = 3000
word_dict = {}

# ---------------------------- Generating Random Words ------------------------------- #
# Implementing pandas and creating word dictionary
try:
    language_data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/chinese_words.csv")
    word_dict = {row["char"]: [row["pinyin"], row["eng"]] for _, row in original_data.iterrows()}
else:
    word_dict = {row["char"]: [row["pinyin"], row["eng"]] for _, row in language_data.iterrows()}
known_words = list(word_dict.keys())
current_card = {}
print(word_dict)


def next_card():
    global LANGUAGE, current_card
    current_card = random.choice(known_words)
    print(current_card)
    generated_pinyin = word_dict[current_card][0]
    canvas.itemconfig(word_text, text=f"{current_card}")
    canvas.itemconfig(pinyin_text, text=f"{generated_pinyin}")
    canvas.itemconfig(language_text, text=LANGUAGE)

    global card_is_flipped
    if card_is_flipped != 0:
        window.after_cancel(card_is_flipped)
    card_is_flipped = window.after(FLASHCARD_TIMER, lambda: flip_card())
    canvas.itemconfig(canvas_image, image=front_card)
    canvas.itemconfig(word_text, fill="black")
    canvas.itemconfig(language_text, fill="black")

# ---------------------------- REMOVE KNOWN WORDS ------------------------------- #


def is_known():
    del word_dict[current_card]
    columns = ["char", "pinyin", "eng"]
    new_data = pd.DataFrame.from_dict(word_dict, orient="index", columns=["pinyin", "eng"])
    new_data.index.name = "char"
    new_data.reset_index(inplace=True)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
# CARD FRONT DESIGN
# Create window
window = Tk()
window.title("Flashcard App")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)

# Create canvas
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
front_card = PhotoImage(file="images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=front_card)
canvas.grid(row=1, column=1, columnspan=2)

# Create canvas text
language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"), fill="black")
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"), fill="black")
pinyin_text = canvas.create_text(400, 350, text="", font=("Arial", 20, "bold"), fill="black")
# Create right/wrong buttons
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, background=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(row=2, column=1)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, background=BACKGROUND_COLOR, command=is_known)
right_button.grid(row=2, column=2)


# ---------------------------- FLIP CARD ------------------------------- #
back_card = PhotoImage(file="images/card_back.png")


def flip_card():
    generated_answer = word_dict[current_card][1]
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=f"{generated_answer}", fill="white")
    canvas.itemconfig(pinyin_text, text="")


card_is_flipped = 0
next_card()

# ---------------------------- CREATE NEW FILE ------------------------------- #


window.mainloop()



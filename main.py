import tkinter
from tkinter import *
from tkinter import messagebox
from random import *
import pandas
import os

BACKGROUND_COLOR = "#B1DDC6"

#-------------------------- UI ---------------------------#

window = Tk()
window.title("LFlash")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# CANVAS
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
path = "words_to_learn.csv"
if os.path.exists(path) and os.path.getsize(path) > 10:
    data = pandas.read_csv(path)
    df = pandas.DataFrame(data)
else:
    data = pandas.read_csv("german_words.csv")
    df = pandas.DataFrame(data)
dict_data = df.to_dict(orient="records")
random_dict = None
front_canvas = None


def got_wrong():
    global random_dict
    german_word = dict_data[random_dict]["German"]
    english_word = dict_data[random_dict]["English"]
    data_new = {
        "German": german_word,
        "English": english_word,
    }
    df = pandas.DataFrame(data_new, index=[0])
    path = "words_to_learn.csv"
    if os.path.exists(path) and os.path.getsize(path) > 10:
        df.to_csv(path, mode="a", header=False, index=False)
    else:
        df.to_csv(path, mode="w", header=True, index=False)
    front_side()

def got_right():
    global random_dict
    del dict_data[random_dict]
    try:
        if len(dict_data) > 0:
            front_side()
        else:
            messagebox.showinfo(title="Words Finished", message="Done with all the words, how did you do?")
            window.destroy()
    except tkinter.TclError as e:
        messagebox.showinfo(f"Caught an error: {e}\nNo need to worry about it though")

def front_side():
    global random_dict
    random_dict = randint(0, len(dict_data) - 1)
    global front_canvas
    front_canvas = tkinter.Canvas(window, bg=BACKGROUND_COLOR, width=800, height=526, highlightthickness=0)
    front_canvas.grid(column=0, row=0, columnspan=2)
    front_canvas.create_image(410, 269, image=front_image)
    front_canvas.create_text(400, 150, text="German", font=("Arial", 25, "italic"))
    german_word = dict_data[random_dict]["German"]
    front_canvas.create_text(400, 263, text=german_word, font=("Arial", 50, "bold"))
    window.after(3000, back_side)


def back_side():
    global random_dict
    if len(dict_data) > 0:
        front_canvas.delete("all")
        front_canvas.create_image(410, 269, image=back_image)
        front_canvas.create_text(400, 150, text="English", font=("Arial", 25, "italic"))
        english_word = dict_data[random_dict]["English"]
        front_canvas.create_text(400, 263, text=english_word, font=("Arial", 50, "bold"))
    else:
        pass


# BUTTONS

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, borderwidth=0, command=got_right)
right_button.grid(column=1, row=1)
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, borderwidth=0, command=got_wrong)
wrong_button.grid(column=0, row=1)

front_side()

window.mainloop()

from tkinter import *
import pandas
import random

# ---------------------------- CONSTANTS ------------------------------- #
YELLOW = "#f7f5dd"
GREEN = '#9bdeac'
L_PURPLE = "#372948"
H_PURPLE = "#251B37"
FONT_NAME = "Courier"
TIMER_SEC = 30
timer = None
random_string_words = ""


# ---------------------------- LIST OF MOST COMMON WORDS ------------------------------- #
def get_words():
    with open("words_list.txt") as words_list:
        all_words = [line.rstrip() for line in words_list]
        random.shuffle(all_words)
        for word in all_words:
            global random_string_words
            random_string_words += word
            random_string_words += " "


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="1min")
    get_words()
    words_reset()
    typing_area_reset()


# ---------------------------- WORDS AREA RESET ------------------------------- #

def words_reset():
    words['state'] = 'normal'
    words.delete('1.0', 'end')
    words.insert('1.0', f"{random_string_words}")
    words['state'] = 'disabled'
    text.delete('1.0', 'end')


# ---------------------------- TYPING AREA RESET ------------------------------- #

def typing_area_reset():
    text.delete('1.0', 'end')
    text.insert('1.0', "Type here the words you see above.")


# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    count_down(TIMER_SEC)
    words_reset()
    text.delete('1.0', 'end')


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

def count_down(count):
    count_sec = count
    text_content = text.get('1.0', 'end')
    if " " in text_content:
        typed_words = text_content.split(" ")
        print(len(typed_words))
        if len(typed_words) > 2:
            config_words_area()

    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_sec}sec")

    if count > 0:
        global timer, ranking
        timer = window.after(1000, count_down, count - 1)

    if count == 0:
        text_content = text.get('1.0', 'end')
        typed_words = ("").join(text_content)
        typed_words_list = typed_words.split()
        # print(typed_words_list)

        correct_list = [_ for _ in typed_words_list if _ in random_string_words]
        incorrect_list = [_ for _ in typed_words_list if _ not in random_string_words]
        WPM = len(correct_list)
        CPM = sum(len(i) for i in correct_list)
        canvas.itemconfig(timer_text, text="0sec")
        # print(f" Correct words: {correct_list}, incorrect words: {incorrect_list}")

        # Ranking

        new_score = {"CPM": CPM, "WPM": WPM}
        new_score_df = pandas.DataFrame(new_score, index=[0])
        try:
            ranking = pandas.read_csv("ranking.csv")
        except FileNotFoundError:
            new_score_df.to_csv("ranking.csv", index=False)
            ranking = pandas.read_csv("ranking.csv")
        finally:
            new_record = pandas.concat([ranking, new_score_df])
            new_record.to_csv("ranking.csv", index=False)

        print(new_record)

        CPM_hs = new_record.CPM.max()
        WPM_hs = new_record.WPM.max()

        CPM_mean = new_record.CPM.mean()
        WPM_mean = new_record.WPM.mean()

        words['state'] = 'normal'
        words.delete('1.0', 'end')
        words.insert('2.2', f"End of Time. \nYour score: {WPM}WPM, {CPM}CPM \nHighest record: {WPM_hs}WMP, {CPM_hs}CMP")
        words['state'] = 'disabled'
        words.update()


# ---------------------------- UPDATING WORDS FIELD ------------------------------- #

def config_words_area():
    words['state'] = 'normal'
    words.delete('1.0', '1.1')
    words['state'] = 'disabled'
    words.update()


# ---------------------------- UI SETUP ------------------------------- #
get_words()

window = Tk()
window.title("Typing Speed Test")
window.config(pady=50, padx=100, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
timer_text = canvas.create_text(100, 130, text="1min", fill=H_PURPLE, font=(FONT_NAME, 20, "bold"))
canvas.grid(row=1, column=2)

# Text

text = Text(window, width=50, height=5, fg="grey", font=(FONT_NAME, 16))
text.insert('1.0', "Click the start button and type here the words you can see above.")
text.grid(row=2, column=0)

words = Text(window, width=50, height=5, fg=H_PURPLE, bg=GREEN, font=(FONT_NAME, 16))
words.grid(row=1, column=0)
words.insert('1.0', f"{random_string_words}")
words['state'] = 'disabled'

# Labels

label_timer = Label(text="Typing Speed Test", fg=L_PURPLE, bg=YELLOW, font=(FONT_NAME, 40, "bold"))
label_timer.grid(row=0, column=0, columnspan=2)

label_CMP = Label(text="CMP - Correct Characters Per Minute", fg=L_PURPLE, bg=YELLOW, font=(FONT_NAME, 14))
label_CMP.grid(row=3, column=0, columnspan=2)
label_WPM = Label(text="WMP - Correct Words Per Minute", fg=L_PURPLE, bg=YELLOW, font=(FONT_NAME, 14))
label_WPM.grid(row=4, column=0, columnspan=2)

# Button

start_image = PhotoImage(file="play.png")
button_start = Button(image=start_image, highlightthickness=0, bg=YELLOW, command=start_timer)
button_start.grid(row=2, column=2)

restart_image = PhotoImage(file="restart.png")
button_reset = Button(image=restart_image, highlightthickness=0, bg=YELLOW, command=reset_timer)
button_reset.grid(row=2, column=3)

# Window mainloop

window.mainloop()

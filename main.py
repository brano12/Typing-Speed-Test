# What are CPM and WPM?
# They're short for Characters Per Minute, and Words Per Minute.
# The "raw CPM" is the actual number of characters you type per minute, including all the mistakes.
# "Correct" scores count only correctly typed words. "WPM" is just the corrected CPM divided by 5.
# That's a de facto international standard.
import requests
import tkinter as tk
from tkinter.messagebox import showinfo

window = tk.Tk()
window.geometry("520x200")
window.title("Typing speed test")
window.config(background="#ffeaea", pady=7, padx=4)
FONT_NAME = "'Roboto Mono'"

class Text_Class:
    def __init__(self):
        self.txt_list = self.text_generator()
        self.pressed_let = None
        self.counter = 0
        self.corrCPM = 0
        self.offset = 0
        self.coefficient = 1
        self.first_time = True

    def text_generator(self):
        response = requests.get(url="https://random-word-api.vercel.app/api?words=150")
        self.text_to_type = " ".join(response.json())
        return response.json()


text_machine = Text_Class()

def start_timer():
    if text_machine.first_time:
        text_machine.first_time = False
    # resetting writing field if starter triggered another time than first time
    else:
        window.after_cancel(text_machine.tmr)

        text_machine.txt_list = text_machine.text_generator()
        shown_text.config(state='normal')
        shown_text.delete('1.0', 'end')
        shown_text.insert('1.0', text_machine.text_to_type)
        shown_text.tag_add("center-text", "1.0", "end")
        shown_text.config(state='disabled')
        window.update_idletasks()

        entry_wgt.delete(0, tk.END)
        entry_wgt.focus_set()
        shown_text.tag_remove("redd", 1.0, 'end')
        shown_text.tag_remove("prpl", 1.0, 'end')
        text_machine.pressed_let = None
        text_machine.counter = 0
        text_machine.corrCPM = 0
        text_machine.offset = 0
        text_machine.coefficient = 1

    entry_wgt.delete(0, tk.END)
    entry_wgt.focus_set()
    count_down(60)
    cpm_display.config(text=0)
    wpm_display.config(text=0)
    entry_wgt.bind("<KeyRelease>", click)


def click(event):
    shown_text.tag_remove("redd", f"1.{text_machine.offset}", f"1.{text_machine.offset + len(text_machine.txt_list[text_machine.counter])}")
    shown_text.tag_remove("prpl", f"1.{text_machine.offset}", f"1.{text_machine.offset + len(text_machine.txt_list[text_machine.counter])}")

    text_machine.pressed_let = event.char
    written_text_str = entry_wgt.get()

    if len(written_text_str) > len(text_machine.txt_list[text_machine.counter]):
        length = len(text_machine.txt_list[text_machine.counter])
    else:
        length = len(written_text_str)
    #here we compare each entry with shown word from line, letter after letter
    for i in range(0, length):
        if written_text_str[i] == text_machine.txt_list[text_machine.counter][i]:
            # this condition is just for app tweak so it doesn't show any red color when just spaces are typed
            if written_text_str != " ":
                shown_text.tag_remove("redd", f"1.{i + text_machine.offset}", f"1.{i + 1 + text_machine.offset}")
                shown_text.tag_add("prpl", f"1.{i + text_machine.offset}", f"1.{i + 1 + text_machine.offset}")

        else:
            if written_text_str != " ":
                shown_text.tag_remove("prpl", f"1.{i + text_machine.offset}", f"1.{i + 1 + text_machine.offset}")
                shown_text.tag_add("redd", f"1.{i + text_machine.offset}", f"1.{i + 1 + text_machine.offset}")
    # this condition is just for app tweak so when just spaces are accidentaly typed nothing happens and writer can type further
    if text_machine.pressed_let == " ":
        if written_text_str == " ":
            entry_wgt.delete(0, tk.END)

        else:
            print("space was pressed")
            written_text_str = written_text_str[:-1]

            # here code compares typed word with shown one
            if text_machine.txt_list[text_machine.counter] == written_text_str:
                #if typed word matches its correct CPM is counted and shown matching word will be signed with green color
                text_machine.corrCPM = text_machine.corrCPM + len(written_text_str)
                print(text_machine.corrCPM)
                shown_text.tag_remove("redd", f"1.{text_machine.offset}", f"1.{text_machine.offset + len(text_machine.txt_list[text_machine.counter])}")
                shown_text.tag_add("good", f"1.{text_machine.offset}", f"1.{text_machine.offset + len(text_machine.txt_list[text_machine.counter])}")
            else:
                #incorrect word will be signed with red after typing SPACE
                shown_text.tag_remove("prpl", f"1.{text_machine.offset}", f"1.{text_machine.offset + len(text_machine.txt_list[text_machine.counter])}")
                shown_text.tag_add("bad", f"1.{text_machine.offset}", f"1.{text_machine.offset + len(text_machine.txt_list[text_machine.counter])}")

            text_machine.offset = text_machine.offset + len(text_machine.txt_list[text_machine.counter]) + 1
            text_machine.counter += 1
            print(text_machine.counter)
            print(text_machine.offset)
            entry_wgt.delete(0, tk.END)

            #part for checking on which line we are and when to scroll the text according of what is being typed
            lines = shown_text.count('1.0', 'end', 'displaylines')
            chars = len(shown_text.get('1.0', 'end'))
            average_charpline = chars / lines[0]

            if text_machine.offset > (average_charpline+7)*text_machine.coefficient:
                shown_text.yview_scroll(1,'units')
                text_machine.coefficient += 1
        #written_text_str = entry_wgt.get()

def count_down(count):
    timer_display.config(text=count)

    if count == 0:
        entry_wgt.unbind("<KeyRelease>")

        cpm_display.config(text=text_machine.corrCPM)
        wpm_display.config(text=text_machine.corrCPM/5)
        return

    text_machine.tmr=window.after(1000, count_down, count -1)

def help():
    tk.messagebox.showinfo(title="Help", message="Hello\n\nThis is one-minute typing test to find out\nhow many words do you type in one minute:\n\n- 'raw CPM' "
                                                 "is the actual number of characters you type per minute, including all the mistakes."
                                                      "\n- 'Corrected CPM' scores count only characters of correctly typed words."
                                                 "\n- 'WPM' is just the corrected CPM divided by 5.\n- press Start to trigger the timer and start to type\n- only word finished with SPACE counts!"
                                                 "\n\n Good Luck!")


################################################## GUI part ############################################################

starter_button = tk.Button(width=6, bg="#76ffe1", text="Start", font= (FONT_NAME, 10, "bold"), highlightthickness=0, command=start_timer)
starter_button.grid(row=0,column=0, sticky="W", padx=(3,0))

empty_label = tk.Label(width=20, text="HI! TEST YOURSELF ;)", font= ("System", 10, "normal"), bg="#ffeaea")
empty_label.grid(row=0, column=1, padx=(110,0))

timer_sign = tk.Label(text="Time left:",font= (FONT_NAME, 10, "normal"), bg="#ffeaea")
timer_sign.grid(row=0, column=2, sticky="E", columnspan=2)

timer_display = tk.Label(text="60",font= (FONT_NAME, 12, "bold"), fg="#f98484", bg="black", width=2)
timer_display.grid(row=0, column=3, sticky="E", padx=(0,5), columnspan=2)

######################################## TABLE FOR PRINTING THE TEXT TO BE TYPED #######################################

shown_text = tk.Text(width=53, height=3, font= (FONT_NAME, 12, "normal"), bg="#ffeaea", wrap='word')
shown_text.insert('1.0', text_machine.text_to_type)
shown_text.config(state='disabled')

shown_text.tag_configure("prpl", foreground="#7A316F")
shown_text.tag_configure("redd", foreground="red")
shown_text.tag_configure("good", font= (FONT_NAME, 12, "italic"), foreground="#7A316F")
shown_text.tag_configure("bad", font= (FONT_NAME, 12, "italic", "underline"), foreground="#CD6688")
shown_text.tag_configure("center-text", justify='center')
shown_text.tag_add("center-text", "1.0", "end")

shown_text.grid(row=1, columnspan= 5, pady=(20,10), padx=(15,15))

######################################### WINDOW WHERE USER TYPES TEXT #################################################
entry_wgt = tk.Entry(width=40, font= (FONT_NAME, 12, "normal"), justify="center")
entry_wgt.focus_set()
entry_wgt.grid(row=2, columnspan= 5, pady=(10,15))
################################################################################################################

help_button = tk.Button(width=6, background="#76ffe1", text="Help", font= (FONT_NAME, 10, "bold"), command=help)
help_button.grid(row=3, column=0)

cpm_label = tk.Label(text="Corrected CPM:", font= (FONT_NAME, 10, "normal"), bg="#ffeaea")
cpm_label.grid(row=3, column=1, sticky="E")

cpm_display = tk.Label(width=4, font= (FONT_NAME, 10, "bold"), bg="black", fg="#f98484")
cpm_display.grid(row=3, column=2, sticky="W")

wpm_label = tk.Label(text="WPM:",font= (FONT_NAME, 10, "normal"), bg="#ffeaea")
wpm_label.grid(row=3, column=3, sticky="E")

wpm_display = tk.Label(width=4, font= (FONT_NAME, 10, "bold"), bg="black", fg="#f98484")
wpm_display.grid(row=3, column=4, sticky="W")

window.mainloop()
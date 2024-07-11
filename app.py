from tkinter import *
from tkinter import ttk
from subprocess import call
from pickle import load
import tkinter.scrolledtext as scrolledtext
import fetcher

def get_fetched_data():
    text.delete(1.0,END)
    fetcher.fetch()
    with open("data.pkl","rb") as f:
        all_contests = load(f)

    _text = ""
    for itm in all_contests:
        _text+=display(itm)

    text.insert('1.0', _text)

print("App Running")
root = Tk()
root.title("Fetch Contests")

frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Contest List").grid(column=0, row=0)

#Buttons
get_btn = ttk.Button(frm,text="Get Contests",width=50,command=get_fetched_data)
quit_btn = ttk.Button(frm, text="Quit", command=root.destroy)
get_btn.grid(column=0, row=2)
quit_btn.grid(column=0, row=10)

#Scrollable Text
text = scrolledtext.ScrolledText(root, undo=True)
text['font'] = ('consolas', '12')
text.grid(row=1,column=0)


def display(contest):
    return f''' Name : {contest.name}\n
                Date : {contest.date}\n
                Time : {contest.time}\n'''

class ContestInfo:
    def __init__(self,name,date,time):
        self.name = name
        self.date = date
        self.time = time

root.mainloop()
print("App Ended")
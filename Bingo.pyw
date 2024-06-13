import json
import random
import tkinter as tk
import sys

#TODO: Sachen die von Personen und spielmodi abhängig sind seperat behandeln
#braucht mayor rewrite ... cringe. bis dahin einfach boards neu generieren falls nötig
#Klassen würden sich inzwischen auch lohnen
def main():
    def generate_Bingo(window):
        for deck in cardDecks:
            cardDecks[deck] = buttonsVars[deck].get()
        global closing
        closing = False
        window.destroy()

    def toggle_background(target):
        if target['background'] == "white":
            target.configure(background="grey")
        else:
            target.configure(background="white")


    def set_wrap(event):
        width = event.width
        for child in window.winfo_children():
            child.configure(wraplength = width-20)

    global closing
    closing = True
    f = open('BingoJson.json', 'r', encoding='utf-8')
    cardJson = json.loads(f.read())
    f.close()
    cardDecks = {}
    for deck in cardJson:
        cardDecks.update({deck: False})
    finalDeck = []
    w1 = tk.Tk()
    w1.title("Bingo Settings")
    buttons = {}
    buttonsVars = {}
    for deck in cardDecks:
        temp = tk.IntVar()
        buttonsVars.update({deck: temp})
        buttons.update({deck: tk.Checkbutton(w1, text=deck, variable=buttonsVars[deck], onvalue=True, offvalue=False)})
        buttons[deck].pack()
    buttons['general'].select()
    tk.Label(w1, text = "Dimensions: ").pack()
    dimensions = tk.IntVar()
    dimensions.set(5)
    dimensionsOptions = [("3", 3),
              ("4", 4),
              ("5", 5),
              ("6", 6)]
    for text, d in dimensionsOptions:
        tk.Radiobutton(text = text, value = d, variable= dimensions).pack()
    button = tk.Button(
        text = "Create Bingo Board",
        width = 25,
        height = 5,
        command = lambda: generate_Bingo(w1)
    )
    button.pack()
    w1.mainloop()
    if closing == True:
        sys.exit()
    for deck in cardDecks:
        if cardDecks[deck] == True:
            temp = cardJson[deck]
            for card in temp:
                finalDeck.append(card)
    for card in finalDeck:
        i = finalDeck.index(card)
        for otherCard in finalDeck[i+1:]:
            if card == otherCard:
                finalDeck.remove(otherCard)
    i = 0
    global window
    window = tk.Tk()
    window.title("Bingo")
    row = 0
    column = 0
    bingoBoard = {}
    while i < dimensions.get() * dimensions.get():
        temp = random.choice(finalDeck)
        finalDeck.remove(temp)
        button = tk.Button(
            text=temp,
            width=30,
            height=5,
            bg="white",
            wraplength = 100
        )
        button.configure(command=lambda target=button: toggle_background(target))
        bingoBoard.update({temp: button})
        button.grid(row=row, column=column, padx=5, pady=5, sticky="news")
        tk.Grid.rowconfigure(window, row, weight=1)
        row += 1
        if row == dimensions.get():
            tk.Grid.columnconfigure(window, column, weight=1)
            row = 0
            column += 1
        if i == 0:
            button.bind("<Configure>", set_wrap)
        i += 1
    window.mainloop()
    main()
main()

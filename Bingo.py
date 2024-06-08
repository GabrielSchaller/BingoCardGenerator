import json
import random
import tkinter as tk

#TODO: Sachen die von Personen und spielmodi abhängig sind seperat behandeln

def main():
    def generate_Bingo(window):
        for deck in cardDecks:
            cardDecks[deck] = buttonsVars[deck].get()
        window.destroy()

    def toggle_background(target):
        if target['background'] == "white":
            target.configure(background="grey")
        else:
            target.configure(background="white")

    f = open('BingoJson.json', 'r', encoding='utf-8')
    cardJson = json.loads(f.read())
    f.close()
    cardDecks = {}
    for deck in cardJson:
        cardDecks.update({deck: False})
    finalDeck = []
    window = tk.Tk()
    window.title("Bingo Settings")
    buttons = {}
    buttonsVars = {}
    for deck in cardDecks:
        temp = tk.IntVar()
        buttonsVars.update({deck: temp})
        buttons.update({deck: tk.Checkbutton(window, text=deck, variable=buttonsVars[deck], onvalue=True, offvalue=False)})
        buttons[deck].pack()
    buttons['general'].select()
    tk.Label(window, text = "Dimensions: ").pack()
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
        command = lambda: generate_Bingo(window)
    )
    button.pack()
    window.mainloop()
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
            width=40,
            height=5,
            bg="white"
        )
        button.configure(command=lambda target=button: toggle_background(target))
        bingoBoard.update({temp: button})
        button.grid(row=row, column=column, padx=5, pady=5)
        row += 1
        if row == dimensions.get():
            row = 0
            column += 1
        i += 1
    window.mainloop()
    main()
main()

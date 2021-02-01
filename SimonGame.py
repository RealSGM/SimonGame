from random import randint
from tkinter import mainloop,Tk,LabelFrame,Label,Button,Entry,W

#Variables
linesOfColours = []
colourSequence = []
count = 0
correct = 0
difficulty = ""
username = ""
confirmation = False
noOfColours = 4

#Constants
COLOURS = ["blue","orange","#f482c9","cyan","yellow","#5f1242"]
ROUNDS = 10
FLASH = 400
BUTTONSIZE = 10


def colour_flash(button,colour):
    button.config(bg = colour)
    

#Resets the difficulty buttons back to black
def buttonReset():
    simpleButton.configure(fg = "black")
    normalButton.configure(fg = "black")
    trickyButton.configure(fg = "black")

#End frame, shows the player's score
def end_frame():
    global correct
    global username
    gameFrame.destroy()
    score = Label(root, text = ("Score: " + str(correct)),padx = 5, pady = 5)
    score.grid(row = 0, column = 0, sticky = W, padx = 100, pady = 100)  
    with open("scores.txt","a") as scoreFile:
        scoreFile.write(username + "," + str(correct) + "\n")   

#Choosing difficulty, turns the difficulty button to red when clicked
def difficulty_chooser(diff,button):
    global difficulty
    difficulty = diff
    buttonReset()
    button.configure(fg = 'red')

#Checks that the variables are saved correctly then runs the rest of the game
def save_var(name,root,difficulty):
    global confirmation
    global username
    username = name.get()
    if username != "" and difficulty != "":
        #Changes the sequence based on the difficulty
        RSG(difficulty)
        #Destroys the menu 
        menuFrame.destroy()
        colour_read(noOfColours)
        game(linesOfColours)

#Read colours from file then saves it
def colour_read(noOfColours):
    global linesOfColours

    with open("sequences.txt", "r") as sequence_file:
        linesOfColours = sequence_file.readlines()
    for line in range(len(linesOfColours)):
        linesOfColours[line] = linesOfColours[line].strip("\n")
        if (line+1) % (noOfColours+1) == 0:
            colourSequence.append(linesOfColours[line])

#Function to check if the button clicked was the correct button, flashes green or red depending on if it was correct or not
def onClick(colour,correctColours,button):
    global count
    global correct
    global FLASH

    if (colour == correctColours[count]):
        correct += 1
        button.configure(bg = 'green')
        root.after(400,lambda:colour_flash(button,colour))
    else:
        button.configure(bg = 'red')
        root.after(400,lambda: colour_flash(button,colour))

    if count == ROUNDS-1:
        end_frame()
    count+=1
 
#Initialises the game gui depending on the difficulty
def game(listOfColours):
    root.title("Simon!")
    gameFrame.grid()

    blueButton.grid(row = 0, column = 0)
    orangeButton.grid(row = 0, column = 1)

    if difficulty == "Normal" or difficulty == "Tricky":
        cyanButton.grid(row = 1, column = 0)
        yellowButton.grid(row = 1, column = 1) 

    if difficulty == "Tricky":
        purpleButton.grid(row =1, column = 2)  
        pinkButton.grid(row = 0, column = 2)         

# Random Sequence Generator which is based on the difficulty 
def RSG(difficulty):
    global noOfColours
    if difficulty == "Simple":
        noOfColours = 2
    elif difficulty == "Normal":
        noOfColours = 4
    elif difficulty == "Tricky":
        noOfColours = 6

    with open("sequences.txt", "w") as sequence_file:
        #Number of tries
        for line in range(ROUNDS):
            for colour in range(noOfColours):
                sequence_file.write(COLOURS[colour] + "\n")
            sequence_file.write(COLOURS[randint(0,noOfColours - 1)] + "\n")

#Displays the buttons,frames,entries required for the main menu
def main_menu():
    #Display  
    global name
    menuFrame.grid(row = 1,column = 0, sticky = W, padx = 5, pady = 5)
    buttonFrame.grid(row = 2, column = 0, sticky = W, padx = 5, pady = 5)
    confirmFrame.grid(row = 3,column = 0, sticky = W, padx = 5, pady = 5)
    submitButton.grid(row = 0, column = 0, sticky = W, padx = 5, pady = 5)  
    #Input field
    name = Entry(menuFrame)
    name.grid(row = 0, column = 1, sticky = W, padx = 5, pady = 5) 

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
root = Tk()
root.title("Main Menu")
root.resizable(0, 0) 

#Frame assignment
menuFrame = LabelFrame(root,text = "Menu", padx = 5, pady = 5)
gameFrame = LabelFrame(root,text = "Game", padx = 5, pady = 5)
buttonFrame = LabelFrame(menuFrame,text = "Difficulties", padx = 5, pady = 5)
confirmFrame = LabelFrame(menuFrame,text = "", padx = 5, pady = 5)

#Main menu assignment
enterName = Label(menuFrame, text = "Enter your name:")
simpleButton = Button(buttonFrame,text = "Simple",command = lambda: difficulty_chooser("Simple",simpleButton))
normalButton = Button(buttonFrame,text = "Normal",command = lambda: difficulty_chooser("Normal",normalButton))
trickyButton = Button(buttonFrame,text = "Tricky",command = lambda: difficulty_chooser("Tricky",trickyButton))
submitButton = Button(confirmFrame,text = "Submit",command = lambda: save_var(name,root,difficulty))

#Game button assignment
cyanButton = Button(gameFrame, height = BUTTONSIZE, width = 2*BUTTONSIZE, bg = COLOURS[3],command = lambda: onClick(COLOURS[3],colourSequence,cyanButton))
purpleButton = Button(gameFrame, height = BUTTONSIZE, width = 2*BUTTONSIZE, bg = COLOURS[5],command = lambda: onClick(COLOURS[5],colourSequence,purpleButton)) 
blueButton = Button(gameFrame, height = BUTTONSIZE, width = 2*BUTTONSIZE, bg = COLOURS[0],command = lambda: onClick(COLOURS[0],colourSequence,blueButton))
orangeButton = Button(gameFrame, height = BUTTONSIZE, width = 2*BUTTONSIZE, bg = COLOURS[1],command = lambda: onClick(COLOURS[1],colourSequence,orangeButton))
pinkButton = Button(gameFrame, height = BUTTONSIZE, width = 2*BUTTONSIZE, bg = COLOURS[2],command = lambda: onClick(COLOURS[2],colourSequence,pinkButton))
yellowButton = Button(gameFrame, height = BUTTONSIZE, width = 2*BUTTONSIZE, bg = COLOURS[4],command = lambda: onClick(COLOURS[4],colourSequence,yellowButton))

#Menu button assignment
enterName.grid(row = 0, column = 0, sticky = W)
simpleButton.grid(row = 1, column = 0, sticky = W)
normalButton.grid(row = 1, column = 1, sticky = W)
trickyButton.grid(row = 1, column = 2, sticky = W)

#Mainloop
main_menu()
mainloop()
    

    
"""
This will be the "friendly" interface.

Have a menu / button to select and load a file, extract the text and keep that in memory.

Have an input box for a question. Have an output section for displaying the answer. Have a button to submit the question.

"""

from file_digester import *
from question_answerer import *
import PySimpleGUI as sg

import os


# First the window layout in 2 columns
textdata=""
file_list_column = [
    [
        sg.Text("Select a file to ask questions about:"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
answer_question_column = [
    [sg.Text("Once Loaded, you can ask your questions here:")],
[sg.Text(size=(40, 1), key="-STATS-")],

[sg.Text('Question:', size =(40, 1), key="-QUEST-"), sg.InputText()],

[sg.Button("Ask"), sg.Exit()],

[sg.Text(size=(40, 1), key="-TOUT-")]

]



# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(answer_question_column),
    ]
]

window = sg.Window("Question Answerer", layout)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-STATS-"].update("Loading File, Please wait...")
            print(filename)
            textdata=convertToText(filename)
            window["-STATS-"].update("File Loaded")

        except:
            pass
    elif event =="Ask": #we are asking a question
        try:
            #print("values are...")
            #print(values)
            #print("clearing question data...")
            questiondata=values[1]
            #print(questiondata)
            window["-TOUT-"].update("")
            if len(questiondata)<1:
                window["-TOUT-"].update("You need to ask a question!")
            else:
                #print(len(textdata))
                if len(textdata)<1:
                    window["-TOUT-"].update("You need to select a file to ask against!")
                else:
                    #print("processing question...")
                    window["-STATS-"].update("Processing, please wait...")
                    answerdata=answer_question(questiondata,textdata)
                    window["-TOUT-"].update("Answer: "+answerdata)


        except Exception as e:
            print("something went wrong, below is the message:")
            print(e)

window.close()
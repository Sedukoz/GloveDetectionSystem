import PySimpleGUI as sg
import Glove_Orientation_AI as GOA
import Glove_Orientation as GO
import Glove_Measure as GM
import GLove_Type as GT
import Glove_Defect as GD

Image1 = sg.Image(filename='Glove1.png', size=(300, 300), key='image')
Image2 = sg.Image(filename='Glove2.png', size=(300, 300), key='image')
Image3 = sg.Image(filename='Glove3.png', size=(300, 300), key='image')
def main():
    sg.theme("DarkBlue13")
    layout = [[sg.Column([[sg.Text('GLOVE INSPECTION SYSTEM' , size=(30, 1), justification="center", font=('Impact` 30'),
                                     text_color='#195AA4',
                                     background_color='white',pad=(5, 3))]], justification='center')]
                ,[sg.Column([[sg.Text('Select a task from the following:' , size=(30, 1), justification="center", font=('Impact` 20'),
                                     text_color='#195AA4',
                                     background_color='white',pad=(3, 5))]], justification='center')]
                ,[sg.Column([[Image1,Image3,Image2]], justification='center')]
                ,[sg.Column([[sg.Button("Glove Type Detector") ,sg.Button('Glove Measurements'),
                              sg.Button('Glove Defects Detector') , sg.Button('Glove Orientation') ,
                              sg.Button('Glove Orientation + AI'), sg.Button('Exit') ]], justification='center')]]     #buttons

    window = sg.Window('Glove Inspection System' , layout ,resizable=True )

    while True:             # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):         # checks if user wants to exit
            break

        if event == 'Glove Type Detector':
            print("Task 1")
            GT.glove_type()
        if event == 'Glove Measurements':
            print("Task 2")
            GM.Glove_Measure()
        if event == 'Glove Defects Detector':
            print("Task 3")
            GD.glove_defect()
        if event == 'Glove Orientation':
            print("Task 4")
            GO.glove_detect()
        if event == 'Glove Orientation + AI':
            print("Task 4 + AI")
            GOA.glove_detectAI()

    window.Close()


if __name__ == '__main__':
    main()
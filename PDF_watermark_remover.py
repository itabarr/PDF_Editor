import fitz
import PySimpleGUI as sg
from os.path import exists


def add_white_watermark(input_file , output_dir , filename):
    # Open the pdf
    doc = fitz.open(input_file)
    for page in doc:
        # For every page, draw a rectangle on coordinates (1,1)(100,100)
        page.draw_rect([200,820,450,835],  color = (1,1, 1), width = 2 , fill = True)
    # Save pdf
    doc.save(f'{output_dir}/{filename}.pdf')


# All the stuff inside your window.
layout = [[sg.T("")], [sg.Text("Input PDF: "), sg.Input(), sg.FileBrowse()],
          [sg.T("")], [sg.Text("Output folder: "), sg.Input(), sg.FolderBrowse()],
        [sg.T("")], [sg.Text("File name: "), sg.Input()],
          [sg.T("")], [sg.Button("Press here to remove watermark")]]

###Building Window
window = sg.Window('Remove Watermark App', layout, size=(550,250) , element_justification='c' , icon='icon.ico')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

    elif event == "Press here to remove watermark":
        input_file = values[0]
        output_dir = values[1]
        filename = values[2]

        if not input_file or not output_dir or not filename:
            sg.popup("You didn't choose one of the inputs.")
            continue

        if not input_file.endswith('.pdf'):
            sg.popup("Input file is not PDF." )
            continue

        if  exists(f'{output_dir}/{filename}.pdf'):
            sg.popup(f"{filename}.pdf file already exists in chosen folder. Please choose diffrent filename / folder.")
            continue
        try:
            add_white_watermark(input_file , output_dir, filename)
            sg.popup(f"{filename}.pdf file was saved in output folder.")
        except:
            sg.popup("An unknown error occured. You might tried to override an existing file. Please choose a unique name. If this doesn't work, contact developers." )

window.close()
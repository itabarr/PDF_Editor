from pikepdf import Pdf
import glob

import PySimpleGUI as sg
from os.path import exists
import shutil

import os

def parse_pages_string(pages_string):
    numbers_list = []

    try:
        pages_string = pages_string.replace(" ", "")
        numbers = pages_string.split(",")
        for substring in numbers:
            if "-" in substring:
                first_num = substring.split("-")[0]
                first_num = int(first_num)
                last_num = substring.split("-")[1]
                last_num = int(last_num)

                for i in range(first_num , last_num +1):
                    numbers_list.append(i)
            else:
                substring = int(substring)
                numbers_list.append(substring)

        numbers_list = list(set(numbers_list))
        numbers_list.sort()
        return numbers_list

    except:
        return -1

def init_IN_WORK(output_dir):
    IN_WORK = "IN_WORK_9386986982341234"
    path = os.path.join(output_dir , IN_WORK)
    if exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    return path

def fin_IN_WORK(path):
    if exists(path):
        shutil.rmtree(path)

def split_merge_pdf(input_file, output_dir , filename , numbers_list):
    pdf = Pdf.open(input_file)

    if not all(i <= len(pdf.pages)  for i in numbers_list):
        return f"MAX-PAGES-NUMBER-IS-{len(pdf.pages)}"

    IN_WORK = init_IN_WORK(output_dir)
    for n, page in enumerate(pdf.pages):
        if n+1 in numbers_list:
            dst = Pdf.new()
            dst.pages.append(page)
            dst.save(f'{IN_WORK}/{n:02d}.pdf')

    out_pdf = Pdf.new()
    for file in glob.glob(f"{IN_WORK}/*"):
        src = Pdf.open(file)
        out_pdf.pages.extend(src.pages)
    src.close()

    out_pdf.save(f'{output_dir}/{filename}.pdf')
    fin_IN_WORK(IN_WORK)
    return "SUCCESS"




# All the stuff inside your window.
layout = [[sg.T("")], [sg.Text("Input PDF: "), sg.Input(), sg.FileBrowse()],
        [sg.T("")], [sg.Text("Output folder: "), sg.Input(), sg.FolderBrowse()],
        [sg.T("")], [sg.Text("File name: "), sg.Input()],
        [sg.T("")], [sg.Text("Page numbers:"), sg.Input()],
        [sg.T("")], [sg.Button("Press here to edit PDF")]]

###Building Window
window = sg.Window('PDF Splitter App', layout, size=(550,350) , element_justification='c' , icon='icon.ico')

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

    elif event == "Press here to edit PDF":
        # input_file= "C:/Users/as/Desktop/INPUT_PDF.pdf"
        # output_dir = "C:/Users/as/Desktop/"
        # filename = "try__"
        # pages_numbers = "1-10,22"


        input_file = values[0]
        output_dir = values[1]
        filename = values[2]
        pages_numbers = values[3]

        if not input_file or not output_dir or not filename or not pages_numbers:
            sg.popup("You didn't choose one of the inputs.")
            continue

        if not input_file.endswith('.pdf'):
            sg.popup("Input file is not PDF." )
            continue

        if  exists(f'{output_dir}/{filename}.pdf'):
            sg.popup(f"{filename}.pdf file already exists in chosen folder. Please choose diffrent filename / folder.")
            continue
        try:
            pages_numbers = parse_pages_string(pages_numbers)

            if pages_numbers == -1:
                sg.popup(
                    f"Could not parse pages number. Maybe you inserted incorrect format.")
                continue

            status = split_merge_pdf(input_file,output_dir,filename,pages_numbers)
            if status == "SUCCESS":
                sg.popup(f"{filename}.pdf file was saved in output folder.")
            else:
                sg.popup(f"Error with editing pdf. Error is: {status}.")

        except Exception as e:
            print(e)
            sg.popup("An unknown error occured. You might tried to override an existing file. Please choose a unique name. If this doesn't work, contact developers." )

window.close()
import tkinter
import tkinter.filedialog


import sqlite3
import pandas as pd


# create the root window
root = tkinter.Tk()
root.title('Whatsapp Extractor')
root.resizable(False, False)
root.geometry('500x280')


def select_file():
    global filename
    filetypes = (('database', '*.db'),)
    filename = tkinter.filedialog.askopenfilename(
        title='Please choose the database',
        initialdir='/',
        filetypes=filetypes)

def save_file():
    global file_saved
    files = [('Excel File', '*.xlsx'),]
    file = tkinter.filedialog.asksaveasfile(filetypes = files, defaultextension = files)
    file_saved = file.name



def reader(database):
    conn = sqlite3.connect(database)
    select = "SELECT * FROM messages;"
    cursor = conn.cursor()
    cursor.execute(select)

    phones = []
    texts = []
    sends = []

    print("Process has started successfuly!")
    while True:
        record = cursor.fetchone()
        if record == None:
            break
        a_string = record[1]
        numeric_filter = filter(str.isdigit, a_string)
        numeric_string = "".join(numeric_filter)
        phones.append(numeric_string)
        texts.append(record[6])
        if record[2] == 1:
            sends.append('Sender')
        else:
            sends.append('Reciever')


    df = pd.DataFrame({'Phone': phones,
                       'Text': texts,
                       'Sender/Reciever': sends})
    writer = pd.ExcelWriter(file_saved, engine='xlsxwriter')    
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    conn.close()
    print('EOL')


# open button
open_button = tkinter.Button(
    root,
    text='Open Database',
    command=select_file,
    height = 2,
    width=50
).grid(row=1, column=0, padx=50, pady=(25, 0))

save_button = tkinter.Button(
    root,
    text='Save Here',
    command=save_file,
    height = 2,
    width=50
).grid(row=2, column=0, padx=50, pady=(25, 0))

convert_button = tkinter.Button(
    root,
    text='Convert',
    command= lambda: reader(filename),
    height = 2,
    width=50
).grid(row=3, column=0, padx=50, pady=(25, 0))

open_button.pack(expand=True)
convert_button.pack(expand=True)

# run the application
root.mainloop()

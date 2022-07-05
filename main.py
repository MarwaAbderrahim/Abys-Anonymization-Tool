############# Importation 
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.constants import DISABLED, NORMAL
from os import listdir
from glob import glob
import os
from PIL import Image, ImageTk
import pandas as pd
import glob
import cv2
import csv as csv_lib
import sys
import pandas
import numpy as np


############ page 1 
def call_home_page():
    root.geometry('600x750')
    home_page = Frame(root, bg=bg)
    home_page.grid(row=0, column=0, sticky='nsew')
    title = Label(home_page, text='Abys Anonymization Tool', bg=bg, fg='Black', font='Arial 30 ')
    title.pack(pady=(20,0))
    image = Image.open('utils/image.png')
    image=image.resize((350,150))
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image = photo)
    label.image = photo
    label.grid(row=1,column=0)
    buttons_frame = Frame(home_page, bg=bg)
    buttons_frame.pack( padx=10,pady=40)

    dicom_to_nifti_button = Button(buttons_frame, text='k-Anonymity', font='none 20 bold', width=15, bg='black',fg='white', command=second)
    dicom_to_nifti_button.pack(pady=(80,0))

############# page 2 
def second ():
    global text_message_d_n
    global convert_save
    global root
    global df2
    dicom_to_nifti = Frame(root, bg=bg)
    dicom_to_nifti.grid(row=0, column=0, sticky='nsew')

    title = Label(dicom_to_nifti, text='k-Anonymity', bg='black',fg='white', font='Arial 20 bold')
    title.pack()
    open_buttons = Frame(dicom_to_nifti, bg=bg)
    open_buttons.pack(pady=(30,0))

    open_dir = Button(open_buttons, text='Open csv file', font='none 20 bold', width=10, fg='orangered',bg='gainsboro', command=call_open_file_csv)
    open_dir.grid(row=0, column=1, pady=(40,0))

    convert_save = Button(dicom_to_nifti, text='Convert & Save', state = NORMAL , font='none 20 bold', fg='orangered',bg='gainsboro', command= call_convert_csv)
    convert_save.pack(pady=(40,0))

    convert_save = Button(dicom_to_nifti, text='Anonymity check', font='none 20 bold', fg='orangered',bg='gainsboro', command=anonymity_check)
    convert_save.pack(pady=(40,0))

    text_message_d_n = Label(dicom_to_nifti,text='Choose csv file', font='none 7', bg='darkorange',fg='black')
    text_message_d_n.pack(pady=(20,0))
        
    home_button = Button(dicom_to_nifti, text='Home', command=call_home_page, font='none 20 bold', width=15, bg='black',fg='white')
    home_button.place(x=170, y=450)

    home_button = Button(dicom_to_nifti, text='Restart', command=restart, font='none 20 bold', width=15, bg='black',fg='white')
    home_button.place(x=170, y=510)
        

############# page 2 : Functions to open and convert .csv & .xls files            
# Open .csv & .xls file 
def call_open_file_csv():
    global flag_dicom_nifti
    global in_path_csv
    global text_message_d_n
    in_path_csv = filedialog.askopenfilename()
    print(in_path_csv)
    print(type(in_path_csv))
    if in_path_csv: 
        text_message_d_n.config(text='You opened:\n' + str(in_path_csv))
    else:
       messagebox.showerror("Error", "try again")
# Anonymize .csv & .xls file
def call_convert_csv():
    global text_message_d_n
    global new_out_path
    global df
    df3=[]
    path=os.path.splitext(in_path_csv)[0]
    if in_path_csv:
        root, extension = os.path.splitext(in_path_csv)
        print (extension)
        print(extension=='.xlsx')
        if extension=='.xlsx':
            df=pd.read_excel(in_path_csv)
        else: df = pandas.read_csv(in_path_csv, sep=';')
        age11= df.columns[df.columns.str.contains('AGE|Age|age|AGe')]
        age111=df.loc[:,age11].squeeze()
        print(type(age11))
        age11=age111.name
        print(age11)
        print(age111)
        print(type(age111))
        x=len(age111)
        for i in range(x):
            if int(age111[i]) >0 and int(age111[i]<=30):
                df3.append("[0,30]")
            elif int(age111[i]>30) and int(age111[i]<=70):
                df3.append("[30,70]")
            else: 
                df3.append(">70") 
        print(age11)
        print(type(age11))        
        df[age11]=df3
        new_out_path=path+'_reidentificated.csv'
        df.to_csv(new_out_path, index=False, sep=';')
        text_message_d_n.config(text='Anonymization is finished\n'+'File saved at\n' + new_out_path)

# Check anonymity of the converted file
def anonymity_check(): 
    k=2
    global df
    for index, row in df.iterrows():
        age11= df.columns[df.columns.str.contains('AGE|Age|age|AGe')]
        age111=df.loc[:,age11].squeeze()
        age11=age111.name
        sexe= df.columns[df.columns.str.contains('Sex|SEX|sex')]
        sexe=df.loc[:,sexe].squeeze()
        sexe=sexe.name
        quasi_identi=[age11,sexe]
        q = ' & '.join([f"{col} == '{row[col]}'"  for col in quasi_identi])
        kk = df.query(q)
        ll=df.groupby([age11, age11]).size()
        if ll.shape[0] < k:
            messagebox.showerror("Anonymity check", "False")
    messagebox.showinfo("Anonymity check", "Anonymity check : True")

# To restart the interface 
def restart():
    os.execv(sys.executable, ['python'] + sys.argv)


############# The main function 
if __name__ == '__main__':
    global in_path_image_dicom
    global in_path_dicom_image
    global in_path_nifti_dicom
    global in_path_dicom_nifti

    global flag_image_dicom
    global flag_dicom_image 
    global flag_nifti_dicom 
    global flag_dicom_nifti

    flag_image_dicom = 0
    flag_dicom_image = 0
    flag_nifti_dicom = 0
    flag_dicom_nifti = 0
    bg = 'white'
    root = Tk()
    root.geometry('600x750')
    root.title('Abys Anonymization Tool')
    root.iconbitmap('utils/logo.ico')
    root.resizable(width=0, height=0)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    call_home_page()
    root.mainloop()
    

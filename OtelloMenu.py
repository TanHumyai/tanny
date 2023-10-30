import tkinter as tk
from tkinter import *
from customtkinter import *
import customtkinter 
from tkinter import PhotoImage
from PIL import Image, ImageTk
from ottelloGamePVP import OthelloPVP
from ottelloGamePVAHard import OthelloPVA
from ottelloGamePVAEZ import OthelloPVA as EZ
class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Menu")
        self.geometry('500x550')
        self.resizable(width=False,height=False)
        customtkinter.set_appearance_mode('dark')
        customtkinter.set_default_color_theme('blue')
        self.config(bg='darkblue')
        self.img = Image.open("C:\\Users\\tansxerd\\OneDrive\\เอกสาร\\vscode\\test\\cat.png")
        self.photo = ImageTk.PhotoImage(self.img)

        self.lable = Label(self,bg='darkblue', image=self.photo)
        self.lable.pack(side = "bottom")

        
        # Add a title
        self.wellcome = CTkLabel(self, text="OTHELLO",font=('Times New Roman',40))
        self.wellcome.pack(pady=40,side="top")
        
        
        # Button to start the Othello game
        self.start_button = CTkButton(self, text="PVP", command=self.start_pvpgame)
        self.start_button.pack(pady=20)
        
 
        self.pva_button = CTkButton(self, text="PVA EASY", command=self.start_pvaezgame)
        self.pva_button.pack(pady=20)
        self.pva_button = CTkButton(self, text="PVA MEDIUM", command=self.start_pvahardgame)
        self.pva_button.pack(pady=20)
            
            

    def start_pvpgame(self):
        game = OthelloPVP()
    def start_pvaezgame(self):
        game = EZ()

    def start_pvahardgame(self):
        game = OthelloPVA()
    

if __name__ == '__main__':
    menu = MainMenu()
    menu.mainloop()

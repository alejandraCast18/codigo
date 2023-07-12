import tkinter as tk
import customtkinter 
from client.gui_app import Frame_login

def main():
    root = customtkinter.CTk()
    root.title('Inicio')
    root.geometry('1000x480')
    root.minsize(980,460)
    customtkinter.set_appearance_mode("dark")
    #customtkinter.set_default_color_theme("theme.json")
    app = Frame_login(root = root)

    app.mainloop()

if __name__ == '__main__':
    main()
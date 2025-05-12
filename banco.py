import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode('dark')

def apesnas_leitura(entry_value):
    return entry_value.isalpha() or entry_value == "" 

def validar_login():
    usuario = campo_nome.get()
    senha = campo_password.get()

    if usuario == "Ismar" and  senha == "te amo":
        verdade.configure(text='Login feito com sucesso!', text_color="green")
    else:
        verdade.configure(text='Login negado!', text_color="red")

app = ctk.CTk()
app.title("Sistema de Login da carteira")
app.geometry('300x300')

app.mainloop()
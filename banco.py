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
 
vcmd = app.register(apesnas_leitura)

campo_user = ctk.CTkLabel(app, text='Usuário:')
campo_user.pack(pady=5)

campo_nome = ctk.CTkEntry(app, placeholder_text="Digite seu nome", validate="key", validatecommand=(vcmd, "%P"))
campo_nome.pack(pady=5)

campo_senha = ctk.CTkLabel(app, text="Senha:")
campo_senha.pack(pady=10)

campo_password = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*" )
campo_password.pack(pady=5)

botao = ctk.CTkButton(app, text='Login', command=validar_login)
botao.pack(pady=10)

verdade = ctk.CTkLabel(app, text='')
verdade.pack(pady=10)

app.mainloop()
import customtkinter as ctk
import tkinter as tk
import json
import os

ctk.set_appearance_mode('dark')

ARQUIVO_USUARIOS = "usuarios.json"

def carregar_usarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        json.dump({}, f)
    with open(ARQUIVO_USUARIOS, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f)

def verificar_login(usuarios, senha):
    usuarios = carregar_usarios
    return usuarios in usuarios and usuarios[usuarios] == senha

def cadastrar_usuarios(usuarios, senha):
    usuarios = carregar_usarios()
    if usuarios in usuarios:
        return False
    usuarios[usuarios] = senha
    salvar_usuarios(usuarios)
    return True

def apesnas_leitura(entry_value):
    return entry_value.isalpha() or entry_value == "" 

def validar_login():
    usuario = campo_nome.get()
    senha = campo_password.get()

    if usuario == "Ismar" and  senha == "te amo":
        verdade.configure(text='Login feito com sucesso!', text_color="green")
    else:
        verdade.configure(text='Login negado!', text_color="red")

def cadastrar():
    usuario = campo_nome.get()
    senha = campo_password.get()

    if cadastrar_usuarios(usuario, senha):
        verdade.configure(text='Cadastro feito!', text_color='green')
    else:
        verdade.configure(text="O usuario já existe!", text_color='orange')

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

botoao_login = ctk.CTkButton(app, text='login', command=validar_login)
botoao_login.pack(pady=10)

botao_cadastro = ctk.CTkButton(app, text='Castrar', command=cadastrar)
botao_cadastro.pack(pady=5)

verdade = ctk.CTkLabel(app, text='')
verdade.pack(pady=10)



app.mainloop()
<<<<<<< HEAD
import customtkinter as ctk
import tkinter as tk
import json
import os

ctk.set_appearance_mode('dark')

ARQUIVO_USUARIOS = "usuarios.json"

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump({}, f)
    with open(ARQUIVO_USUARIOS, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f)

def verificar_login(usuario, senha):
    usuarios = carregar_usuarios()
    return usuario in usuarios and usuarios[usuario] == senha

def cadastrar_usuario(usuario, senha):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        return False
    usuarios[usuario] = senha
    salvar_usuarios(usuarios)
    return True

def apenas_leitura(entry_value):
    return entry_value.isalpha() or entry_value == "" 

def validar_login():
    usuario = campo_nome.get()
    senha = campo_password.get()

    if verificar_login(usuario, senha):
        verdade.configure()
        campo_user.pack_forget()
        campo_nome.pack_forget()
        campo_senha.pack_forget()
        campo_password.pack_forget()
        botoao_login.pack_forget()
        botao_cadastro.pack_forget()
        pagina_conversor.pack(pady=20)
    else:
        verdade.configure(text='Login negado!', text_color="red")

def cadastrar():
    usuario = campo_nome.get()
    senha = campo_password.get()

    if cadastrar_usuario(usuario, senha):
        verdade.configure(text='Cadastro feito!', text_color='green')
    else:
        verdade.configure(text="O usuario já existe!", text_color='orange')


app = ctk.CTk()
app.title("Sistema de Login da carteira")
app.geometry('300x300')
 
vcmd = app.register(apenas_leitura) 

pagina_conversor= ctk.CTkFrame(app)

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

botao_cadastro = ctk.CTkButton(app, text='Cadastrar', command=cadastrar)
botao_cadastro.pack(pady=5)

verdade = ctk.CTkLabel(app, text='')
verdade.pack(pady=10)

titulo= ctk.CTkLabel(pagina_conversor, text="Conversor de moedas")
texto_moeda_origem= ctk.CTkLabel(pagina_conversor, text="Selecione a moeda de origem")
texto_moeda_destino= ctk.CTkLabel(pagina_conversor, text="Selecione a moeda de destino")

campo_moeda_origem= ctk.CTkOptionMenu(pagina_conversor, values=["USD", "BRL", "EUR", "BTC"] )
campo_moeda_destino= ctk.CTkOptionMenu(pagina_conversor, values=["USD", "BRL", "EUR", "BTC"] )

titulo.pack(padx=10, pady=10)
texto_moeda_origem.pack(padx=10, pady=10)
campo_moeda_origem.pack(padx=10, pady=10)
texto_moeda_destino.pack(padx=10, pady=10)
campo_moeda_destino.pack(padx=10, pady=10)

app.mainloop()

=======
>>>>>>> c7fcbb9 (Pagina de Login com titulos)

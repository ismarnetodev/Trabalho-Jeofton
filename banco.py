import customtkinter as ctk
import tkinter as tk
import json
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from convercoes import pegar_cotacao_moeda
import random

ctk.set_appearance_mode('dark')

app = ctk.CTk()
app.title("Sistema de Login da carteira")
app.attributes('-fullscreen', True)
app.geometry('410x400')

pagina_saldo = ctk.CTkFrame(app)
scroll_frame_conversor = ctk.CTkScrollableFrame(app)

ARQUIVO_USUARIOS = "usuarios.json"

usuario_logado = None

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump({}, f)
    with open(ARQUIVO_USUARIOS, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

def verificar_login(usuario, senha):
    usuarios = carregar_usuarios()

    return usuario in usuarios and usuarios[usuario]["senha"] == senha

def cadastrar_usuario(usuario, senha):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        return False
    saldo = round(random.uniform(1000, 10000), 2)
    usuarios[usuario] = {"senha": senha, "saldo": saldo}
    salvar_usuarios(usuarios)
    return True

def apenas_leitura(entry_value):
    return entry_value.isalpha() or entry_value == "" 

def validar_login():
    global usuario_logado
    usuario = campo_nome.get()
    senha = campo_password.get()
    

    if verificar_login(usuario, senha):
        usuario_logado = usuario
        verdade.configure(text="Seja bem vindo {}!".format(usuario))
       
        for widget in [campo_user, campo_nome, campo_senha, campo_password, botoao_login, botao_cadastro, mostrar_senha, frame_login]:
           widget.pack_forget()
        atualizar_saldo()
        pagina_saldo.pack(pady=20)
        scroll_frame_conversor.pack(fill="both", expand=True)
        
    
    else:
        verdade.configure(text='Login negado!', text_color="red")

def cadastrar():
    usuario = campo_nome.get()
    senha = campo_password.get()

    if cadastrar_usuario(usuario, senha):
        verdade.configure(text='Cadastro feito!', text_color='green')
    else:
        verdade.configure(text="O usuario já existe!", text_color='orange')


def alternar_senha():
    if mostrar_var.get() == 1:
        campo_password.configure(show="")
    else:
        campo_password.configure(show="*")    

def sair_tela_cheia(event=None):
    app.attributes('-fullscreen', False)

def exibir_grafico():
    origem = campo_moeda_origem.get()
    destino = campo_moeda_destino.get()

    cotacao = {
        "USD": 5.7,
        "EUR": 6.7,
        "ARS": 209.96,
        "BRL": 1.0,
        "CAD": 0.24,
    }

    if origem == destino:
        verdade.configure(text="Selecione moedas diferentes!", text_color="orange")
        return

    for widget in scroll_frame_conversor.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

    valor_inicial = cotacao.get(origem, 1.0)
    fator_conversao =  cotacao.get(destino, 1.0) / valor_inicial

    x = list(range(10))
    y = [valor_inicial * (fator_conversao ** i) for i in x]        

    fig, ax = plt.subplots()
    ax.plot(x, y, color="lime", linestyle="--", marker="o", label="Crescimento exponencial")
    ax.set_title(f"Curva Exponencial: {origem} → {destino}")
    ax.set_xlabel("Unidade de Tempo (simulada)")
    ax.set_ylabel(f"Valor em {destino}")

    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=scroll_frame_conversor)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)
         
def atualizar_saldo():
    usuarios = carregar_usuarios()
    saldo = usuarios[usuario_logado]["saldo"]
    label_saldo.configure(text=f"Saldo disponível: R$ {saldo:,.2f}")

def cotacao_moeda():
    moeda_origem= campo_moeda_origem.get()
    moeda_destino= campo_moeda_destino.get()

    try:
        
        valor= float(campo_valor.get())
        usuarios = carregar_usuarios()
        saldo = usuarios[usuario_logado]["saldo"]

        if valor <= 0 or valor > saldo:
            raise ValueError
    except ValueError:
        texto_cotacao_moeda.configure(text="Digite um valor válido!", text_color="red")
        return
    
    if moeda_origem and moeda_destino:
        if moeda_origem == moeda_destino:
            texto_cotacao_moeda.configure(text="Escolha moedas diferentes!", text_color="orange")

        cotacao= pegar_cotacao_moeda(moeda_origem, moeda_destino)

        try:
            cotacao = float(cotacao)
            convertido = valor * cotacao
            texto_cotacao_moeda.configure(
                text=f"{valor:.2f} {moeda_origem} = {convertido:.2f} {moeda_destino}", 
                text_color="white"
            )
        except ValueError as e:
            texto_cotacao_moeda.configure(text=f"Erro ao converter: {str(e)}", text_color="red") 

app.bind("<Escape>", sair_tela_cheia)
vcmd = app.register(apenas_leitura) 

frame_login = ctk.CTkFrame(app)
frame_login.pack(expand=True)

ctk.CTkLabel(frame_login, text='Bem vindo!', text_color='Blue', font=ctk.CTkFont(size=24, weight='bold')).pack(pady=20)
ctk.CTkLabel(scroll_frame_conversor, text="Selecione a moeda para converte-la!", font=ctk.CTkFont(size=15, weight='bold')).pack(pady=15)

campo_user = ctk.CTkLabel(app, text='Usuário:')
campo_user.pack(pady=5)

campo_nome = ctk.CTkEntry(app, placeholder_text="Digite seu usuário", validate="key", validatecommand=(vcmd, "%P"))
campo_nome.pack(pady=5)

campo_senha = ctk.CTkLabel(app, text="Senha:")
campo_senha.pack(pady=10)

campo_password = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*")
campo_password.pack(pady=5)

mostrar_var= tk.IntVar()
mostrar_senha= ctk.CTkCheckBox(app, text="Mostrar Senha", variable=mostrar_var, command=alternar_senha)
mostrar_senha.pack(padx=10, pady=10)

botoao_login = ctk.CTkButton(app, text='login', command=validar_login)
botoao_login.pack(pady=10)

botao_cadastro = ctk.CTkButton(app, text='Cadastrar', command=cadastrar)
botao_cadastro.pack(pady=5)

verdade = ctk.CTkLabel(app, text='')
verdade.pack(pady=10)

label_saldo = ctk.CTkLabel(pagina_saldo, text="")
label_saldo.pack(pady=20)


titulo= ctk.CTkLabel(scroll_frame_conversor, text="Conversor de moedas")
texto_moeda_origem= ctk.CTkLabel(scroll_frame_conversor, text="Selecione a moeda de origem")
texto_moeda_destino= ctk.CTkLabel(scroll_frame_conversor, text="Selecione a moeda de destino")

campo_moeda_origem= ctk.CTkOptionMenu(scroll_frame_conversor, values=["BRL"] )
campo_moeda_destino= ctk.CTkOptionMenu(scroll_frame_conversor, values=["USD","EUR", "ARS", "CAD"] )

texto_valor = ctk.CTkLabel(scroll_frame_conversor, text="Digite o valor a ser convertido: ")

campo_valor = ctk.CTkEntry(scroll_frame_conversor, placeholder_text="Ex: 100.00")

botao_converter= ctk.CTkButton(scroll_frame_conversor, text="Converter", command=cotacao_moeda)

texto_cotacao_moeda= ctk.CTkLabel(scroll_frame_conversor, text="")

btn_grafico = ctk.CTkButton(scroll_frame_conversor, text="Exibir grafico de preços", command=exibir_grafico)

titulo.pack(padx=10, pady=10)
texto_moeda_origem.pack(padx=10, pady=10)
campo_moeda_origem.pack(padx=10, pady=10)
texto_moeda_destino.pack(padx=10, pady=10)
campo_moeda_destino.pack(padx=10, pady=10)
texto_valor.pack(padx=10, pady=10)
campo_valor.pack(padx=10, pady=10)
botao_converter.pack(padx=10, pady=10)
texto_cotacao_moeda.pack(padx=10, pady=10)
btn_grafico.pack(pady=10, padx=10)

app.mainloop()
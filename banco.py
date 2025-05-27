import customtkinter as ctk
import tkinter as tk
import json
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from convercoes import pegar_cotacao_moeda

ctk.set_appearance_mode('dark')

app = ctk.CTk()
app.title("Sistema de Login da carteira")
app.attributes('-fullscreen', True)
app.geometry('410x400')
pagina_conversor = ctk.CTkFrame(app)

ARQUIVO_USUARIOS = "usuarios.json"

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump({}, f),
    with open(ARQUIVO_USUARIOS, "r") as f:
        return json.load(f)

def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

def verificar_login(usuario, senha):
    usuarios = carregar_usuarios()
    print("Usuarios carregados: {}".format(usuarios))

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
        verdade.configure(text="Seja bem vindo {}!".format(usuario))
        campo_user.pack_forget()
        campo_nome.pack_forget()
        campo_senha.pack_forget()
        campo_password.pack_forget()
        botoao_login.pack_forget()
        botao_cadastro.pack_forget()
        frame_login.pack_forget()
        mostrar_senha.pack_forget()
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
        "BTC": 320000.0,
        "BRL": 1.0
    }

    if origem == destino:
        verdade.configure(text="Selecione moedas diferentes!", text_color="orange")
        return

    moedas = [origem, destino]
    valores = [cotacao.get(origem, 0), cotacao.get(destino, 0)]

    # Limpar gráfico anterior
    for widget in pagina_conversor.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.get_tk_widget().destroy()

    fig, ax = plt.subplots()
    ax.bar(moedas, valores, color=["blue", "green"])
    ax.set_title("Cotação entre as moedas selecionadas")
    ax.set_ylabel("Valor em BRL")

    for i, valor in enumerate(valores):
        ax.text(i, valor + 0.02 * max(valores), f"R$ {valor:,.2f}", ha="center", fontsize=10)

    canvas = FigureCanvasTkAgg(fig, master=pagina_conversor)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

def cotacao_moeda():
    moeda_origem= campo_moeda_origem.get()
    moeda_destino= campo_moeda_destino.get()
    if moeda_origem and moeda_destino:
        cotacao= pegar_cotacao_moeda(moeda_origem, moeda_destino) 
        texto_cotacao_moeda.configure(text=f"1 {moeda_origem} = {cotacao} {moeda_destino}")   


app.bind("<Escape>", sair_tela_cheia)
vcmd = app.register(apenas_leitura) 

frame_login = ctk.CTkFrame(app)
frame_login.pack(expand=True)

ctk.CTkLabel(frame_login, text='Bem vindo!', text_color='Blue', font=ctk.CTkFont(size=24, weight='bold')).pack(pady=20)
ctk.CTkLabel(pagina_conversor, text="Selecione a moeda para converte-la!", font=ctk.CTkFont(size=15, weight='bold')).pack(pady=15)

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

titulo= ctk.CTkLabel(pagina_conversor, text="Conversor de moedas")
texto_moeda_origem= ctk.CTkLabel(pagina_conversor, text="Selecione a moeda de origem")
texto_moeda_destino= ctk.CTkLabel(pagina_conversor, text="Selecione a moeda de destino")

campo_moeda_origem= ctk.CTkOptionMenu(pagina_conversor, values=["USD", "BRL", "EUR", "BTC"] )
campo_moeda_destino= ctk.CTkOptionMenu(pagina_conversor, values=["USD", "BRL", "EUR", "BTC"] )

botao_converter= ctk.CTkButton(pagina_conversor, text="Converter", command=cotacao_moeda)

texto_cotacao_moeda= ctk.CTkLabel(pagina_conversor, text="")

btn_grafico = ctk.CTkButton(pagina_conversor, text="Exibir grafico de preços", command=exibir_grafico)

titulo.pack(padx=10, pady=10)
texto_moeda_origem.pack(padx=10, pady=10)
campo_moeda_origem.pack(padx=10, pady=10)
texto_moeda_destino.pack(padx=10, pady=10)
campo_moeda_destino.pack(padx=10, pady=10)
botao_converter.pack(padx=10, pady=10)
texto_cotacao_moeda.pack(padx=10, pady=10)
btn_grafico.pack(pady=10, padx=10)

app.mainloop()
import requests

def pegar_cotacao_moeda(moeda_origem, moeda_destino):
    link= f"https://economia.awesomeapi.com.br/json/last/{moeda_origem}-{moeda_destino}"
    requisicao= requests.get(link)

    cotacao= requisicao.json()[f"{moeda_origem}{moeda_destino}"]["bid"]
    return cotacao
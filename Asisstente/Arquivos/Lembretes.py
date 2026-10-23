import json
import os
from datetime import datetime

ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lembretes.json")

def carregar():
    if not os.path.exists(ARQUIVO):
        return[]

    try:
        with open(ARQUIVO, encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except json.JSONDecodeError:
        os.replace(ARQUIVO, ARQUIVO + ".bak")
        print(f"Arquivo de lembretes corrompido. Cópia salva em {ARQUIVO}.bak")
        return []
         

def salvar(lembretes):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(lembretes, arquivo, ensure_ascii=False, indent=2)


def adicionar(texto):
    lembretes = carregar()
    lembretes.append({
        "texto": texto,
        "criado_em": datetime.now().isoformat(timespec="minutes"),
    })
    salvar(lembretes)
    return len(lembretes)


def remover(numero):
    lembretes = carregar()

    if not 1 <= numero <= len(lembretes):
        return None

    removido = lembretes.pop(numero - 1)
    salvar(lembretes)
    return removido

def buscar(palavras):
    numeros = []

    for numero, lembrete in enumerate(carregar(), start=1):
        texto = lembrete["texto"].lower()

        if all(palavra in texto for palavra in palavras):
            numeros.append(numero)

    return numeros
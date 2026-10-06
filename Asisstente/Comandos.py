"""
Comandos do assistente.

Cada comando é uma função que recebe o texto falado. A tabela COMANDOS, no
final do arquivo, liga as palavras-gatilho a cada função.

Para criar um comando novo:
    1. escreva uma função  def meu_comando(comando): ...
    2. adicione uma linha na tabela COMANDOS
"""

from datetime import datetime
import webbrowser
from urllib.parse import quote_plus

import wikipedia

from Config import SITES
from Programas import abrir_programa
from Texto import extrair_termo
from Voz import falar

wikipedia.set_lang("pt")

DIAS_SEMANA = [
    "segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
    "sexta-feira", "sábado", "domingo",
]
 
MESES = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]

# =========================
# DATA E HORA
# =========================
 
def texto_hora(agora):
    """Transforma um datetime em uma frase falada: 'São 15 horas e 46 minutos'."""
    h, m = agora.hour, agora.minute
 
    # Em português, algumas horas têm forma e verbo especiais
    if h == 0:
        verbo, horas = "É", "meia-noite"
    elif h == 12:
        verbo, horas = "É", "meio-dia"
    elif h == 1:
        verbo, horas = "É", "uma hora"
    else:
        verbo, horas = "São", f"{h} horas"
 
    if m == 0:
        # "em ponto" não faz sentido para meia-noite e meio-dia
        sufixo = "" if h in (0, 12) else " em ponto"
        return f"{verbo} {horas}{sufixo}"
 
    minutos = "1 minuto" if m == 1 else f"{m} minutos"
    return f"{verbo} {horas} e {minutos}"
 
 
def texto_data(agora):
    """Transforma um datetime em uma frase falada: 'Hoje é terça-feira, 6 de ...'."""
    dia_semana = DIAS_SEMANA[agora.weekday()]
    mes = MESES[agora.month - 1]  # mês 1 (janeiro) fica na posição 0 da lista
    dia = "primeiro" if agora.day == 1 else agora.day
 
    return f"Hoje é {dia_semana}, {dia} de {mes} de {agora.year}"

# =========================
# FUNÇÕES DOS COMANDOS
# =========================

def informar_hora(comando):
    falar(texto_hora(datetime.now()))
 
 
def informar_data(comando):
    falar(texto_data(datetime.now()))
 
 
def informar_data_hora(comando):
    # Pega o "agora" uma vez só, para data e hora serem do mesmo instante
    agora = datetime.now()
    falar(f"{texto_data(agora)}. {texto_hora(agora)}")
 

def buscar_wikipedia(comando):
    termo = extrair_termo(comando, {"pesquisar", "wikipedia", "wikipédia"})

    if not termo:
        falar("Por favor, diga o que deseja pesquisar na Wikipedia.")
        return

    try:
        falar(wikipedia.summary(termo, sentences=2))

    except wikipedia.exceptions.DisambiguationError as erro:
        print(f"Algumas sugestões: {erro.options[:5]}")
        falar("O termo é muito amplo, tente ser mais específico.")

    except wikipedia.exceptions.PageError:
        falar("Não encontrei nada sobre isso na Wikipedia.")

    except Exception as erro:
        print(f"Erro na Wikipedia: {erro}")
        falar("Não consegui acessar a Wikipedia agora.")


def pesquisar_google(comando):
    termo = extrair_termo(comando, {"pesquisar"})

    if not termo:
        falar("Por favor, diga o que deseja pesquisar.")
        return

    webbrowser.open("https://www.google.com/search?q=" + quote_plus(termo))
    falar(f"Pesquisando {termo} no Google")


def abrir(comando):
    alvo = extrair_termo(comando, {"abrir"})

    if not alvo:
        falar("Qual programa você deseja abrir?")
    elif alvo in SITES:
        webbrowser.open(SITES[alvo])
        falar(f"Abrindo {alvo}")
    else:
        abrir_programa(alvo)


# =========================
# TABELA DE COMANDOS
# =========================
 
# (palavras-gatilho, função). A ORDEM IMPORTA: vale o primeiro que casar.
# "pesquisar na wikipedia ..." contém "pesquisar", então Wikipedia vem antes.
COMANDOS = [
    (("wikipedia", "wikipédia"), buscar_wikipedia),
    (("pesquisar",), pesquisar_google),
    (("abrir",), abrir),
    # "data e hora" vem antes de "hora" e "data" sozinhas: é o mais específico
    (("data e hora", "hora e data"), informar_data_hora),
    (("que horas", "que hora é"), informar_hora),
    (("que dia", "qual a data", "qual é a data", "data de hoje"), informar_data),
]
 
 
def executar_comando(comando):
    for gatilhos, funcao in COMANDOS:
        if any(gatilho in comando for gatilho in gatilhos):
            funcao(comando)
            return
 
    falar("Comando não reconhecido.")
 
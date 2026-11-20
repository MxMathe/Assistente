""" 
Cada comando é uma função que recebe o texto falado. A tabela COMANDOS, no
final do arquivo, liga as palavras-gatilho a cada função.
 
Para criar um comando novo:
    1. escreva uma função  def meu_comando(comando): ...
    2. adicione uma linha na tabela COMANDOS
"""



from datetime import datetime
from difflib import get_close_matches
import re
import webbrowser
from urllib.parse import quote_plus

import wikipedia

import Lembretes
from Config import SITES
from Programas import abrir_programa
from Texto import extrair_termo
from Voz import confirmar, falar, ouvir
from Respostas import frase

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
    falar(frase("pesquisando", termo=termo))


def abrir(comando):
    alvo = extrair_termo(comando, {"abrir"})
 
    if not alvo:
        falar("Qual programa você deseja abrir?")
    elif alvo in SITES:
        webbrowser.open(SITES[alvo])
        falar(frase("abrindo", nome=alvo))
    else:
        abrir_programa(alvo)

# =========================
# LEMBRETES
# =========================

PADRAO_ANOTAR = (
    r"^(anotar|anota|anote|me lembr(e|a) de|lembr(e|a)[- ]me de|lembrar de"
    r"|(criar|crie|novo|adicionar|adicione) lembrete( para| de)?)( que)?\b"
)
PADRAO_APAGAR = (
    r"^(apagar|apague|apaga|excluir|exclua|deletar|delete|remover|remova|limpar|limpe)\b"
    r".*\b(lembretes?|anotações?)\b"
)
PADRAO_LISTAR = (
    r"\b(ler|leia|listar|liste|mostrar|mostre|ver|veja|quais|meus|minhas|diga)\b"
    r".*\b(lembretes?|anotações?)\b"
)
 
NUMEROS_POR_EXTENSO = {
    "um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "tres": 3,
    "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9, "dez": 10,
}
 
# Palavras do comando que NÃO fazem parte do assunto do lembrete a apagar
PALAVRAS_APAGAR = {
    "apagar", "apague", "apaga", "excluir", "exclua", "deletar", "delete",
    "remover", "remova", "limpar", "limpe",
    "lembrete", "lembretes", "anotação", "anotações", "meu", "meus",
}
 
 
def extrair_numero(comando):
    achado = re.search(r"\d+", comando)
    if achado:
        return int(achado.group())
 
    for palavra in comando.split():
        if palavra in NUMEROS_POR_EXTENSO:
            return NUMEROS_POR_EXTENSO[palavra]
 
    if "último" in comando or "ultimo" in comando:
        return len(Lembretes.carregar())
 
    return None
 
 
def anotar_lembrete(comando):
    achado = re.match(PADRAO_ANOTAR, comando)
    texto = comando[achado.end():].strip()
 
    if not texto:
        falar("O que devo anotar?")
        texto = ouvir()
 
        if not texto:
            falar("Não ouvi nada, então não anotei.")
            return
 
    numero = Lembretes.adicionar(texto)
    falar(frase("anotado", numero=numero, texto=texto))
 
 
def listar_lembretes(comando):
    todos = Lembretes.carregar()
 
    if not todos:
        falar(frase("sem_lembretes"))
        return
 
    plural = "lembrete" if len(todos) == 1 else "lembretes"
    partes = [f"Você tem {len(todos)} {plural}."]
 
    for numero, lembrete in enumerate(todos, start=1):
        partes.append(f"Número {numero}: {lembrete['texto']}.")
 
    falar(" ".join(partes))
 
 
def apagar_lembrete(comando):
    total = len(Lembretes.carregar())
 
    if total == 0:
        falar(frase("sem_lembretes"))
        return
 
    # 1) Apagar tudo: pede confirmação, porque não dá para desfazer
    if re.search(r"\b(todos|todas|tudo)\b", comando):
        if confirmar(f"Você tem {total} lembretes. Tem certeza que quer apagar todos?"):
            Lembretes.remover_todos()
            falar("Todos os lembretes foram apagados.")
        else:
            falar("Tudo bem, não apaguei nada.")
        return
 
    # 2) Apagar por número: "apagar lembrete 2" / "o último lembrete"
    numero = extrair_numero(comando)
 
    # 3) Apagar pelo assunto: "apagar lembrete comprar pão"
    if numero is None:
        palavras = extrair_termo(comando, PALAVRAS_APAGAR).split()
 
        if not palavras:
            falar("Qual lembrete devo apagar? Diga o número, por exemplo: apagar lembrete 2.")
            return
 
        achados = Lembretes.buscar(palavras)
 
        if not achados:
            falar("Não encontrei nenhum lembrete com isso.")
            return
 
        if len(achados) > 1:
            falar("Encontrei mais de um. Diga o número do lembrete que quer apagar.")
            return
 
        numero = achados[0]
 
    removido = Lembretes.remover(numero)
 
    if removido:
        falar(frase("apagado", numero=numero, texto=removido["texto"]))
    else:
        falar(f"Não existe lembrete número {numero}.")

# =========================
# TENTAR ENTENDER COMANDOS DESCONHECIDOS
# =========================
 
# Verbos que vêm seguidos de um complemento ("abrir youtube", "pesquisar gatos").
# Cada forma que o reconhecimento de voz pode gerar aponta para o verbo certo.
VERBOS = {
    "abrir": "abrir", "abra": "abrir", "abre": "abrir",
    "pesquisar": "pesquisar", "pesquise": "pesquisar", "pesquisa": "pesquisar",
    "anotar": "anotar", "anote": "anotar",
}
 
# Palavra solta -> comando completo que a pessoa provavelmente quis dizer
PISTAS = {
    "hora": "que horas são",
    "horas": "que horas são",
    "data": "que dia é hoje",
    "lembrete": "ler meus lembretes",
    "lembretes": "ler meus lembretes",
    "anotações": "ler meus lembretes",
}
 
 
def adivinhar_comando(comando):
    """
    Tenta descobrir qual comando conhecido a frase lembra.
    Devolve a frase corrigida, ou None se não encontrar nada parecido.
    """
    palavras = comando.split()
 
    if not palavras:
        return None
 
    # 1) A primeira palavra parece um verbo conhecido? ("abri youtube")
    #    get_close_matches compara por semelhança de letras (0 a 1).
    parecidos = get_close_matches(palavras[0], VERBOS, n=1, cutoff=0.75)
 
    if parecidos and len(palavras) > 1:
        verbo = VERBOS[parecidos[0]]
        return " ".join([verbo] + palavras[1:])
 
    # 2) Alguma palavra lembra uma pista? ("me fala a hora")
    for palavra in palavras:
        parecidas = get_close_matches(palavra, PISTAS, n=1, cutoff=0.85)
 
        if parecidas:
            return PISTAS[parecidas[0]]
 
    return None
 
 
def sugerir_comando(comando):
    sugestao = adivinhar_comando(comando)
 
    if not sugestao:
        falar(frase("nao_entendi"))
        return
 
    if confirmar(frase("sugestao", sugestao=sugestao)):
        # sugerir=False evita um laço infinito se a sugestão também falhar
        executar_comando(sugestao, sugerir=False)
    else:
        falar(frase("cancelado"))
 
 
# =========================
# TABELA DE COMANDOS
# =========================
 
# (gatilhos, função). Cada gatilho é uma expressão regular, procurada na frase
# com re.search. Palavras simples ("pesquisar") continuam funcionando.
#
# A ORDEM IMPORTA: vale o primeiro que casar.
#  - Lembretes vêm PRIMEIRO: o texto de um lembrete pode conter qualquer coisa
#    ("me lembre de abrir o banco") e não deve disparar outros comandos.
#  - "pesquisar na wikipedia ..." contém "pesquisar", então Wikipedia vem antes.

COMANDOS = [
    ((PADRAO_APAGAR,), apagar_lembrete),
    ((PADRAO_ANOTAR,), anotar_lembrete),
    ((PADRAO_LISTAR,), listar_lembretes),
    (("wikipedia", "wikipédia"), buscar_wikipedia),
    (("pesquisar",), pesquisar_google),
    (("abrir",), abrir),
    # "data e hora" vem antes de "hora" e "data" sozinhas: é o mais específico
    (("data e hora", "hora e data"), informar_data_hora),
    (("que horas", "que hora é"), informar_hora),
    (("que dia", "qual a data", "qual é a data", "data de hoje"), informar_data),
]
 
 
def executar_comando(comando, sugerir=True):
    for gatilhos, funcao in COMANDOS:
        if any(re.search(gatilho, comando) for gatilho in gatilhos):
            funcao(comando)
            return
 
    # Nenhum gatilho casou: tenta adivinhar o que a pessoa quis dizer
    if sugerir:
        sugerir_comando(comando)
    else:
        falar(frase("nao_entendi"))
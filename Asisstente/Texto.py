"""Funções auxiliares para tratar o texto falado."""

from Config import FRASES_ATIVACAO, PALAVRAS_LIGACAO


def limpar_inicio(texto):
    """Remove artigos/preposições do começo: 'o vs code' -> 'vs code'."""
    palavras = texto.split()

    while palavras and palavras[0] in PALAVRAS_LIGACAO:
        palavras.pop(0)

    return " ".join(palavras)


def extrair_termo(comando, palavras_comando):
    """Tira as palavras de comando e devolve só o assunto da pesquisa."""
    palavras = [p for p in comando.split() if p not in palavras_comando]
    return limpar_inicio(" ".join(palavras))


def detectar_ativacao(texto):
    """
    Verifica se o texto contém a frase de ativação.
    Devolve (ativou, resto), onde 'resto' é o que foi dito depois dela:
    'olá assistente abrir youtube' -> (True, 'abrir youtube')
    """
    # Remove pontuação ("olá, assistente" -> "olá assistente")
    texto = "".join(c for c in texto if c.isalnum() or c.isspace())
    texto = " ".join(texto.split())

    for frase in FRASES_ATIVACAO:
        if frase in texto:
            return True, texto.split(frase, 1)[1].strip()

    return False, ""
"""
Frases do assistente, com várias versões para cada situação.

Em vez de escrever ou falar("Abrindo youtube")  no código, usamos
falar(frase("abrindo", nome="youtube"))  e a função sorteia uma das versões.
Assim o assistente não repete sempre a mesma resposta.

Listas de frases abaixo.
Os trechos entre chaves, como {nome}, são preenchidos na hora de falar.
"""

import random

FRASES = {
    # --- conversa ---
    "saudacao": [
        "Olá! Como posso te ajudar?",
        "Oi! Pode falar.",
        "Estou ouvindo.",
        "Pois não?",
        "Às ordens! O que você precisa?",
    ],
    "espera": [
        "Voltando ao modo de espera.",
        "Vou ficar quietinho. É só me chamar.",
        "Qualquer coisa, é só chamar.",
    ],
    "tchau": [
        "Até mais!",
        "Até logo!",
        "Tchau, até a próxima!",
    ],

    # --- comando desconhecido ---
    "nao_entendi": [
        "Não entendi, pode repetir por favor?",
        "Hum, não consegui entender. Fala de novo?",
        "Desculpa, não peguei essa. Pode repetir?",
        "Esse comando você ainda não programou.",
        "Isso eu ainda não sei fazer.",
    ],
    "sugestao": [
        'Não conheço esse comando, mas acho que você quis dizer "{sugestao}". Quer que eu faça isso?',
        'Será que você quis dizer "{sugestao}"? Posso fazer isso?',
        'Não tenho certeza, mas parece que você quer "{sugestao}". É isso?',
    ],
    "cancelado": [
        "Tudo bem, deixa pra lá.",
        "Ok, não vou fazer nada.",
        "Sem problemas, cancelado.",
    ],

    # --- programas, sites e pesquisas ---
    "abrindo": [
        "Abrindo {nome}.",
        "Certo, abrindo {nome}.",
        "Já estou abrindo {nome}.",
        "Beleza, abrindo {nome}.",
    ],
    "programa_nao_encontrado": [
        "Não encontrei o programa {nome}.",
        "Procurei, mas não achei {nome} aqui.",
        "Hum, não achei nenhum programa chamado {nome}.",
    ],
    "pesquisando": [
        "Pesquisando {termo} no Google.",
        "Vou procurar {termo} para você.",
        "Certo, buscando {termo}.",
    ],

    # --- lembretes ---
    "anotado": [
        "Anotado! Lembrete número {numero}: {texto}",
        "Pronto, anotei. Lembrete {numero}: {texto}",
        "Combinado, está anotado como lembrete {numero}: {texto}",
    ],
    "apagado": [
        "Apaguei o lembrete {numero}: {texto}",
        "Pronto, o lembrete {numero} foi apagado: {texto}",
        "Feito. Lembrete {numero} removido: {texto}",
    ],
    "sem_lembretes": [
        "Você não tem lembretes.",
        "Sua lista de lembretes está vazia.",
        "Não há nenhum lembrete por aqui.",
    ],
}

# Guarda a última frase usada em cada situação, para não repetir em seguida
_ultima = {}


def frase(chave, **dados):
    """Escolhe ao acaso uma versão da frase 'chave' e preenche os {campos}."""
    opcoes = FRASES[chave]

    # Evita repetir a mesma frase duas vezes seguidas (se houver outra opção)
    if len(opcoes) > 1:
        opcoes = [o for o in opcoes if o != _ultima.get(chave)]

    escolhida = random.choice(opcoes)
    _ultima[chave] = escolhida

    return escolhida.format(**dados)
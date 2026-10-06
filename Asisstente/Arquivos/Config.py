"""Configurações do assistente. Para ajustar o comportamento, mexa aqui."""

SITES = {
    "youtube": "https://www.youtube.com",
    "instagram": "https://www.instagram.com",
    "github": "https://github.com/MxMathe",
}

# Apelidos: o que é falado -> nome real do programa
ALIASES = {
    "vs code": "visual studio code",
    "vscode": "visual studio code",
    "chrome": "google chrome",
}

# Palavras que sobram no começo do termo e atrapalham a busca
PALAVRAS_LIGACAO = {"o", "a", "os", "as", "na", "no", "sobre", "por", "de", "da", "do"}

# Frases que "acordam" o assistente (o reconhecimento pode variar o acento)
FRASES_ATIVACAO = ("olá assistente", "ola assistente", "oi assistente")

# Quantas tentativas seguidas sem fala até voltar ao modo de espera
MAX_SILENCIOS = 2
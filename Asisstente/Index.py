"""
Assistente de voz em Python (somente Windows).

Diga "olá assistente" para ativar. Comandos de exemplo:
    "abrir youtube"
    "abrir o vs code"
    "pesquisar receita de bolo"
    "pesquisar na wikipedia sobre Santos Dumont"
    "tchau"
"""

from Comandos import executar_comando
from Config import FRASES_ATIVACAO, MAX_SILENCIOS
from Texto import detectar_ativacao
from Voz import falar, ouvir


def main():
    ativo = False
    silencios = 0

    print(f"Assistente em espera. Diga '{FRASES_ATIVACAO[0]}' para ativar.")

    while True:
        if not ativo:
            # Modo de espera: escuta em silêncio até ouvir a frase de ativação
            texto = ouvir(timeout=3, phrase_time_limit=6, verboso=False)
            ativou, comando = detectar_ativacao(texto)

            if not ativou:
                continue

            ativo = True
            silencios = 0

            # Se não veio comando junto ("olá assistente"), pergunta
            if not comando:
                falar("Olá! Como posso te ajudar?")
                continue
        else:
            comando = ouvir()

        # Ativo, mas sem fala: após algumas tentativas, volta a dormir
        if not comando:
            silencios += 1

            if silencios >= MAX_SILENCIOS:
                falar("Voltando ao modo de espera.")
                ativo = False

            continue

        silencios = 0

        if "tchau" in comando:
            falar("Até mais!")
            break

        executar_comando(comando)


if __name__ == "__main__":
    main()
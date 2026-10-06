"""Entrada e saída de voz: falar (texto -> áudio) e ouvir (áudio -> texto)."""

import pyttsx3
import speech_recognition as sr

# Criados uma única vez, para não recriar a cada fala
engine = pyttsx3.init()
recognizer = sr.Recognizer()


def falar(texto):
    """Mostra o texto no terminal e fala em voz alta."""
    print(texto)
    engine.say(texto)
    engine.runAndWait()


def ouvir(timeout=5, phrase_time_limit=10, verboso=True):
    """
    Escuta o microfone e devolve o texto em minúsculas ('' se falhar).
    Com verboso=False (modo de espera) não imprime avisos a cada tentativa.
    """
    with sr.Microphone() as source:
        if verboso:
            print("Diga algo...")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        except sr.WaitTimeoutError:
            return ""

    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")

        if verboso:
            print(f"Você disse: {texto}")

        return texto.lower()

    except sr.UnknownValueError:
        if verboso:
            print("Não foi possível entender o áudio.")
    except sr.RequestError:
        print("Erro na requisição ao serviço de reconhecimento.")

    return ""
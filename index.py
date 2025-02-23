import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import pywhatkit

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio.")
        return ""
    except sr.RequestError:
        print("Erro na requisição ao serviço de reconhecimento.")
        return ""


import wikipedia

def executar_comando(comando):
    wikipedia.set_lang("pt")

    if "wikipédia" in comando or "wikipedia" in comando:
        termo = comando.replace("wikipédia", "").replace("wikipedia", "").strip()
        
        if not termo or termo == "":
            resposta = "Por favor, diga o que deseja pesquisar na Wikipedia para que possa te apresentar resultados."
            print(resposta)
            text_to_speech(resposta)
            return

        try:
            resultado = wikipedia.summary(termo, sentences=2)
            print(resultado)
            text_to_speech(resultado)
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Termo muito amplo, tente ser mais específico. Algumas sugestões: {e.options}")
            text_to_speech("O termo é muito amplo, tente ser mais específico.")
        except wikipedia.exceptions.PageError:
            print("Página não encontrada na Wikipedia.")
            text_to_speech("Não encontrei nada sobre isso na Wikipedia.")

    
    elif "abrir youtube" in comando:
        webbrowser.open("https://www.youtube.com")
        text_to_speech("Abrindo YouTube")

    elif "abrir instagram" in comando:
        webbrowser.open("https://www.instagram.com")
        text_to_speech("Abrindo instagram")    
    
    elif "pesquisar" in comando:
        termo = comando.replace("pesquisar", "").strip()
        if termo:
            url = f"https://www.google.com/search?q={termo.replace(' ', '+')}"
            webbrowser.open(url)
            text_to_speech(f"Pesquisando {termo} no Google")
        else:
            text_to_speech("Por favor, diga o que deseja pesquisar.")
    
    else:
        text_to_speech("Comando não reconhecido.")

if __name__ == "__main__":
    text_to_speech("Olá! Como posso te ajudar?")
    while True:
        comando = speech_to_text()
        if "tchau" in comando:
            text_to_speech("Até mais!")
            break
        elif comando:
            executar_comando(comando)
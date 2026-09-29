import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import pywhatkit
import os

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

programas = {
        "steam": r"C:\Program Files (x86)\Steam\steam.exe",
        "bloco de notas": "notepad.exe",
        "paint": "mspaint.exe",
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "discord": os.path.expandvars(r"C:\Users\TeusD\AppData\Local\Discord\Discord.exe"),
    }
def abrir_programa(programa):
    caminho = programas.get(programa)

    if caminho:
        try:
            os.startfile(caminho)
            text_to_speech(f"Abrindo {programa}")
            print(f"Abrindo {programa}...")
        except Exception:
            text_to_speech(f"Não consegui abrir o {programa}.")
    else:
        text_to_speech(f"Não tenho o programa {programa} configurado.")

        

import wikipedia

def executar_comando(comando):
    wikipedia.set_lang("pt")

# WIKIPEDIA
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

# SITES    
    elif "abrir youtube" in comando:
        webbrowser.open("https://www.youtube.com")
        text_to_speech("Abrindo YouTube")

    elif "abrir instagram" in comando:
        webbrowser.open("https://www.instagram.com")
        text_to_speech("Abrindo instagram")

    elif "abrir github" in comando:
            webbrowser.open("https://github.com/MxMathe")
            text_to_speech("Abrindo github")

# PROGRAMAS      
    
    elif "abrir steam" in comando:
        abrir_programa("steam")

    elif "abrir bloco de notas" in comando:
        abrir_programa("bloco de notas")

    elif "abrir chrome" in comando:
            abrir_programa("chrome")

    elif "abrir discord" in comando:
        abrir_programa("discord")

# PESQUISA NO GOOGLE

    elif "pesquisar" in comando:
        termo = comando.replace("pesquisar", "").strip()
        if termo:
            url = f"https://www.google.com/search?q={termo.replace(' ', '+')}"
            webbrowser.open(url)
            text_to_speech(f"Pesquisando {termo} no Google")
        else:
            text_to_speech("Por favor, diga o que deseja pesquisar.")

# COMANDO NÃO RECONHECIDO

    else:
        text_to_speech("Comando não reconhecido.")

# INÍCIO

if __name__ == "__main__":
    text_to_speech("Olá! Como posso te ajudar?")
    while True:
        comando = speech_to_text()
        if "tchau" in comando:
            text_to_speech("Até mais!")
            break
        elif comando:
            executar_comando(comando)
from random import random
from winreg import QueryInfoKey
import speech_recognition
import pyfirmata 
import time
import pyttsx3
import datetime

def randomInt() -> int:
    if random() < 0.5:
        return 0
    else:
        return 1

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5
"""Голосовая функция"""
tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voice', 'ru') 
# Попробовать установить предпочтительный голос
for voice in voices:
    if voice.name == 'Irina':
        tts.setProperty('voice', voice.id)


def greeting():
    """функция приветствия"""
    hour = int(datetime.datetime.now().hour)
    if hour>=6 and hour<12:
        tts.say('доброе утро, сэр') 
        tts.runAndWait()   
    elif hour>=12 and hour<18:
        tts.say('добрый день, сэр')  
        tts.runAndWait()
    elif hour >= 18 and hour < 22:
        tts.say('добрый вечер, сэр')
        tts.runAndWait()
    else:
        tts.say('доброй ночи, сэр')
        tts.runAndWait()


def create_task(command):
    file = None
    filename = ""
    if "задач" in command:
        filename = "todo-list.txt"
    elif "дел" in command:
        filename = "todo-list.txt"
    elif "заметк" in command:
        filename = "remarks.txt"
    file = open(filename, "a", encoding="utf-8")
    if file is None:
        tts.say("Не смогла открыть файл, извините")
        tts.runAndWait()
        return
    tts.say("Что добавить?")
    tts.runAndWait()
    query = listen()
    if query is None:
        tts.say("я не поняла")
        tts.runAndWait()
        return
    file.write(f"! {query}\n")
    if filename == "todo-list.txt":
        speech = "задача"
    else:
        speech = "заметка"
    tts.say(f'{speech} {query} добавлена!')
    tts.runAndWait()


def diod(command: str) -> None:
    tts.say('Включаю')
    tts.runAndWait()
    board = pyfirmata.Arduino('COM3')
        
    if 'красный' in command:
        tts.say('красный')
        tts.runAndWait()
        board.digital[13].write(1)
        time.sleep(1)
        board.digital[13].write(0)
        time.sleep(1)
    elif 'зелёный' in command:
        tts.say('зеленый')
        tts.runAndWait()
        board.digital[12].write(1)
        time.sleep(1)
        board.digital[12].write(0)
        time.sleep(1)
    elif 'синий' in command:
        tts.say('синий')
        tts.runAndWait()
        board.digital[11].write(1)
        time.sleep(1)
        board.digital[11].write(0)
        time.sleep(1)
    elif 'белый' in command:
        tts.say('белый')
        tts.runAndWait()
        board.digital[11].write(1)
        board.digital[12].write(1)
        board.digital[13].write(1)
        time.sleep(5)
        board.digital[11].write(0)
        board.digital[12].write(0)
        board.digital[13].write(0)
    else:
        tts.say('случайный')
        tts.runAndWait()
        board.digital[11].write(randomInt())
        board.digital[12].write(randomInt())
        board.digital[13].write(randomInt())


commandByKey = {
    'привет': greeting,
    'пятница': greeting,
    'доброе утро': greeting,
    'добрый день': greeting,
    'добрый вечер': greeting,

    'список дел': create_task,
    'задач': create_task,
    'заметк': create_task,

    'свет': diod,
    'диод': diod,
    'лампочка': diod
}


def listen() -> str|None: 
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-Ru'). lower()   
        return query
    except speech_recognition.UnknownValueError:
        return None


def execCommand(command: str):
    for key in commandByKey.keys():
        if key in command:
            commandByKey[key](command)
            
if __name__ == '__main__':
    greeting()
    while True:
        tts.say('Что я могу сделать для вас')
        tts.runAndWait()
        command = listen()
        if command is None:
            tts.say("Повторите")
        elif command == "пока":
            break
        execCommand(command)
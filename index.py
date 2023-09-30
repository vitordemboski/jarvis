import speech_recognition as sr
import pyttsx3

from pynput import keyboard

import json

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_KEY')

import openai
openai.api_key = OPENAI_KEY

# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language):
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[0 if language == "pt-BR" else 1].id)


def SpeakText(command, language = "pt-BR"):
	engine = pyttsx3.init()
	change_voice(engine, language)
	engine.say(command)
	engine.runAndWait()
	engine.stop()


r = sr.Recognizer()

def record_text(language="pt-BR"):
	while(1):
		try:
			with sr.Microphone() as source2:
				
				r.adjust_for_ambient_noise(source2, duration=0.2)

				print("IA: Estou ouvindo")

				audio2 = r.listen(source2)

				MyText = r.recognize_google(audio_data=audio2, language=language)

				return MyText
		except sr.RequestError as e:
			print("Could not request resuls: {0}".format(e))
		
		except sr.UnknownValueError:
			print("Unknown error occurred")

def send_to_chatGPT(messages, model="gpt-3.5-turbo"):

	response = openai.ChatCompletion.create(
		model=model,
		messages=messages,
		max_tokens=100,
		n=1,
		stop=None,
		temperature=0.5
	)

	message = response.choices[0].message.content
	messages.append(response.choices[0].message)

	return message

first_command = {"role": "user", "content": 'Por favor finja ser o Jarvis do Homen de Ferro, por favor somente me responda nesse formato de JSON conforme a seguir {"lang": "pt-BR", "content": "o que você me responder"}, lang seria a linguagem  em que você está me respondendo como por exemplo pt-BR ou en-US e content a mensagem de resposta. E sempre que eu te dizer para trocar o idioma você reponde "{"lang":"pt-BR", "content": "Entendido"}" e você sempre vai me responder naquele idioma fornecido'}

messages = [first_command]

def start_recording():
	lang = 'pt-BR'
	text = record_text(lang)
	print(text)
	messages.append({"role": "user", "content": text})
	response = send_to_chatGPT(messages)

	try:
		json_object = json.loads(response)
		lang = json_object["lang"]
		content_text = json_object["content"]
	except:
		lang = "pt-BR"
		content_text = response

	print("IA: {0}".format(content_text))
	
	SpeakText(content_text, lang)

def on_press(key):
	if key == keyboard.Key.f10:
		start_recording()	
		
def on_release(key):
	if key == keyboard.Key.esc:
			# Stop listener
			return False

print('Press and hold "F10" to record and "Esc" to quit')


with keyboard.Listener(
	on_press=on_press,
	on_release=on_release
) as h:
	h.join()





import speech_recognition as sr
import os
import webbrowser
import win32com.client
import openai
import datetime
import re
import pywhatkit

#


apikey = input("Enter your OpenAPI Key: ")

class VoiceAssistant:
    def __init__(self):
        self.speaker = win32com.client.Dispatch('SAPI.SpVoice')
        self.chatStr = ""

    def chat(self, query):
        print(self.chatStr)
        openai.api_key = apikey
        self.chatStr += f"sir: {query}\n Jarvis: "
        response = openai.Completion.create(
            model="gpt-3.5-turbo-0125", 
            prompt=self.chatStr, 
            temperature=0.7, 
            max_tokens=256, 
            top_p=1, 
            frequency_penalty=0, 
            presence_penalty=0
        )
        self.speaker.speak(response["choices"][0]["text"])
        self.chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]

    def ai(self, prompt):
        openai.api_key = apikey
        text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
        response = openai.Completion.create(
            model="gpt-3.5-turbo-0125", 
            prompt=prompt, 
            temperature=0.7, 
            max_tokens=256, 
            top_p=1,
            frequency_penalty=0, 
            presence_penalty=0
        )
        text += response["choices"][0]["text"]
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
            f.write(text)

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                print("Recognizing...")
                query = r.recognize_google(audio, language="en-in")
                print(f"User said: {query}")
                return query
            except Exception as e:
                return "Some Error Occurred. Sorry from Jarvis"

    def extract_phone_number(self, input_string):
        phone_numbers = re.findall(r'\d+', input_string)
        phone_num = ''.join(phone_numbers)
        if phone_num:
            return str(phone_num)
        else:
            return None

    def extract_message(self, input_message):
        message = ''.join(input_message.split('saying')[1:]).strip()
        return message

    def open_website(self, query):
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ["instagram", "www.instagram.com"],
                 ["facebook", "www.facebook.com"], ["python for me", "www.python4me.com"],
                 ["school website", "davdayanandvihar.net"], ["wartex website", "wartex.co.in"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                self.speaker.speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

    def get_time(self):
        hour = datetime.datetime.now().strftime("%H")
        minute = datetime.datetime.now().strftime("%M")
        self.speaker.speak(f"Sir, the time is {hour} hours {minute} minutes")

    def use_ai(self, query):
        self.ai(prompt=query)

    def send_whatsapp_message(self, query):
        message_and_number = query
        phone_number = self.extract_phone_number(message_and_number)
        ph_no = f"+91{phone_number}"
        number = ph_no
        print(number)
        txt_message = self.extract_message(message_and_number)
        current_time = datetime.datetime.now()
        pywhatkit.sendwhatmsg(number, txt_message, current_time.hour, current_time.minute + 1)

    def stop_listening(self):
        pass

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    voice_assistant = VoiceAssistant()
    voice_assistant.speaker.speak("Jarvis A.I")
    while True:
        print("Listening...")
        query = voice_assistant.take_command()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                voice_assistant.speaker.speak(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        if "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            voice_assistant.speaker.speak(f"Sir time is {hour} hours {min} minutes")
        elif "Using artificial intelligence".lower() in query.lower():
            voice_assistant.ai(prompt=query)
        elif "whatsapp".lower() in query.lower():
            message_and_number = query
            phone_number = voice_assistant.extract_phone_number(message_and_number)
            ph_no = f"+91{phone_number}"
            number = ph_no
            print(number)
            txt_message = voice_assistant.extract_message(message_and_number)
            current_time = datetime.datetime.now()
            pywhatkit.sendwhatmsg(number, txt_message, current_time.hour, current_time.minute + 1)
        elif "stop".lower() in query.lower():
            voice_assistant.speaker.speak("ok")
            break
        else:
            print("Chatting...")
            voice_assistant.chat(query)

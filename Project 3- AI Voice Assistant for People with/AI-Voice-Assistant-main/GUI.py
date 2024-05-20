import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from Main import VoiceAssistant
import threading
import speech_recognition as sr

class VoiceAssistantGUI:
    def __init__(self, master):
        self.master = master
        master.title("Jarvis A.I")
        #master.tk.call('source', 'forest-dark.tcl')
        ttk.Style().theme_use('clam')

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        self.label = ttk.Label(master, text="Welcome to Jarvis A.I", font=("Helvetica", 16, "bold"))
        self.label.pack(pady=10)
        ttk.Separator(master, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)

        self.chat_log = tk.Text(master, height=20, width=60, wrap=tk.WORD,
                                font=("Helvetica", 12), bg='#1E1E1E', fg='white',
                                insertbackground='white', selectbackground='#4CAF50',
                                selectforeground='white')
        self.chat_log.pack(pady=10, padx=10)

        self.textbox = ttk.Entry(master, width=40, font=("Helvetica", 12), justify='center')
        self.textbox.pack(pady=10)

        self.send_button = ttk.Button(master, text="Send", command=self.listen_and_respond, style='Accent.TButton')
        self.send_button.pack(pady=10)

        self.mic_button = ttk.Button(master, text="Microphone", command=self.listen_with_microphone, style='Accent.TButton')
        self.mic_button.pack(pady=10)

        self.commands_frame = tk.Frame(master)
        self.commands_frame.pack()

        self.voice_assistant = VoiceAssistant()

        self.suggestions = ["Tell me a joke", "What's the weather like?", "OpenYouTube"]
        self.create_suggestion_buttons()

        self.made_by_label = ttk.Label(master, text="Made by Priyanshu and Yash", font=("Helvetica", 10), foreground='#808080')
        self.made_by_label.pack(side=tk.BOTTOM, pady=10)

        self.listening_thread = None
        self.listening_flag = threading.Event()

    def create_suggestion_buttons(self):
        for suggestion in self.suggestions:
            suggestion_button = ttk.Button(self.commands_frame, text=suggestion, command=lambda s=suggestion: self.suggestion_clicked(s), style='Suggestion.TButton')
            suggestion_button.pack(side=tk.LEFT, padx=5)

    def listen_and_respond(self):
        query = self.textbox.get()
        self.handle_query(query)

    def listen_with_microphone(self):
        query = self.listen_with_speech_recognition()
        if query:
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0, query)
            self.handle_query(query)

    def continuous_listen_and_respond(self):
        while self.listening_flag.is_set():
            query = self.voice_assistant.take_command()
            self.handle_query(query)

    def suggestion_clicked(self, suggestion):
        self.textbox.delete(0, tk.END)
        self.textbox.insert(0, suggestion)
        self.listen_and_respond()

    def update_chat_log(self, message):
        self.chat_log.insert(tk.END, message)
        self.chat_log.see(tk.END)

    def handle_query(self, query):
        if any(keyword in query.lower() for keyword in ["youtube", "wikipedia", "google", "instagram", "facebook", "python for me", "school website", "wartex website"]):
            self.voice_assistant.open_website(query)
        elif "the time" in query:
            self.voice_assistant.get_time()
        elif "using artificial intelligence" in query.lower():
            self.voice_assistant.use_ai(query)
        elif "whatsapp" in query.lower():
            self.voice_assistant.send_whatsapp_message(query)
        elif "stop" in query.lower():
            exit()
        else:
            response = self.voice_assistant.chat(query)
            self.update_chat_log(f"User: {query}\nJarvis: {response}\n\n")

    def stop_listening(self):
        self.listening_flag.clear()
        if self.listening_thread:
            self.listening_thread.join()

    def listen_with_speech_recognition(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio = recognizer.listen(source, timeout=5)
                query = recognizer.recognize_google(audio, language="en-in")
                print(f"User said: {query}")
                return query
            except sr.UnknownValueError:
                print("Speech Recognition could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

if __name__ == '__main__':
    try:
        root = tk.Tk()
        app = VoiceAssistantGUI(root)
        style = ttk.Style()
        style.configure('Accent.TButton', background='#4CAF50', foreground='white', font=("Helvetica", 12))
        style.configure('Suggestion.TButton', font=("Helvetica", 10), padding=5)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")

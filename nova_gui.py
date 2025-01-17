import speech_recognition as sr
from translate import Translator
import tkinter as tk
from tkinter import ttk
import pyttsx3
from tkinter import messagebox
import threading

# Global flag to manage speech recognition state
is_listening = False
recognizer = sr.Recognizer()

def translate_text(text, src_language="hi", target_language="te"):
    translator = Translator(from_lang=src_language, to_lang=target_language)
    return translator.translate(text)

def recognize_and_translate():
    global is_listening
    is_listening = True

    try:
        with sr.Microphone() as source:
            output_label.config(text="🎤 Listening... Speak something in Hindi!")
            loading_label.config(text="🔄 Processing...", foreground="#FF5733")  # Show processing message
            root.update()

            # Continuously listen to audio until is_listening is set to False
            while is_listening:
                audio = recognizer.listen(source, timeout=5)  # Adjust timeout as needed
                try:
                    hindi_text = recognizer.recognize_google(audio, language="hi-IN")
                    hindi_text_label.config(text="🗣️ You said: " + hindi_text)

                    telugu_text = translate_text(hindi_text)
                    telugu_text_label.config(text="🌐 Telugu Translation: " + telugu_text)

                    # Add voice feedback (Text-to-Speech)
                    engine = pyttsx3.init()
                    engine.say(f"The translation in Telugu is: {telugu_text}")
                    engine.runAndWait()

                    output_label.config(text="✔️ Translation Complete!")
                    
                    break
                except sr.UnknownValueError:
                    output_label.config(text="⚠️ Could not understand audio.")
                except sr.RequestError as e:
                    output_label.config(text=f"⚠️ Could not request results from Google Speech Recognition service; {e}")
                except Exception as e:
                    output_label.config(text="⚠️ An unexpected error occurred.")
                    print(f"Error: {e}")
            else:
                output_label.config(text="🛑 Listening stopped manually.")
                loading_label.config(text="")  # Clear the processing label
    except Exception as e:
        output_label.config(text="⚠️ An error occurred.")
        print(f"Error: {e}")
    finally:
        is_listening = False
        stop_button.config(state="disabled")
        recognize_button.config(state="normal")

def stop_listening():
    global is_listening
    is_listening = False
    output_label.config(text="🛑 Listening stopped.")
    stop_button.config(state="disabled")
    recognize_button.config(state="normal")
    loading_label.config(text="")  # Clear processing label when stopped

def start_listening_thread():
    stop_button.config(state="normal")
    recognize_button.config(state="disabled")
    loading_label.config(text="🔄 Processing...", foreground="#FF5733")  # Show processing message when started
    threading.Thread(target=recognize_and_translate, daemon=True).start()

# Set up the main application window
root = tk.Tk()
root.title("Nova: Hindi to Telugu Translator")

# Dynamically resize window based on screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size (80% of the screen size)
root.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")
root.resizable(True, True)  # Allow resizing

# Create a gradient background
canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill="both", expand=True)

# Create a gradient from top to bottom
gradient = tk.PhotoImage(width=screen_width, height=screen_height)
canvas.create_image(0, 0, anchor="nw", image=gradient)

# Add a frame to center the text and button
frame = tk.Frame(root, bg="#ffffff", bd=5, relief="groove", padx=30, pady=30)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Add labels and button to the frame
output_label = ttk.Label(
    frame,
    text="Press the button to start",
    font=("Comic Sans MS", 20, "bold"),
    background="#ffffff",
    foreground="#FF5733",  # Vibrant Red-Orange color
)
output_label.pack(pady=30)

hindi_text_label = ttk.Label(
    frame,
    text="",
    font=("Arial", 16),
    background="#ffffff",
    foreground="#8B32FF",  # Elegant Purple color
)
hindi_text_label.pack(pady=15)

telugu_text_label = ttk.Label(
    frame,
    text="Telugu Translation: ",
    font=("Arial", 16),
    background="#ffffff",
    foreground="#1E88E5",  # Blue color
)
telugu_text_label.pack(pady=15)

loading_label = ttk.Label(
    frame,
    text="",
    font=("Arial", 14, "italic"),
    background="#ffffff",
    foreground="#FF5733",  # Color for loading message
)
loading_label.pack(pady=15)

recognize_button = ttk.Button(
    frame,
    text="🎙️ Start to Speak",
    command=start_listening_thread,  # Start the listening in a separate thread
    style="Custom.TButton",
)
recognize_button.pack(pady=15)

stop_button = ttk.Button(
    frame,
    text="🛑  Stop Listening",
    command=stop_listening,
    style="Custom.TButton",
)
stop_button.pack(pady=15)
stop_button.config(state="disabled")  # Initially disable the stop button

# Customize button style with a modern touch
style = ttk.Style()
style.configure(
    "Custom.TButton",
    font=("Arial", 16, "bold"),
    padding=15,
    foreground="black",
    background="#4CAF50",  # Green color
    borderwidth=2,
    relief="raised",
    anchor="center",
    focuscolor="none",
    width=20
)

# Add hover effect for buttons
style.map(
    "Custom.TButton",
    background=[("active", "#45A049")],  # Darker green on hover
    foreground=[("active", "black")],
)

# Run the GUI
root.mainloop()

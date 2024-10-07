import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, scrolledtext
import requests


# Function to call the NeurochainAI API
def translate_text():
    text_to_translate = text_entry.get("1.0", tk.END).strip()  # Get text from the chat input
    selected_language = language.get()

    if not text_to_translate:
        messagebox.showwarning("Input Error", "Please enter text to translate.")
        return

    API_URL = "https://ncmb.neurochain.io/tasks/message"
    API_KEY = api_key_entry.get()

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Translate the following English text to {selected_language}: {text_to_translate}"

    data = {
        "model": "Mistral-7B-Instruct-v0.2-GPTQ",
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.6,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 1.1
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()

        translation = response.json().get('result', 'No translation found.')
        update_chat("You: " + text_to_translate)
        update_chat("Translator: " + translation)

        # Clear the text entry for next input
        text_entry.delete("1.0", tk.END)

    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("Error", f"HTTP error occurred: {http_err}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def update_chat(message):
    chat_area.configure(state='normal')  # Allow editing
    chat_area.insert(tk.END, message + "\n")  # Insert message into chat area
    chat_area.configure(state='disabled')  # Disable editing
    chat_area.yview(tk.END)  # Scroll to the end


# Set up the main application window
app = tk.Tk()
app.title("NeurochainAI Translator Chat")
app.geometry("400x500")
app.configure(bg='lightblue')

# Set a custom font
custom_font = tkFont.Font(family="Helvetica", size=12)

# Create frames for better layout
input_frame = tk.Frame(app, bg='lightblue')
input_frame.pack(pady=20)

# API Key Entry
tk.Label(input_frame, text="Enter your API Key:", bg='lightblue').pack()
api_key_entry = tk.Entry(input_frame, width=50)
api_key_entry.pack(pady=10)

# Chat area
chat_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, state='disabled', height=15, bg='lightyellow',
                                      font=custom_font)
chat_area.pack(padx=10, pady=10, fill=tk.BOTH)

# Language selection
language = tk.StringVar(value="French")
tk.Label(input_frame, text="Select target language:", bg='lightblue').pack()
language_menu = tk.OptionMenu(input_frame, language, "French", "Spanish", "German", "Italian")
language_menu.pack(pady=10)

# Text Entry
tk.Label(input_frame, text="Enter text to translate:", bg='lightblue').pack()
text_entry = tk.Text(input_frame, height=4, width=30)
text_entry.pack(pady=10)

# Translate Button
translate_button = tk.Button(input_frame, text="Translate", command=translate_text,
                             bg='green', fg='white', relief='raised', font=custom_font)
translate_button.pack(pady=10)

# Run the application
app.mainloop()

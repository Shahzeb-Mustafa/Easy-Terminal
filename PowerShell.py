import os
import re
import sys
import subprocess
import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import threading

GOOGLE_API_KEY = "place your api key here"


class NaturalLanguageTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Easy Terminal for PowerShell")
        self.root.configure(bg='navy blue')

        self.terminal_font = ('Courier', 10)
        self.text_color = 'white'
        self.bg_color = 'navy blue'

        self.command_history = []
        self.history_index = 0
        self.current_directory = os.getcwd()

        self.terminal = scrolledtext.ScrolledText(root, bg=self.bg_color, fg=self.text_color,
                                                  font=self.terminal_font, insertbackground=self.text_color)
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.input_start = "1.0"
        self.input_active = False
        self.current_command = ""

        self.setup_genai()

        self.terminal.bind('<Return>', self.handle_return)
        self.terminal.bind('<BackSpace>', self.handle_backspace)
        self.terminal.bind('<Up>', self.handle_up)
        self.terminal.bind('<Down>', self.handle_down)

        welcome_msg = "Welcome to Natural Language Terminal for PowerShell\n"
        welcome_msg += "- Type PowerShell commands OR natural language\n"
        welcome_msg += "- Type 'exit' or 'quit' to close\n\n"
        self.terminal.insert(tk.END, welcome_msg)
        self.display_prompt()

        self.terminal.config(state=tk.NORMAL)
        self.terminal.focus_set()

    def setup_genai(self):
        try:
            genai.configure(api_key=GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            self.append_output(f"Error initializing AI: {str(e)}\n")

    def display_prompt(self):
        self.enable_text_widget()
        prompt = f"{self.current_directory}> "
        self.terminal.insert(tk.END, prompt)
        self.terminal.see(tk.END)
        self.input_start = self.terminal.index(tk.INSERT)
        self.input_active = True

    def append_output(self, text):
        self.enable_text_widget()
        self.terminal.insert(tk.END, text)
        self.terminal.see(tk.END)

    def get_current_command(self):
        try:
            command = self.terminal.get(self.input_start, tk.END)
            return command.strip()
        except:
            return ""

    def handle_return(self, event):
        self.terminal.config(state=tk.NORMAL)
        command = self.get_current_command()
        self.terminal.insert(tk.END, "\n")

        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)

            if command.lower() in ['exit', 'quit']:
                self.root.quit()
                return "break"

            if command.lower() in ['clear', 'cls']:
                self.clear_terminal()
                return "break"

            threading.Thread(target=self.process_command, args=(command,), daemon=True).start()
        else:
            self.display_prompt()
        return "break"

    def handle_backspace(self, event):
        if self.terminal.compare(tk.INSERT, '<=', self.input_start):
            return "break"
        return

    def handle_up(self, event):
        if not self.command_history or self.history_index <= 0:
            return "break"
        self.terminal.delete(self.input_start, tk.END)
        self.history_index -= 1
        self.terminal.insert(self.input_start, self.command_history[self.history_index])
        return "break"

    def handle_down(self, event):
        if not self.command_history:
            return "break"
        self.terminal.delete(self.input_start, tk.END)
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.terminal.insert(self.input_start, self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
        return "break"

    def clear_terminal(self):
        self.terminal.delete("1.0", tk.END)
        self.display_prompt()

    def detect_command_type(self, command):
        powershell_keywords = ["Get-", "Set-", "New-", "Remove-", "Start-", "Stop-", "Restart-", "Test-", "Invoke-"]
        if any(keyword in command for keyword in powershell_keywords):
            return 'powershell'
        return 'natural'

    def process_command(self, command):
        command_type = self.detect_command_type(command)

        if command_type == 'powershell':
            output = self.execute_powershell_command(command)
            self.append_output(output)
        else:
            self.append_output(f"Translating: {command}\n")
            try:
                prompt = f"""
You are an AI that converts natural language requests into PowerShell commands.
Current directory: {self.current_directory}
User query: {command}
Provide ONLY the PowerShell command without any explanations.
If no valid command exists, return "ERROR: Unable to translate."
                """
                response = self.model.generate_content(prompt)
                translated_command = response.text.strip()

                if translated_command.startswith("ERROR:"):
                    self.append_output(f"{translated_command}\n")
                    self.display_prompt()
                    return

                self.append_output(f"Executing: {translated_command}\n")
                output = self.execute_powershell_command(translated_command)
                self.append_output(output)
            except Exception as e:
                self.append_output(f"Error processing: {str(e)}\n")

        self.display_prompt()

    def execute_powershell_command(self, command):
        try:
            process = subprocess.Popen(["powershell", "-Command", command],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, cwd=self.current_directory)
            stdout, stderr = process.communicate()
            return stderr if stderr else stdout
        except Exception as e:
            return f"Error executing: {str(e)}\n"

    def enable_text_widget(self):
        self.terminal.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = NaturalLanguageTerminal(root)
    root.mainloop()


if __name__ == "__main__":
    main()

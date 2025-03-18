import os
import re
import sys
import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox
import google.generativeai as genai
import threading

GOOGLE_API_KEY = "AIzaSyA1RJISbzG7WJ0T_ZRQIEVj_WWkhiHKml4"  # Replace with your actual API key


class NaturalLanguageTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Easy Terminal for CMD")
        self.root.configure(bg='black')

        # Set up the terminal appearance
        self.terminal_font = ('Courier', 10)
        self.text_color = 'white'
        self.bg_color = 'black'

        # Command history
        self.command_history = []
        self.history_index = 0

        # Current working directory
        self.current_directory = os.getcwd()

        # Create the terminal text area
        self.terminal = scrolledtext.ScrolledText(
            root,
            bg=self.bg_color,
            fg=self.text_color,
            font=self.terminal_font,
            insertbackground=self.text_color
        )
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Terminal state tracking
        self.input_start = "1.0"
        self.input_active = False
        self.current_command = ""

        # Setup Google Generative AI with Gemini
        self.setup_genai()

        # Bind events
        self.terminal.bind('<Key>', self.handle_keypress)
        self.terminal.bind('<Return>', self.handle_return)
        self.terminal.bind('<BackSpace>', self.handle_backspace)
        self.terminal.bind('<Delete>', self.handle_delete)
        self.terminal.bind('<Up>', self.handle_up)
        self.terminal.bind('<Down>', self.handle_down)
        self.terminal.bind('<Left>', self.handle_left)
        self.terminal.bind('<Right>', self.handle_right)
        self.terminal.bind('<Home>', self.handle_home)
        self.terminal.bind('<End>', self.handle_end)
        self.terminal.bind('<Control-c>', self.handle_interrupt)
        self.terminal.bind('<Control-l>', self.handle_clear)
        self.terminal.bind("<Tab>", self.handle_tab)

        # Welcome message
        welcome_msg = "Welcome to Natural Language Terminal\n"
        welcome_msg += "- Type normal CMD commands OR natural language\n"
        welcome_msg += "- Natural language will be automatically detected and translated\n"
        welcome_msg += "- Type 'exit' or 'quit' to close the terminal\n\n"
        welcome_msg += "- __Created by Wasif Sohail with ♥__ \n\n"
        self.terminal.insert(tk.END, welcome_msg)

        # Initial prompt
        self.display_prompt()

        # Disable text widget configuration for proper terminal behavior
        self.terminal.config(state=tk.NORMAL)

        # Set focus on terminal
        self.terminal.focus_set()

    def setup_genai(self):
        """Set up Google Generative AI with Gemini"""
        try:
            # Configure the API key
            genai.configure(api_key=GOOGLE_API_KEY)

            # Initialize the Gemini model
            self.model = genai.GenerativeModel('gemini-1.5-flash')

        except Exception as e:
            self.append_output(f"Error initializing Generative AI: {str(e)}\n")

    def disable_text_widget(self):
        """Disable user editing in areas they shouldn't edit"""
        self.terminal.config(state=tk.DISABLED)

    def enable_text_widget(self):
        """Enable user editing"""
        self.terminal.config(state=tk.NORMAL)

    def display_prompt(self):
        """Display the terminal prompt with current directory"""
        self.enable_text_widget()
        prompt = f"{self.current_directory}> "
        self.terminal.insert(tk.END, prompt)
        self.terminal.see(tk.END)
        self.input_start = self.terminal.index(tk.INSERT)
        self.input_active = True

    def append_output(self, text):
        """Append output text to the terminal"""
        self.enable_text_widget()
        self.terminal.insert(tk.END, text)
        self.terminal.see(tk.END)

    def get_current_command(self):
        """Get the current command from the terminal"""
        try:
            command = self.terminal.get(self.input_start, tk.END)
            return command.strip()
        except:
            return ""

    def handle_keypress(self, event):
        """Handle key press events"""
        # Ignore events like Shift, Control, etc.
        if len(event.char) == 0 or event.char == '\r' or event.char == '\t':
            return

        # Ignore if cursor is before input_start
        if self.terminal.compare(tk.INSERT, '<', self.input_start):
            self.terminal.mark_set(tk.INSERT, tk.END)

        # Check if we need to enable editing
        cursor_pos = self.terminal.index(tk.INSERT)
        if self.terminal.compare(cursor_pos, '<', self.input_start):
            self.terminal.mark_set(tk.INSERT, tk.END)

    def handle_return(self, event):
        """Handle Return key - process the command"""
        self.terminal.config(state=tk.NORMAL)
        command = self.get_current_command()
        self.terminal.insert(tk.END, "\n")

        if command:
            self.command_history.append(command)
            self.history_index = len(self.command_history)

            # Exit command handling
            if command.lower() in ['exit', 'quit']:
                self.root.quit()
                return "break"

            # Clear command handling
            if command.lower() in ['clear', 'cls']:
                self.clear_terminal()
                return "break"

            # Process command in a separate thread
            threading.Thread(target=self.process_command, args=(command,), daemon=True).start()
        else:
            self.display_prompt()

        return "break"

    def handle_backspace(self, event):
        """Handle backspace key"""
        if self.terminal.compare(tk.INSERT, '<=', self.input_start):
            return "break"
        return

    def handle_delete(self, event):
        """Handle delete key"""
        if self.terminal.compare(tk.INSERT, '<', self.input_start):
            return "break"
        return

    def handle_left(self, event):
        """Handle left arrow key"""
        if self.terminal.compare(tk.INSERT, '<=', self.input_start):
            return "break"
        return

    def handle_home(self, event):
        """Handle home key"""
        self.terminal.mark_set(tk.INSERT, self.input_start)
        return "break"

    def handle_end(self, event):
        """Handle end key"""
        self.terminal.mark_set(tk.INSERT, tk.END)
        return "break"

    def handle_right(self, event):
        """Handle right arrow key"""
        return

    def handle_up(self, event):
        """Handle up arrow key - navigate command history"""
        if not self.command_history or self.history_index <= 0:
            return "break"

        self.terminal.delete(self.input_start, tk.END)
        self.history_index -= 1
        self.terminal.insert(self.input_start, self.command_history[self.history_index])
        return "break"

    def handle_down(self, event):
        """Handle down arrow key - navigate command history"""
        if not self.command_history:
            return "break"

        self.terminal.delete(self.input_start, tk.END)
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            self.terminal.insert(self.input_start, self.command_history[self.history_index])
        else:
            self.history_index = len(self.command_history)
        return "break"

    def handle_interrupt(self, event):
        """Handle Ctrl+C interrupt"""
        self.append_output("\n^C\n")
        self.display_prompt()
        return "break"

    def handle_clear(self, event):
        """Handle Ctrl+L (clear)"""
        self.clear_terminal()
        return "break"

    def handle_tab(self, event):
        """Handle tab completion"""
        command = self.get_current_command()

        # Basic implementation of tab completion for files in current directory
        if " " in command:
            parts = command.split(" ")
            prefix = parts[-1]

            try:
                files = os.listdir(self.current_directory)
                matches = [f for f in files if f.startswith(prefix)]

                if len(matches) == 1:
                    self.terminal.delete(f"{self.input_start}+{len(command) - len(prefix)}", tk.END)
                    self.terminal.insert(tk.INSERT, matches[0])
                elif len(matches) > 1:
                    # Show options
                    self.terminal.insert(tk.END, "\n" + "  ".join(matches) + "\n")
                    self.display_prompt()
                    self.terminal.insert(tk.INSERT, command)
            except Exception as e:
                # Silently handle tab completion errors
                pass

        return "break"

    def clear_terminal(self):
        """Clear the terminal screen"""
        self.terminal.delete("1.0", tk.END)
        self.display_prompt()

    def detect_command_type(self, command):
        """
        Detect if the command is a CMD command or natural language
        Returns: 'cmd' or 'natural'
        """
        # Common CMD commands regex pattern
        cmd_pattern = r'^(cd|dir|mkdir|rmdir|del|copy|move|find|echo|type|cmd|exit|cls|attrib|ren|md|rd|xcopy|more|help|systeminfo|ipconfig|ping|tracert|netstat|net|tasklist|taskkill|time|date|chdir|pushd|popd|where|fc|comp|shutdown|set|start|assoc|ftype|title|tree|prompt|path|for|call|if|ver|vol|label|chkdsk|diskpart|sfc|cipher|powershell|whoami|color|robocopy|forfiles|sort|findstr)( .*)?$'

        # Check if it's a recognized CMD command
        if re.match(cmd_pattern, command) or '|' in command or '&' in command or '>' in command:
            return 'cmd'

        # Check if it contains flags or options (/a, /?)
        if ' /' in command:
            return 'cmd'

        # Check if it seems to be a path or has quotes
        if ('\\' in command or ':' in command or
                ('"' in command and '"' in command[command.index('"') + 1:]) or
                ("'" in command and "'" in command[command.index("'") + 1:])):
            return 'cmd'

        # By default, try to interpret as natural language if it's more than one word
        # or contains certain natural language indicators
        natural_indicators = ['show', 'list', 'display', 'find', 'get', 'what', 'how', 'create',
                              'make', 'write', 'search', 'tell', 'give', 'count', 'calculate',
                              'please', 'help', 'can', 'could', 'would', 'do', 'does']

        command_words = command.lower().split()
        if len(command_words) > 1 or any(word in natural_indicators for word in command_words):
            return 'natural'

        # Default to CMD if we're not sure
        return 'cmd'

    def process_command(self, command):
        """Process the command entered by the user"""
        # Detect if it's a CMD command or natural language
        command_type = self.detect_command_type(command)

        if command_type == 'cmd':
            # Try to execute directly
            output = self.execute_cmd_command(command)
            self.append_output(output)
        else:
            # Try to translate natural language to CMD
            self.append_output(f"Translating: {command}\n")

            try:
                # Create prompt for Gemini
                prompt = f"""
You are an expert in translating natural language queries into Windows CMD commands.

Current working directory: {self.current_directory}

User query: {command}

Determine if this query is already a valid CMD command. If it is, return "VALID_COMMAND".

If it's natural language, translate it into a valid CMD command that would run in a Windows CMD terminal.
Provide ONLY the CMD command without any explanations, prefixes, or comments.
Do not include ANY extra text, markdown formatting, or code blocks in your response.
Your response must contain exactly one line with just the CMD command.

Be lenient with natural language queries and try to find the most reasonable CMD equivalent.
Only respond with "ERROR: Unable to translate to a valid CMD command." if you're absolutely certain 
there is no reasonable CMD command that can satisfy the request.

If the query is asking for something that could be harmful or destructive, respond with 
"ERROR: This command could be potentially harmful."
                """

                # Get response from Gemini
                response = self.model.generate_content(prompt)
                translated_command = response.text.strip()

                # Clean up response - remove any markdown or extra text that might appear
                translated_command = self.clean_llm_response(translated_command)

                # Check if it's already a valid command (no need for translation)
                if translated_command == "VALID_COMMAND":
                    self.append_output(f"Executing as-is: {command}\n")
                    output = self.execute_cmd_command(command)
                # Check for errors in translation
                elif translated_command.startswith("ERROR:"):
                    self.append_output(f"{translated_command}\n")
                    self.display_prompt()
                    return
                # Execute the translated command
                else:
                    self.append_output(f"Executing: {translated_command}\n")
                    output = self.execute_cmd_command(translated_command)

                self.append_output(output)

            except Exception as e:
                self.append_output(f"Error processing command: {str(e)}\n")

        self.display_prompt()

    def clean_llm_response(self, response):
        """Clean LLM response from markdown, code blocks, or extra text"""
        if response.startswith("ERROR:"):
            return response

        if response == "VALID_COMMAND":
            return response

        response = re.sub(r'```(?:batch|cmd)?\s*(.*?)\s*```', r'\1', response, flags=re.DOTALL)

        lines = [line.strip() for line in response.split('\n') if line.strip() and not line.strip().startswith('#')]
        if lines:
            return lines[0]

        return response

    def execute_cmd_command(self, cmd_command):
        """Execute a CMD command and return the output"""
        try:
            # Handle built-in commands like cd
            if cmd_command.strip().startswith("cd ") or cmd_command.strip() == "cd":
                dir_part = cmd_command.strip()[3:].strip() if cmd_command.strip() != "cd" else ""

                # Handle special case for home directory
                if dir_part == "" or dir_part == "%HOMEPATH%":
                    target_dir = os.path.expanduser("~")
                # Handle parent directory
                elif dir_part == "..":
                    target_dir = os.path.dirname(self.current_directory)
                # Handle absolute paths
                elif os.path.isabs(dir_part) or ":" in dir_part:
                    target_dir = dir_part
                # Handle relative paths
                else:
                    target_dir = os.path.join(self.current_directory, dir_part)

                if os.path.exists(target_dir) and os.path.isdir(target_dir):
                    self.current_directory = os.path.abspath(target_dir)
                    return f"Changed directory to {self.current_directory}\n"
                else:
                    return f"The system cannot find the path specified: {dir_part}\n"

            # Handle dir command
            if cmd_command.strip().lower() == "dir":
                try:
                    files = os.listdir(self.current_directory)
                    result = f" Directory of {self.current_directory}\n\n"
                    for file in files:
                        full_path = os.path.join(self.current_directory, file)
                        if os.path.isdir(full_path):
                            result += f"{file.ljust(30)} <DIR>\n"
                        else:
                            size = os.path.getsize(full_path)
                            result += f"{file.ljust(30)} {size:,} bytes\n"
                    return result
                except Exception as e:
                    return f"Error listing directory: {str(e)}\n"

            # For all other commands
            process = subprocess.Popen(
                cmd_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.current_directory
            )
            stdout, stderr = process.communicate()

            if stderr:
                return stderr
            elif stdout:
                return stdout
            else:
                return ""

        except Exception as e:
            return f"Error executing command: {str(e)}\n"


def main():
    root = tk.Tk()
    root.geometry("800x600")
    app = NaturalLanguageTerminal(root)
    root.mainloop()


if __name__ == "__main__":
    main()
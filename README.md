# Custom Linux Terminal & Script Generator

This project is a Python-based GUI terminal and Bash script generator powered by Google's Gemini AI. It allows users to execute Linux commands, enforce input restrictions, and generate executable Bash scripts from natural language descriptions.

## Features
- **Custom Linux Terminal**: Linux shell
- **Bash Script Generator**: Converts natural language task descriptions into Bash scripts using Gemini AI.
- **Interactive Interface**: Built with Tkinter for ease of use.
- **Command Execution**: Supports running Bash commands directly within the application.
- **Script Saving**: Save generated Bash scripts and make them executable automatically.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Tkinter (included with Python standard library)
- Google Generative AI SDK

### Setup
1. Clone this repository:
   ```sh
   git clone https://github.com/your-repo/custom-linux-terminal.git
   cd custom-linux-terminal
   ```
2. Install dependencies:
   ```sh
   pip install google-generativeai
   ```
3. Replace `GEMINI_API_KEY` in the script with your actual Google Gemini API key.
4. Run the application:
   ```sh
   python terminal_gui.py
   ```

## Usage
### Terminal Mode
- Start typing commands after the prompt (`$` sign).
- Commands execute on pressing `Enter`.
- The terminal prevents accidental deletion of the prompt.
- Type `clear` to reset the terminal.

### Script Generator Mode
1. Enter a description of the task (e.g., "List all .txt files").
2. Click "Generate Script" to create a Bash script.
3. Review the script in the text box.
4. Click "Save Script" to store it as an executable `.sh` file.

## Notes
- The AI-generated commands may require verification before execution.
- Running incorrect Bash commands may affect your system. Use with caution.

## License
This project is open-source. Feel free to modify and use it as needed.

## Author
Developed by Haider.


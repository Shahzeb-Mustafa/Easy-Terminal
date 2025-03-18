# 🖥️ Windows Natural Language Terminal

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-brightgreen.svg)
![Python](https://img.shields.io/badge/python-3.7+-yellow.svg)
![Status](https://img.shields.io/badge/status-beta-orange.svg)

> **Transform how you interact with your Windows command line!** Type natural language commands and watch them translate automatically to CMD instructions.

## ✨ Features

- 🗣️ **Natural Language Processing** - Type commands as you would speak them
- 🔄 **Real-time Translation** - Instantly converts plain English to CMD commands
- 💻 **Familiar Interface** - Classic terminal look with modern AI capabilities
- 📝 **Command History** - Easily access previously used commands
- 🔍 **Tab Completion** - Quick file and folder name completion
- 🛡️ **Safety Checks** - Protects against potentially harmful commands
- 🔌 **Powered by Google Gemini** - Cutting-edge language model for accurate translations

## 🖼️ Screenshots

![Natural Language Terminal Screenshot](https://via.placeholder.com/800x500?text=Natural+Language+Terminal)

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Windows 8/10/11
- Google API Key for Gemini

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/windows-natural-language-terminal.git
   cd windows-natural-language-terminal
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API key:
   - Get an API key from the [Google AI Studio](https://makersuite.google.com/)
   - Replace the placeholder API key in the code:
     ```python
     GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
     ```

4. Run the application:
   ```bash
   python natural_language_terminal.py
   ```

## 💡 Usage Examples

| Natural Language | Translated CMD |
|------------------|----------------|
| "Show me all files in this folder" | `dir` |
| "Create a folder named projects" | `mkdir projects` |
| "What's my IP address?" | `ipconfig` |
| "Show running processes" | `tasklist` |
| "Find all text files" | `dir *.txt` |
| "Show system information" | `systeminfo` |
| "Check disk space" | `wmic logicaldisk get size,freespace,caption` |
| "Create a new text file called notes" | `echo. > notes.txt` |

## 🛠️ How It Works

1. **Input Detection** - The system determines if your input is a standard CMD command or natural language
2. **AI Translation** - If natural language is detected, the Gemini AI model translates it to CMD
3. **Command Execution** - The system runs the command and displays the output
4. **Learning** - The system improves with usage as you work with it

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Up/Down` | Navigate command history |
| `Tab` | Auto-complete filenames |
| `Ctrl+C` | Interrupt current command |
| `Ctrl+L` | Clear screen |
| `Home/End` | Move to start/end of line |

## 🔧 Customization

You can customize the terminal appearance by modifying these variables:

```python
self.terminal_font = ('Courier', 10)
self.text_color = '#00FF00'  # Green text
self.bg_color = 'black'
```

## 🔍 Troubleshooting

- **API Key Issues**: Ensure your Google API key is valid and has access to the Gemini models
- **Translation Problems**: For complex queries, try simplifying your language
- **Performance**: If the terminal becomes slow, consider clearing the history with `cls`

## 🔮 Future Enhancements

- [ ] Support for PowerShell commands
- [ ] Custom command aliases
- [ ] Multi-language support
- [ ] Cloud synchronization of command history
- [ ] Theme customization options
- [ ] Plugin system for extended functionality

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgements

- Created with ♥ by Wasif Sohail
- Powered by Google Gemini AI
- Thanks to all contributors and testers

---

⭐ Star this repository if you find it useful! ⭐

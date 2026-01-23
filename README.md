# Python Coding Challenges

An interactive web platform for learning and practicing Python programming! Solve coding challenges ranging from elegant one-liners to full scripts with input handling.

## 🎯 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   ```
   http://localhost:5000
   ```

4. **Want your own challenges?** See [SETUP_YOUR_CHALLENGES.md](SETUP_YOUR_CHALLENGES.md) for easy customization!

## Features

- 🎯 **15 Progressive Challenges** - From easy to hard difficulty levels
- 💻 **Full Python Support** - Multi-line code, imports, functions, and more!
- 📥 **Input Handling** - Practice parsing stdin with `input()` for realistic challenges
- ✅ **Automated Testing** - Each challenge has test cases with inputs and expected outputs
- 🎨 **Modern Dark UI** - Clean, professional interface inspired by VS Code
- 📊 **Progress Tracking** - Keep track of completed challenges
- ⌨️ **Keyboard Shortcuts** - Ctrl/Cmd + Enter to run code
- 🔄 **Split-Screen Interface** - Challenge description on the left, code editor on the right
- 💾 **Code Saving** - Auto-save to localStorage and server-side storage
- ⚙️ **Customizable Editor** - Settings for themes, indentation, font size, and more
- 🎯 **Auto-Save** - Your code is automatically saved as you type

## What's New

The editor now supports:
- ✨ **Multi-line Python scripts** (no more one-liner restriction!)
- 📝 **Input/Output challenges** - Read from stdin using `input()`, write with `print()`
- 📦 **Imports** - Use any Python standard library module
- 🎓 **Real-world scenarios** - Parse inputs, format outputs, solve practical problems

See [EXAMPLES.md](EXAMPLES.md) for detailed examples and patterns!

## Installation

1. Clone the repository:
```bash
git clone https://github.com/BernieCodez/one-liner.git
cd one-liner
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## How to Play

1. Read the challenge description on the left panel
2. Write your Python solution in the editor (can be single or multiple lines)
3. For challenges with input, check the test cases to see what input will be provided
4. Use `input()` to read from stdin and `print()` to output your answer
5. Click "Run Code" or press Ctrl/Cmd + Enter
6. View test results in the console below (shows input, expected output, and your output)
7. Once all tests pass, move to the next challenge!
8. Your code is automatically saved - come back anytime to continue!

## Customizing Challenges

Want to create your own problem set? It's easy!

1. Edit [setup_challenges.py](setup_challenges.py) with your 15 challenges
2. Run `python setup_challenges.py`
3. Restart the app

See [SETUP_YOUR_CHALLENGES.md](SETUP_YOUR_CHALLENGES.md) for detailed instructions.

## Challenge Topics

- List comprehensions and one-liners
- String manipulation
- Input/Output parsing
- Mathematical calculations
- Dictionary comprehensions
- Lambda functions
- Nested data structures
- Mathematical operations
- Advanced Python techniques

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Design**: Custom CSS with VS Code-inspired theme

## Contributing

Feel free to add more challenges or improve the platform! Pull requests are welcome.

## License

MIT License

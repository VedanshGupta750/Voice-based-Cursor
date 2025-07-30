
# 🤖 AI Coding Assistant

Welcome to your all-in-one **Voice based Cursor**! This assistant executes your natural language requests, handles coding workflows, automates file management, opens websites, and searches YouTube—all powered by cutting-edge language models and automation tools. 🚀

---

## ✨ What This Project Does

- **Conversational AI assistant:** Chat with the AI​ to plan, enhance, and execute coding tasks.
- **Command runner:** Safely run system commands right from your chat.
- **File creator:** Generate, modify, and organize code files automatically into a `generated/` folder.
- **Website/YouTube opener:** Open websites or search YouTube with a simple request.
- **Smart orchestration:** All actions are organized based on your intent using advanced LangChain & LangGraph workflows.
- **Plug-and-play tools:** Easily add your own tool functions for customized automation.

---

## 🛠️ Tech Stack

| 🚩 Technology/Library           | 🌟 Role / Purpose                                     |
| ------------------------------   | ----------------------------------------------------- |
| Python 3.10+                     | Main programming language                             |
| LangChain / LangChain-Community  | LLM orchestration, tool integration, coding agents    |
| LangGraph                        | Declarative, stateful graph-based workflow management |
| Google Generative AI (Gemini)    | LLM backend for natural language and logic            |
| And many others!                 | See all in `requirements.txt` for full dependency set |

---

## 📦 Installation

1. **Clone the Repository**
   ```
   git clone https://github.com/VedanshGupta750/Voice-based-Cursor.git
   cd voice_enabled
   ```

2. **(Recommended) Create Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install All Requirements**  
   (👀 Double check that you’re using Python 3.10 or newer)
   ```
   pip install -r requirements.txt
   ```

4. **Set up API Keys & Environment Vars**
   - Create a `.env` file at your project root.
     ```
     GEMINI_API_KEY=your-google-gemini-api-key
     ```

5. **Run the Assistant**
   ```
   python main.py
   ```

---

## 🤝 How to Use

- **Chat with the assistant** via terminal, notebook, or web UI (optional).
- **Request code files or scripts:**  
  *You:* “Create a Python script to print Hello, World!”  
  *AI:* (Creates `generated/hello.py`)
- **Execute code or system commands:**  
  *You:* `run_command(cmd="python generated/hello.py")`  
  *AI:* (Executes & shows output)
- **Open a website or search YouTube:**  
  *You:* “Open GitHub” or “Search YouTube for Lo-fi music”
- **Everything generated is stored safely under `generated/`!**

---

## 📝 Customization & Extensibility

- **Add new tools:** Just define Python functions and decorate with `@tool`.
- **Integrate more models:** Swap out the language model if needed.
- **Plug with Flask/Streamlit:** Make a full web-based interface for even more sparkle!

---


## 📜 Example Commands

```
User: Write a Python file that scrapes quotes from a website.
Assistant: (Creates `generated/scraper.py`)

User: run_command(cmd="python generated/scraper.py")
Assistant: (Executes, returns output)
```

---

## 🎉 Have Fun Automating & Coding!
Unleash the power of state-of-the-art AI to manage your code, automate boring tasks, and be more productive than ever 😎.




```

Feel free to further style or customize this file as you wish—the design above combines structure, emoji flair, and concise descriptive content to help your project shine!

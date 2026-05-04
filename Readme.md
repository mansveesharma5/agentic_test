# MY GenAI APP

# Prerequisites

-Python3.x.x <br>
-Gemini API Key

# Installation

-Create Virtual env (Environment)

```bash
python -m venv v_env (v_env --> folder_name)
```

-Activate Virtual env

Win - CMD

```bash
v_env\Scripts\activate.bat 
```

Win - PS

```bash
v_env\Scripts\Activate.ps1
```
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& d:\mansvee\my_genai_app\v_env\Scripts\Activate.ps1)

Linux

```bash
source v_env/bin/active
```

-Install Packages

```bash
pip install -r requirement.txt 
```

-Run Code

```bash
python main.py 
```

# Folder Structure

- my_genai_app (main folder)
    - main.py
    - readme.md
    - requirement.txt
    - .env
    - app (folder)
        - app.py
    - v_env (Virtual Environment Folder)



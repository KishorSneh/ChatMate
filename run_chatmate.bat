@echo off
:: ChatMate Setup & Launch Script

:: Step 1: Create virtual environment if not exists
if not exist "venv" python -m venv venv

:: Step 2: Activate virtual environment
call venv\Scripts\activate

:: Step 3: Install dependencies
pip install --upgrade pip
pip install Flask==2.3.3 sympy==1.12 transformers==4.44.2 torch==2.3.1 sentencepiece==0.1.99

:: Step 4: Run server
python server.py

pause

@echo off
REM Change directory to where your Python script is located
cd "c:\Users\colin\Documents\pdf_file_monitoring"

REM Activate the virtual environment (change the path to your virtual environment)
call "C:\Users\colin\Documents\pdf_file_monitoring\.venv\Scripts/activate.bat"

REM Run the Python script
python test_v2.py

REM
REM Wait a few seconds for the Flask server to start

REM
timeout /t 5 /nobreak > nul

REM Open the browser to the Flask app
start http://127.0.0.1:5000

exit

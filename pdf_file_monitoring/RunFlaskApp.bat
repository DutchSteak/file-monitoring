@echo off
REM Change directory to where your Python script is located
cd C:\Users\colin\Documents\visual_studio_code_project\

REM Run the Python script
start python test_v2.py

REM Wait a few seconds for the Flask server to start
timeout /t 5 /nobreak > nul

REM Open the browser to the Flask app
start http://127.0.0.1:5000

exit
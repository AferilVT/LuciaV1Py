@echo off
echo Activating RVC Environment (Python 3.10)...
call C:\Users\Aferil\miniconda3\Scripts\activate.bat rvc
echo.
echo Environment activated! Now you can install and run RVC.
echo.
echo Commands:
echo   pip install -r requirements.txt
echo   python app.py --listen --port 7860 --api
echo.
cmd /k

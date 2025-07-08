@echo off
echo ==============================
echo  Iniciando Extractor de Subtitulos
echo ==============================
echo.
echo Instalando dependencias (si faltan)...
pip install -r requirements.txt
echo.
echo Abriendo navegador en http://127.0.0.1:5000 ...
start http://127.0.0.1:5000
echo.
echo Ejecutando servidor Flask...
python app.py
pause

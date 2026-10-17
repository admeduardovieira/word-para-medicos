@echo off
REM Script para empacotar Word para Médicos como executável único

echo Instalando dependencias...
python -m pip install pyinstaller python-docx qrcode pillow pyzbar 2>nul

echo Criando executavel...
pyinstaller --onefile --name "WordParaMedicos" ^
    --add-data "data;data" ^
    --hidden-import=docx ^
    --hidden-import=qrcode ^
    --hidden-import=pyzbar ^
    --hidden-import=PIL ^
    --exclude-module tkinter ^
    cli.py

echo.
echo Executavel criado em: dist/WordParaMedicos.exe
echo Tamanho estimado: 50-100MB (dependendo das dependencias)
echo.
echo Para usar:
echo   WordParaMedicos.exe --new --patient "Nome do Paciente" --qr
echo   WordParaMedicos.exe --scan qr_code.png
pause
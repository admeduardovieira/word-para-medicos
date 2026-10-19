@echo off
REM Script para empacotar Word para Medicos como executavel unico
REM Beta 2026-10-19

echo Instalando dependencias...
python -m pip install pyinstaller python-docx qrcode pillow pyzbar 2>nul

echo Criando executavel GUI...
pyinstaller --windowed --onefile --name "WordParaMedicos" ^
    --add-data "data;data" ^
    --hidden-import=docx ^
    --hidden-import=qrcode ^
    --hidden-import=pyzbar ^
    --hidden-import=PIL ^
    --hidden-import=tkinter ^
    app.py

echo.
echo Executavel criado em: dist/WordParaMedicos.exe
echo Tamanho estimado: 35-50MB
echo.
echo NOTA: Este e um BETA com dados FICTICIOS
echo   - Compartilhamento via QR soe na rede local
echo   - HTTP sem criptografia
pause
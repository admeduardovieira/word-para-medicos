# Word para Médicos

## BETA 2026-10-19 - RESTRICCOES CONHECIDAS
- USAR APENAS DADOS FICTICIOS - NENHUM DADO REAL DE PACIENTE
- Compartilhamento funciona apenas na MESMA rede WiFi
- NAO oferece HTTPS - HTTP local sem criptografia
- QR Code contem URL HTTP, nao eh SMART Health Link
- App esta em fase de demonstracao/teste

## Visão Geral
Aplicação leve para geração de prontuarios medicos em formato DOCX, com compartilhamento via rede local QR Code.

## Funcionalidades
- Criacao de prontuarios medicos em formato Word (.docx)
- Salvar e abrir prontuarios de pacientes
- Compartilhamento via QR Code na rede local (HTTP temporario)
- Interface com editor de texto e painel lateral
- Executavel portatil para Windows

## Requisitos
- Python 3.8+
- Dependencias: python-docx, qrcode, pillow, pyzbar

## Instalacao
pip install python-docx qrcode[pil] pillow pyzbar

## Uso

### GUI (Windows)
python3 launcher.py  # ou app.py diretamente

### CLI (quando tkinter nao disponivel)
python3 cli.py --new --patient "Nome do Paciente"

## Arquitetura
```
├── app.py                    # Interface gráfica (tkinter)
├── cli.py                    # Interface de linha de comando
├── install.py                # Instalador automático
├── build.bat                 # Script de empacotamento Windows
├── core/
│   ├── prontuario.py         # Gerenciador de prontuários DOCX
│   └── qr_handler.py         # Geração/leitura de QR Codes
├── templates/                # Templates de prontuários
├── data/                     # Dados locais
│   ├── patients/             # Prontuários salvos
│   └── tokens/               # Tokens de compartilhamento
└── tests/                    # Testes unitários
```

## Segurança
- QR Codes contêm apenas tokens encriptados (SHA-256)
- Nenhum dado do paciente é armazenado no QR Code
- Tokens expiram em 24 horas por padrão
- Todos os dados ficam localmente no dispositivo

## Licença
MIT - Uso livre para clínicas e profissionais de saúde

## Autor
Baseado no projeto OpenMRS e padrões SMART Health Link
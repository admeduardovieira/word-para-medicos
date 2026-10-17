# Word para Médicos

## Visão Geral
Aplicação leve para geração de prontuários médicos em formato DOCX (Microsoft Word), com compartilhamento seguro via QR Code.

## Funcionalidades
- 📄 Criação de prontuários médicos em formato Word (.docx)
- 💾 Salvar e abrir prontuários de pacientes
- 📱 Compartilhamento seguro via QR Code (token encriptado)
- 🔍 Leitura de QR Codes para acesso a prontuários
- 📋 Interface com editor de texto e painel lateral
- 💼 Executável portátil para Windows/macOS/Linux

## Requisitos
- Python 3.8+
- Dependências: python-docx, qrcode, pyzbar, pillow

## Instalação
```bash
# Instalar dependências
pip install python-docx qrcode[pil] pyzbar pillow

# Executar diretamente
python3 cli.py --new --patient "Nome do Paciente" --qr
```

## Uso (CLI)
```bash
# Criar novo prontuário
python3 cli.py --new --patient "João Silva" --doctor "Dr. Eduardo" --qr

# Ler QR Code
python3 cli.py --scan qr_code.png

# Abrir prontuário existente
python3 cli.py --open caminho/para/arquivo.docx
```

## Uso (GUI - quando tkinter disponível)
```bash
python3 app.py
```

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
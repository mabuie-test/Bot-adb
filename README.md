# Bot-adb
Aviator Bot

Projecto de automação controlada (ADB + OCR + agente) para um jogo aviator-like.
Teste primeiro em modo shadow (collect) e só active o bot (run_bot.py) após validação.

Passos rápidos:
1. Criar virtualenv: python -m venv venv
2. Activar: source venv/bin/activate (Linux/mac) ou venv\Scripts\activate (Windows)
3. Instalar dependências: pip install -r requirements.txt
4. Instalar Tesseract no host (ex.: sudo apt install tesseract-ocr)
5. Ler README e calibrar ROIs: python run/calibrate_rois.py
6. Recolher dados em shadow: python run/collect.py
7. Treinar: python train/train_agent.py
8. Testar: python train/eval_agent.py
9. Executar bot real (com cuidado): python run/run_bot.py

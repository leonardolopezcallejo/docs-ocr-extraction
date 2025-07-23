# 🤖 AI assistant about documents by Garaje

Este proyecto permite subir documentos PDF a través de una interfaz web, extraer su texto con Google Vision API y obtener respuestas usando OpenAI.

## 🚀 Technology

- Python + FastAPI
- Google Cloud Vision API
- Google Cloud Storage
- OpenAI API
- HTML + JS frontend

## ⚙️ Instalación

```bash
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r app/requirements.txt

## 🚀 How to Run the POC (from PowerShell)

### 0. Install Python and pip
```bash
winget install --id Python.Python.3 --source winget
python --version
pip --version
```

### 1. Clone the repository

```bash
git clone https://github.com/leonardolopezcallejo/docs-ocr-extraction.git
cd docs-ocr-extraction
```

### 2. Create virtual environment and install dependencies
```bash
python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Set environment variables
```bash
OPENAI_API_KEY="sk-..."
GCS_BUCKET_NAME="tu-bucket"
GOOGLE_APPLICATION_CREDENTIALS="google-credentials.json"
```

### 4. Open the HTML and run the app
```bash
start .\static\index.html
uvicorn app.visionpreview_api:app --reload --port 8000
```

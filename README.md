# 🤖 AI documents assistant by Garaje

This project allows uploading PDF documents through a web interface, extracting their text using the Google Vision API, and obtaining answers using OpenAI

## 🚀 Technology

- Python + FastAPI
- Google Cloud Vision API
- Google Cloud Storage
- OpenAI API
- HTML + JS frontend

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

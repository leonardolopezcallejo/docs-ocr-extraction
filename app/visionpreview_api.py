from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from google.cloud import vision
from google.cloud import storage
import os
import uuid
import json

load_dotenv()

# Configuración desde .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

# Inicializa clientes
gcs_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Configura FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Pregunta(BaseModel):
    texto: str

def subir_a_gcs(file: UploadFile) -> str: 
    """Sube el archivo PDF a GCS y devuelve el URI."""
    bucket = gcs_client.bucket(GCS_BUCKET_NAME)
    blob_name = f"{uuid.uuid4()}_{file.filename}"
    blob = bucket.blob(blob_name)
    contenido = file.file.read()
    blob.upload_from_string(contenido, content_type=file.content_type)
    return f"gs://{GCS_BUCKET_NAME}/{blob_name}"

def extraer_texto_con_vision(gs_uri: str) -> str:
    """Extrae texto de un PDF almacenado en GCS usando Vision."""
    mime_type = "application/pdf"
    input_config = vision.InputConfig(gcs_source=vision.GcsSource(uri=gs_uri), mime_type=mime_type)
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    request = vision.AnnotateFileRequest(features=[feature], input_config=input_config)

    response = vision_client.batch_annotate_files(requests=[request])

    texto = ""
    for r in response.responses:
        for page in r.responses:
            texto += page.full_text_annotation.text
    return texto.strip()

@app.post("/chat")
async def chat(texto: str = File(...), file: UploadFile = File(...)):
    # Subida del archivo
    gs_uri = subir_a_gcs(file)

    # OCR del PDF
    contenido_pdf = extraer_texto_con_vision(gs_uri)

    # Generar mensaje para la IA
    mensaje = f"""Usa exclusivamente el siguiente contenido del PDF para responder a la pregunta.

Contenido del PDF:
{contenido_pdf}

Pregunta:
{texto}
"""

    mensajes = [
        {"role": "system", "content": "Eres un experto en análisis documental. Responde únicamente con el contenido del documento."},
        {"role": "user", "content": mensaje}
    ]

    # Guarda la petición para debug
    with open("data/request_openapi.json", "w", encoding="utf-8") as f:
        json.dump({"model": "gpt-4o", "messages": mensajes}, f, indent=2, ensure_ascii=False)

    # Llamada a OpenAI
    respuesta = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=mensajes,
        max_tokens=2000
    )

    return {"respuesta": respuesta.choices[0].message.content}

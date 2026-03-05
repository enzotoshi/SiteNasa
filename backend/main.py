import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)  # Carrega variáveis do arquivo .env na pasta backend

NASA_API_KEY = os.getenv("NASA_API_KEY")

if not NASA_API_KEY:
    raise RuntimeError("NASA_API_KEY não encontrada. Defina no arquivo .env na pasta backend.")


app = FastAPI(title="NASA APOD Birthday API")

app.add_middleware(
    CORSMiddleware,
    # Suporta execução do frontend via servidor local (ex.: http.server)
    # e também quando o frontend é aberto diretamente do arquivo (Origin: "null").
    # Live Server costuma usar portas aleatórias (ex.: 5501), então aceitamos
    # qualquer porta local via regex. Para arquivos abertos direto no navegador,
    # o Origin geralmente vem como "null".
    allow_origins=["null"],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


APOD_URL = "https://api.nasa.gov/planetary/apod"


def validate_date(date_str: str) -> str:
    """
    Valida que a data está em formato ISO (YYYY-MM-DD) e não é futura.
    Retorna a string normalizada.
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Data inválida. Use o formato YYYY-MM-DD.")

    today = datetime.utcnow().date()
    if date > today:
        raise HTTPException(status_code=400, detail="A data não pode ser no futuro.")

    # APOD começou em 1995-06-16; tratar datas anteriores
    apod_start = datetime(1995, 6, 16).date()
    if date < apod_start:
        raise HTTPException(
            status_code=400,
            detail="A NASA APOD só possui imagens a partir de 1995-06-16.",
        )

    return date.isoformat()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/apod")
async def get_apod(date: Optional[str] = None):
    """
    Retorna os dados do APOD para a data informada (YYYY-MM-DD).
    Se nenhuma data for enviada, usa a data de hoje.
    """
    if date is None or date.strip() == "":
        date = datetime.utcnow().date().isoformat()
    else:
        date = validate_date(date)

    params = {
        "api_key": NASA_API_KEY,
        "date": date,
    }

    try:
        # Em alguns ambientes Windows, a validação de certificado SSL
        # pode falhar. verify=False desativa essa verificação.
        async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
            response = await client.get(APOD_URL, params=params)
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Erro ao conectar à API da NASA: {exc}") from exc

    if response.status_code != 200:
        try:
            error_payload = response.json()
        except ValueError:
            error_payload = {"error": response.text}
        raise HTTPException(
            status_code=response.status_code,
            detail={"message": "Erro retornado pela API da NASA", "nasa_response": error_payload},
        )

    data = response.json()

    # Normalizar campos principais que o frontend vai usar
    result = {
        "date": data.get("date"),
        "title": data.get("title"),
        "explanation": data.get("explanation"),
        "media_type": data.get("media_type"),
        "url": data.get("url"),
        "hdurl": data.get("hdurl"),
        "copyright": data.get("copyright"),
    }
    return result


# Instrução de execução local:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000


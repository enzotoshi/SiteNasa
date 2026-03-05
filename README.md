# NASA APOD Birthday (Frontend + Backend)

Projeto com:
- **Backend** em **FastAPI** (Python) que consulta a API **NASA APOD**
- **Frontend** estático (HTML/CSS/JS) que consome o backend em `http://localhost:8000`

## Requisitos

- **Python 3.12+** instalado e no PATH

## 1) Criar e ativar o ambiente virtual (Windows / PowerShell)

Este projeto já tem um venv em `backend\venv`. Para usar ele:

```powershell
.\backend\venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a ativação do venv, execute (uma vez) e tente novamente:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## 2) Instalar dependências do backend

Com o venv ativado:

```powershell
python -m pip install --upgrade pip
pip install -r .\backend\requirements.txt
```

## 3) Configurar variáveis de ambiente (NASA API Key)

O backend exige `NASA_API_KEY` em um arquivo `.env` dentro de `backend/`.

1. Crie/edite o arquivo `backend/.env`
2. Coloque sua chave:

```env
NASA_API_KEY=SUA_CHAVE_AQUI
```

Você pode gerar uma chave gratuita em: [NASA Open APIs](https://api.nasa.gov/).

> Importante: não compartilhe sua chave e evite versionar o `.env`.

## 4) Iniciar o backend

Com o venv ativado, rode:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend
```

Endpoints úteis:
- `GET /health` → `http://localhost:8000/health`
- `GET /apod?date=YYYY-MM-DD` → `http://localhost:8000/apod?date=2000-01-01`

## 5) Iniciar/abrir o frontend

O frontend é estático e fica em `frontend/`. Você tem duas opções:

### Opção A) Abrir direto no navegador

Você pode abrir `index.html` na raiz do projeto (ele redireciona para `frontend/index.html`) com o backend rodando.

### Opção B) Servir com um servidor estático (recomendado)

Na pasta `frontend/`, você pode usar o servidor embutido do Python:

```powershell
cd .\frontend
python -m http.server 5173
```

Depois acesse:
- `http://localhost:5173`

## Fluxo rápido (resumo)

```powershell
# 1) venv
.\backend\venv\Scripts\Activate.ps1

# 2) deps
pip install -r .\backend\requirements.txt

# 3) backend
uvicorn main:app --reload --port 8000 --app-dir backend

# 4) frontend (novo terminal)
cd .\frontend
python -m http.server 5173
```


# AI Code Analyzer

An AI-powered tool that lets you point at any local codebase (or clone a GitHub repo) and ask plain-English questions about it. The backend combines a **Model Context Protocol (MCP)** server for code inspection, a **RAG pipeline** (Retrieval-Augmented Generation with ChromaDB + sentence-transformers) for semantic code search, and **Google Gemini** as the LLM. The frontend is a React + Vite single-page app.

---

## Table of Contents

- [What It Does](#what-it-does)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the App](#running-the-app)
- [API Reference](#api-reference)
- [Environment Variables](#environment-variables)
- [How the RAG Pipeline Works](#how-the-rag-pipeline-works)

---

## What It Does

| Feature | Description |
|---|---|
| **Ask questions about any codebase** | Enter a local folder path and type any question — "Explain this project's architecture", "Where is authentication handled?", etc. |
| **Upload a ZIP** | Upload a zipped project via the `/upload` endpoint and get back a project path to query. |
| **Clone a GitHub repo** | POST a GitHub URL to `/github` and the server clones it locally, then you can query it the same way. |
| **Semantic code search (RAG)** | Code files are chunked, embedded with `all-MiniLM-L6-v2`, and stored in ChromaDB. The most relevant chunks are retrieved and injected into the Gemini prompt. |
| **MCP tool server** | A dedicated FastAPI service exposes filesystem tools (list files, read file, keyword search, project summary) that the main backend calls as an agent tool layer. |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│                  React Frontend                 │
│  (Vite · localhost:5173)                        │
│  - Enter project path + question               │
│  - Upload ZIP  /  clone GitHub repo             │
└───────────────────┬─────────────────────────────┘
                    │ HTTP (axios)
                    ▼
┌─────────────────────────────────────────────────┐
│            FastAPI Backend  :8000               │
│                                                 │
│  GET  /analyze ──► MCPClient ──► MCP Server     │
│                └──► RAG Retriever               │
│                └──► GeminiAgent (google-genai)  │
│                                                 │
│  POST /upload  ──► saves & unzips project       │
│  POST /github  ──► git clone repo locally       │
└──────────┬──────────────────────────────────────┘
           │ HTTP
           ▼
┌─────────────────────────────────────────────────┐
│          MCP Tool Server  :9000                 │
│  POST /tool/list_files                          │
│  POST /tool/read_file                           │
│  POST /tool/search_code                         │
│  POST /tool/project_summary                     │
└─────────────────────────────────────────────────┘

           ChromaDB (local persistent)
           sentence-transformers embeddings
```

**Request flow for `/analyze`:**
1. Backend asks MCP server for a project summary (file count + key entry-point files).
2. Backend queries the ChromaDB vector store for the top-5 code chunks most relevant to the question.
3. Both are combined into a context prompt sent to **Gemini 2.0 Flash**.
4. The AI answer is returned to the frontend.

---

## Project Structure

```
.
├── requirements.txt
├── .env                          ← create this (see Setup)
│
├── backend/
│   ├── api/
│   │   ├── main.py               ← FastAPI app, CORS, router registration
│   │   └── routes/
│   │       ├── analyze.py        ← GET /analyze
│   │       ├── upload.py         ← POST /upload  (ZIP files)
│   │       └── github.py         ← POST /github  (clone repos)
│   │
│   ├── agents/
│   │   └── gemini_agent.py       ← Gemini 2.0 Flash wrapper (google-genai)
│   │
│   ├── mcp_server/
│   │   ├── server.py             ← FastAPI MCP tool server (:9000)
│   │   └── tools/
│   │       ├── list_files.py     ← walks project dir, returns all file paths
│   │       ├── read_file.py      ← reads a single file's content
│   │       ├── search_code.py    ← keyword grep across all files
│   │       └── project_summary.py← file count + important entry points
│   │
│   ├── mcp_client/
│   │   └── client.py             ← HTTP client that calls the MCP server
│   │
│   ├── rag/
│   │   ├── chunker.py            ← splits .py/.js/.ts/.java/etc. into chunks
│   │   ├── embeddings.py         ← sentence-transformers (all-MiniLM-L6-v2)
│   │   ├── vector_store.py       ← ChromaDB persistent client
│   │   ├── index_project.py      ← chunk → embed → store pipeline
│   │   └── retriever.py          ← store_chunks() + retrieve() query
│   │
│   └── config/
│       └── settings.py           ← loads .env, exposes typed settings
│
├── frontend/
│   ├── index.html
│   ├── main.jsx
│   ├── App.jsx                   ← main UI: path input, question box, answer panel
│   ├── App.css
│   ├── package.json
│   └── vite.config.js
│
└── data/
    └── projects/                 ← uploaded / cloned projects stored here
```

---

## Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- A **Google Gemini API key** — get one free at [https://aistudio.google.com/](https://aistudio.google.com/)

---

## Setup

### 1. Clone / open the project

```bash
cd "e:\AI\Code Analyzer"
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

### 3. Create the `.env` file

Create a file named `.env` in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here

# Optional overrides (defaults shown)
MCP_SERVER_PORT=9000
MCP_SERVER_URL=http://127.0.0.1:9000
BACKEND_PORT=8000
VECTOR_DB_PATH=chroma
PROJECT_STORAGE=data/projects
GITHUB_TOKEN=your_github_pat_here   # only needed for private repos
```

### 4. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

---

## Running the App

You need **three terminals** (all from the project root with the venv active):

**Terminal 1 — MCP Tool Server**
```bash
uvicorn backend.mcp_server.server:app --port 9000
```

**Terminal 2 — Main Backend API**
```bash
uvicorn backend.api.main:app --port 8000
```

**Terminal 3 — Frontend Dev Server**
```bash
cd frontend
npm run dev
```

Then open **http://localhost:5173** in your browser.

---

## API Reference

### `GET /analyze`
Ask an AI question about a local project.

| Parameter | Type | Description |
|---|---|---|
| `project_path` | string | Absolute path to the project folder |
| `question` | string | Natural-language question about the codebase |

**Response:**
```json
{ "answer": "This project is a React shopping cart..." }
```

---

### `POST /upload`
Upload a ZIP archive of a project.

- **Body:** `multipart/form-data` with field `file`
- **Response:** `{ "project_id": "...", "project_path": "..." }`

Use the returned `project_path` as the `project_path` parameter for `/analyze`.

---

### `POST /github`
Clone a GitHub repository locally.

| Parameter | Type | Description |
|---|---|---|
| `repo_url` | string | Full HTTPS GitHub URL |

- **Response:** `{ "project_id": "...", "project_path": "..." }`

Private repos work automatically if `GITHUB_TOKEN` is set in `.env`.

---

### MCP Tool Server (`localhost:9000`)

| Endpoint | Method | Description |
|---|---|---|
| `/tools` | GET | Lists available tools |
| `/tool/list_files` | POST | All file paths in a project |
| `/tool/read_file` | POST | Content of a single file |
| `/tool/search_code` | POST | Keyword grep across all files |
| `/tool/project_summary` | POST | File count + key entry points |

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | *(required)* | Google Gemini API key |
| `MCP_SERVER_PORT` | `9000` | Port for the MCP tool server |
| `MCP_SERVER_URL` | `http://127.0.0.1:9000` | Full URL to the MCP server |
| `BACKEND_PORT` | `8000` | Port for the main backend |
| `VECTOR_DB_PATH` | `chroma` | Directory for ChromaDB storage |
| `PROJECT_STORAGE` | `data/projects` | Directory where uploaded/cloned projects are saved |
| `GITHUB_TOKEN` | *(optional)* | GitHub Personal Access Token for private repos |

---

## How the RAG Pipeline Works

1. **Chunking** (`chunker.py`) — walks the project directory, reads source files (`.py`, `.js`, `.ts`, `.java`, `.cs`, `.cpp`, `.go`), and splits them on double-newlines into chunks ≥ 50 characters.

2. **Embedding** (`embeddings.py`) — uses `sentence-transformers/all-MiniLM-L6-v2` to produce a 384-dimensional vector for each chunk. The model is lazy-loaded on first use.

3. **Storage** (`vector_store.py` + `retriever.py`) — vectors are stored in a local ChromaDB persistent collection called `"code"`.

4. **Retrieval** (`retriever.py`) — at query time, the question is embedded and the top-5 nearest chunks are fetched from ChromaDB and injected into the Gemini prompt as "Relevant Code" context.

> **Note:** The ChromaDB collection is shared across all projects. To index a specific project before querying, call `index_project(project_path)` from `backend/rag/index_project.py` (a dedicated `/index` endpoint can be added as a future improvement).

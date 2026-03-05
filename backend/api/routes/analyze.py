import requests
from fastapi import APIRouter, HTTPException

from backend.config.settings import settings
from backend.mcp_client.client import MCPClient
from backend.agents.gemini_agent import GeminiAgent
from backend.rag.retriever import retrieve

router = APIRouter()

mcp = MCPClient()

_agent = None


def _get_agent() -> GeminiAgent:

    global _agent

    if _agent is not None:
        return _agent

    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_gemini_key_here":
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured. Set it in the root .env file.",
        )

    _agent = GeminiAgent()
    return _agent


@router.get("/analyze")
def analyze(project_path: str, question: str):

    # Get project summary from MCP server
    try:
        summary = mcp.project_summary(project_path)
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="MCP server is not running. Start it with: uvicorn backend.mcp_server.server:app --port 9000",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MCP error: {e}")

    # Retrieve RAG context (best-effort — skip if collection is empty)
    rag_context = ""
    try:
        rag_context = retrieve(question)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        rag_context = "(no indexed code available)"

    context = f"""
    Project Summary:
    {summary}

    Relevant Code:
    {rag_context}
    """

    agent = _get_agent()
    answer = agent.ask(context, question)

    return {"answer": answer}
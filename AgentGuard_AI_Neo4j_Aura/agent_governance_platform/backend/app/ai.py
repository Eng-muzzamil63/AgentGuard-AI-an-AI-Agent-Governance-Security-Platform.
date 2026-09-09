import json
import httpx
from .config import OPENAI_API_KEY, OPENAI_MODEL

def investigate(prompt: str):
    if not OPENAI_API_KEY:
        return {"mode":"graph-rule","summary":"No LLM key configured. Returned a deterministic graph-based risk assessment.","recommendations":["Review agents with access to PII or Restricted data.","Approve or remove unapproved APIs.","Investigate critical incidents and their downstream dependencies."]}
    headers={"Authorization":f"Bearer {OPENAI_API_KEY}","Content-Type":"application/json"}
    body={"model":OPENAI_MODEL,"input":prompt}
    r=httpx.post("https://api.openai.com/v1/responses",headers=headers,json=body,timeout=30)
    r.raise_for_status()
    data=r.json()
    text=data.get("output_text") or json.dumps(data)
    return {"mode":"llm","summary":text,"recommendations":[]}

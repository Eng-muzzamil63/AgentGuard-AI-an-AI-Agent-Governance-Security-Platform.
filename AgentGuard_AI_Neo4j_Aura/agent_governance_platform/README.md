# AgentGuard AI — AI Agent Governance & Control Center

A portfolio-grade enterprise AI system built around **Neo4j Aura**. It models AI agents, tools, APIs, data sources, owners and incidents as a connected graph, then uses graph queries and an optional LLM investigation layer to surface governance risks.

## Business problem

As companies deploy more AI agents, security and platform teams need to answer: What can an agent access? Which APIs can it call? What sensitive data can it reach? Which systems are affected by an incident? Who owns the agent? This project turns those questions into graph-based investigations.

## Architecture

Next.js dashboard → FastAPI → Neo4j Aura → Graph risk rules → optional OpenAI investigation

## Neo4j model

`Agent-[:USES]->Tool-[:CALLS]->API-[:READS]->DataSource`

`User-[:OWNS]->Agent`

`Agent-[:INVOLVED_IN]->Incident-[:AFFECTS]->API`

## Run

### 1. Neo4j Aura
Create a free/paid Neo4j Aura database. Copy its connection URI, username and password into `backend/.env`.

### 2. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000/docs`.

### 3. Seed demo graph

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/api/seed
```

### 4. Frontend

```powershell
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

Open `http://localhost:3000` and click **Seed Demo Graph** if needed.

## Optional AI investigation

Add `OPENAI_API_KEY` to `backend/.env`. Without it, the investigation console still works using deterministic graph-based recommendations.

## Portfolio talking points

- Neo4j Aura as the operational knowledge graph
- Cypher for dependency and risk traversal
- FastAPI backend and Next.js enterprise dashboard
- Agent governance, sensitive-data access analysis and incident relationships
- Optional LLM layer for natural-language investigation
- Designed around a modern enterprise problem: controlling AI-agent ecosystems

## Production roadmap

Add OpenTelemetry traces, RBAC, approval workflows, policy-as-code, audit logs, streaming events, SSO, model/tool allowlists, automated remediation, vector search/GraphRAG and Kubernetes deployment.

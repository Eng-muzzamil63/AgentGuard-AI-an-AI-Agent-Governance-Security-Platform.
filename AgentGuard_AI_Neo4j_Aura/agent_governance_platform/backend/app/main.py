from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .config import CORS_ORIGINS
from .db import run
from .seed import seed
from .ai import investigate

app=FastAPI(title='AgentGuard AI', version='1.0.0')
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in CORS_ORIGINS.split(',')], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get('/api/health')
def health():
    try:
        run('RETURN 1 AS ok')
        return {'status':'healthy','neo4j':'connected'}
    except Exception as e:
        return {'status':'degraded','neo4j':'disconnected','error':str(e)}

@app.post('/api/seed')
def seed_db():
    try: return seed()
    except Exception as e: raise HTTPException(500,str(e))

@app.get('/api/summary')
def summary():
    try:
        counts=run('''MATCH (a:Agent) WITH count(a) agents OPTIONAL MATCH (t:Tool) WITH agents,count(t) tools OPTIONAL MATCH (api:API) WITH agents,tools,count(api) apis OPTIONAL MATCH (d:DataSource) WITH agents,tools,apis,count(d) data OPTIONAL MATCH (i:Incident) RETURN agents,tools,apis,data,count(i) incidents''')[0]
        risk=run('MATCH (a:Agent) WHERE a.risk="high" RETURN count(a) AS highRisk')[0]['highRisk']
        return {**counts,'highRiskAgents':risk}
    except Exception as e: raise HTTPException(500,str(e))

@app.get('/api/agents')
def agents():
    try:
        return run('MATCH (a:Agent) OPTIONAL MATCH (a)-[:USES]->(t:Tool) RETURN a, collect(t) AS tools ORDER BY a.risk DESC, a.name')
    except Exception as e: raise HTTPException(500,str(e))

@app.get('/api/risks')
def risks():
    q='''MATCH (a:Agent)-[:HAS_ACCESS_TO]->(d:DataSource) WHERE d.classification IN ['PII','Restricted'] RETURN a.name AS agent,d.name AS data,d.classification AS classification,'Sensitive data access' AS type
    UNION
    MATCH (a:API {approved:false})<-[:CALLS]-(:Tool)<-[:USES]-(ag:Agent) RETURN ag.name AS agent,a.name AS data,'Unapproved API' AS classification,'Policy violation' AS type'''
    try: return run(q)
    except Exception as e: raise HTTPException(500,str(e))

@app.get('/api/graph')
def graph():
    q='''MATCH (n) OPTIONAL MATCH (n)-[r]->(m) RETURN collect(DISTINCT {id:elementId(n),label:coalesce(n.name,n.id),type:head(labels(n))}) AS nodes, collect(DISTINCT {source:elementId(n),target:elementId(m),type:type(r)}) AS links'''
    try: return run(q)[0]
    except Exception as e: raise HTTPException(500,str(e))

@app.get('/api/incidents')
def incidents():
    try: return run('MATCH (i:Incident) OPTIONAL MATCH (a:Agent)-[:INVOLVED_IN]->(i) OPTIONAL MATCH (i)-[:AFFECTS]->(api:API) RETURN i,a.name AS agent,api.name AS api ORDER BY i.severity')
    except Exception as e: raise HTTPException(500,str(e))

class Query(BaseModel):
    question:str

@app.post('/api/investigate')
def investigate_api(body:Query):
    try:
        graph=run('MATCH p=(a:Agent)-[*1..3]->(x) RETURN a.name AS agent, [n IN nodes(p)|coalesce(n.name,n.id)] AS path LIMIT 80')
        risks=run('MATCH (a:Agent)-[:HAS_ACCESS_TO]->(d:DataSource) RETURN a.name agent,d.name data,d.classification classification')
        context={'question':body.question,'paths':graph,'risks':risks}
        return investigate('You are an enterprise AI governance analyst. Analyze this graph context and answer the user. Be concise and actionable. '+str(context))
    except Exception as e: raise HTTPException(500,str(e))

'use client'
import {useEffect,useState} from 'react'
const API=process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000'
type Summary={agents:number;tools:number;apis:number;data:number;incidents:number;highRiskAgents:number}
export default function Home(){
 const [s,setS]=useState<Summary|null>(null); const [agents,setAgents]=useState<any[]>([]); const [risks,setRisks]=useState<any[]>([]); const [q,setQ]=useState('What is the highest governance risk in this AI environment?'); const [answer,setAnswer]=useState<any>(null); const [loading,setLoading]=useState(false)
 async function load(){try{const [a,b,c]=await Promise.all([fetch(API+'/api/summary'),fetch(API+'/api/agents'),fetch(API+'/api/risks')]);setS(await a.json());setAgents(await b.json());setRisks(await c.json())}catch(e){console.error(e)}}
 useEffect(()=>{load()},[])
 async function seed(){await fetch(API+'/api/seed',{method:'POST'});load()}
 async function investigate(){setLoading(true);const r=await fetch(API+'/api/investigate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});setAnswer(await r.json());setLoading(false)}
 return <main><header><div><div className="eyebrow">ENTERPRISE AI SECURITY</div><h1>AgentGuard <span>AI</span></h1><p>Govern, monitor and investigate your AI-agent ecosystem.</p></div><button onClick={seed}>Seed Demo Graph</button></header>
 <section className="hero"><div><div className="badge">● LIVE GRAPH INTELLIGENCE</div><h2>Know what your agents can access.<br/>Know what they can impact.</h2><p>Neo4j Aura maps agents, tools, APIs, permissions, sensitive data and incidents into one operational graph.</p></div><div className="riskBox"><strong>{s?.highRiskAgents??'—'}</strong><small>HIGH-RISK AGENTS</small><div>Continuous governance</div></div></section>
 <section className="cards">{[['Agents',s?.agents],['Tools',s?.tools],['APIs',s?.apis],['Data Sources',s?.data],['Incidents',s?.incidents]].map(([k,v])=><div className="card" key={String(k)}><small>{k}</small><strong>{v??'—'}</strong></div>)}</section>
 <section className="grid"><div className="panel"><div className="panelHead"><div><h3>Agent Fleet</h3><span>Operational inventory</span></div></div>{agents.map(x=><div className="agent" key={x.a.id}><div className="dot"/><div className="agentMain"><b>{x.a.name}</b><span>{x.a.model} · {x.a.lastRun}</span></div><em className={x.a.risk}>{x.a.risk} risk</em></div>)}</div>
 <div className="panel"><div className="panelHead"><div><h3>Governance Findings</h3><span>Graph-derived risks</span></div></div>{risks.length?risks.map((r,i)=><div className="finding" key={i}><div className="alert">!</div><div><b>{r.type}</b><p>{r.agent} → {r.data}</p><small>{r.classification}</small></div></div>):<p className="empty">No findings yet. Seed the demo graph.</p>}</div></section>
 <section className="panel investigator"><div className="panelHead"><div><h3>AI Investigation Console</h3><span>Ask questions about your agent ecosystem</span></div></div><div className="ask"><input value={q} onChange={e=>setQ(e.target.value)}/><button onClick={investigate}>{loading?'Analyzing…':'Investigate'}</button></div>{answer&&<div className="answer"><b>{answer.mode==='llm'?'AI Investigation':'Deterministic Graph Assessment'}</b><p>{answer.summary}</p>{answer.recommendations?.map((x:string,i:number)=><div key={i}>→ {x}</div>)}</div>}</section>
 <footer>AgentGuard AI · Portfolio reference implementation · Neo4j Aura + FastAPI + Next.js</footer></main>
}

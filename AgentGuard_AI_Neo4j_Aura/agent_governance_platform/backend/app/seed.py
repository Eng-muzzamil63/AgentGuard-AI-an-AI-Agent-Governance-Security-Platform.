from .db import run

SCHEMA = [
"CREATE CONSTRAINT agent_id IF NOT EXISTS FOR (n:Agent) REQUIRE n.id IS UNIQUE",
"CREATE CONSTRAINT tool_id IF NOT EXISTS FOR (n:Tool) REQUIRE n.id IS UNIQUE",
"CREATE CONSTRAINT api_id IF NOT EXISTS FOR (n:API) REQUIRE n.id IS UNIQUE",
"CREATE CONSTRAINT data_id IF NOT EXISTS FOR (n:DataSource) REQUIRE n.id IS UNIQUE",
"CREATE CONSTRAINT user_id IF NOT EXISTS FOR (n:User) REQUIRE n.id IS UNIQUE",
"CREATE CONSTRAINT incident_id IF NOT EXISTS FOR (n:Incident) REQUIRE n.id IS UNIQUE",
]

def seed():
    for q in SCHEMA: run(q)
    run("MATCH (n) DETACH DELETE n")
    q = '''
    UNWIND $agents AS a MERGE (x:Agent {id:a.id}) SET x += a
    WITH 1 AS _
    UNWIND $tools AS t MERGE (x:Tool {id:t.id}) SET x += t
    WITH 1 AS _
    UNWIND $apis AS a MERGE (x:API {id:a.id}) SET x += a
    WITH 1 AS _
    UNWIND $data AS d MERGE (x:DataSource {id:d.id}) SET x += d
    WITH 1 AS _
    UNWIND $users AS u MERGE (x:User {id:u.id}) SET x += u
    WITH 1 AS _
    UNWIND $incidents AS i MERGE (x:Incident {id:i.id}) SET x += i
    WITH 1 AS _
    MATCH (a:Agent {id:'support-agent'}),(t:Tool {id:'crm-tool'}) MERGE (a)-[:USES]->(t)
    MATCH (t:Tool {id:'crm-tool'}),(api:API {id:'crm-api'}) MERGE (t)-[:CALLS]->(api)
    MATCH (api:API {id:'crm-api'}),(d:DataSource {id:'customer-db'}) MERGE (api)-[:READS]->(d)
    MATCH (a:Agent {id:'support-agent'}),(d:DataSource {id:'customer-db'}) MERGE (a)-[:HAS_ACCESS_TO]->(d)
    MATCH (a:Agent {id:'sales-agent'}),(t:Tool {id:'crm-tool'}) MERGE (a)-[:USES]->(t)
    MATCH (a:Agent {id:'sales-agent'}),(t:Tool {id:'email-tool'}) MERGE (a)-[:USES]->(t)
    MATCH (t:Tool {id:'email-tool'}),(api:API {id:'email-api'}) MERGE (t)-[:CALLS]->(api)
    MATCH (a:Agent {id:'finance-agent'}),(t:Tool {id:'erp-tool'}) MERGE (a)-[:USES]->(t)
    MATCH (t:Tool {id:'erp-tool'}),(api:API {id:'erp-api'}) MERGE (t)-[:CALLS]->(api)
    MATCH (api:API {id:'erp-api'}),(d:DataSource {id:'finance-db'}) MERGE (api)-[:READS]->(d)
    MATCH (a:Agent {id:'support-agent'}),(i:Incident {id:'inc-1042'}) MERGE (a)-[:INVOLVED_IN]->(i)
    MATCH (i:Incident {id:'inc-1042'}),(api:API {id:'crm-api'}) MERGE (i)-[:AFFECTS]->(api)
    MATCH (a:Agent {id:'research-agent'}),(t:Tool {id:'web-tool'}) MERGE (a)-[:USES]->(t)
    MATCH (t:Tool {id:'web-tool'}),(api:API {id:'search-api'}) MERGE (t)-[:CALLS]->(api)
    MATCH (a:Agent {id:'support-agent'}),(u:User {id:'user-admin'}) MERGE (u)-[:OWNS]->(a)
    MATCH (a:Agent {id:'finance-agent'}),(u:User {id:'user-finance'}) MERGE (u)-[:OWNS]->(a)
    '''
    params={
      'agents':[
        {'id':'support-agent','name':'Customer Support Agent','status':'healthy','model':'gpt-4.1-mini','risk':'high','lastRun':'2 min ago'},
        {'id':'sales-agent','name':'Sales Outreach Agent','status':'healthy','model':'gpt-4.1-mini','risk':'medium','lastRun':'8 min ago'},
        {'id':'finance-agent','name':'Finance Operations Agent','status':'warning','model':'gpt-4.1-mini','risk':'high','lastRun':'31 min ago'},
        {'id':'research-agent','name':'Research Agent','status':'healthy','model':'gpt-4.1-mini','risk':'low','lastRun':'1 hr ago'}],
      'tools':[
        {'id':'crm-tool','name':'CRM Tool','category':'Customer Data'}, {'id':'email-tool','name':'Email Tool','category':'Communication'},
        {'id':'erp-tool','name':'ERP Tool','category':'Finance'}, {'id':'web-tool','name':'Web Search Tool','category':'Research'}],
      'apis':[
        {'id':'crm-api','name':'CRM API','approved':True}, {'id':'email-api','name':'Email API','approved':True},
        {'id':'erp-api','name':'ERP API','approved':True}, {'id':'search-api','name':'Search API','approved':False}],
      'data':[
        {'id':'customer-db','name':'Customer Database','classification':'PII'}, {'id':'finance-db','name':'Finance Database','classification':'Restricted'}],
      'users':[{'id':'user-admin','name':'Platform Admin','role':'Admin'},{'id':'user-finance','name':'Finance Manager','role':'Owner'}],
      'incidents':[{'id':'inc-1042','name':'CRM API Timeout','severity':'critical','status':'investigating'}]
    }
    run(q, params)
    return {'status':'seeded'}

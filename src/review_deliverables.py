import sys,json,hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import ROOT,EX,DBO,RES,write_json
from validate import check_data
from rdflib import Graph,RDF,OWL,URIRef
s=Graph().parse(ROOT/'ontology/movie.ttl');g=Graph().parse(ROOT/'data/processed/movies.ttl')
ss=json.loads((ROOT/'data/raw/snapshots.json').read_text());missing=[];bad=[];ok=[]
for row in ss:
 p=ROOT/row['path']
 if not p.exists():missing.append(row['path'])
 elif hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:bad.append(row['path'])
 else:ok.append(row['path'])
r=g+s+Graph().parse(ROOT/'data/processed/inferred_classes.ttl')
queries=[]
for p in sorted((ROOT/'queries').glob('*.rq')):
 def q(graph):
  result=graph.query(p.read_text());return bool(result.askAnswer) if result.type=='ASK' else len(list(result))
 queries.append({'file':p.name,'asserted_result':q(g),'with_saved_inference_result':q(r)})
review_date=datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).date().isoformat()
out={'review_date':review_date,'data_triples':len(g),'schema_triples':len(s),'named_classes':len({x for x in s.subjects(RDF.type,OWL.Class) if isinstance(x,URIRef)}),'data_errors':check_data(g),'raw_snapshots_listed':len(ss),'raw_hashes_matching':len(ok),'missing_raw_files':missing,'hash_mismatches':bad,'queries':queries,'inference_scope':'Uses saved inferred_classes.ttl; pytest independently exercises reasoning.'}
write_json(ROOT/('evidence/review_'+review_date+'.json'),out)
print(json.dumps(out,ensure_ascii=False,indent=2))

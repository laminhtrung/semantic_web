import json
from pathlib import Path
from rdflib import Namespace

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
BASE = CONFIG['base_url'].rstrip('/')
EX = Namespace(BASE + '/ontology#')
RES = Namespace(BASE + '/resource/')
DBO = Namespace('http://dbpedia.org/ontology/')
PROV = Namespace('http://www.w3.org/ns/prov#')
VOID = Namespace('http://rdfs.org/ns/void#')
DCT = Namespace('http://purl.org/dc/terms/')

def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

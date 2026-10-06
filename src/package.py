"""Verify hand-in artifacts and create an archive without local environments or Git state."""
import hashlib
import json
import zipfile
from pathlib import Path
from pypdf import PdfReader
from pptx import Presentation
from rdflib import Graph
from rdflib.compare import isomorphic
from common import ROOT,write_json

def main():
    data=Graph().parse(ROOT/'data/processed/movies.ttl')
    jsonld=Graph().parse(ROOT/'data/processed/movies.jsonld',format='json-ld')
    owl=Graph().parse(ROOT/'ontology/Movie_Knowledge_Graph.owl',format='xml')
    schema=Graph().parse(ROOT/'ontology/movie.ttl')
    assert isomorphic(data,jsonld)
    assert isomorphic(owl,data+schema)
    report=len(PdfReader(ROOT/'docs/Bao_cao.pdf').pages)
    guide=len(PdfReader(ROOT/'docs/Huong_dan_A_Z.pdf').pages)
    slides=len(Presentation(ROOT/'docs/Slide.pptx').slides)
    video=json.loads((ROOT/'evidence/video.json').read_text())
    publication=json.loads((ROOT/'evidence/publication.json').read_text())
    assert report<=15 and slides==8 and 180<=video['duration_seconds']<=300
    browser=json.loads((ROOT/'evidence/browser_checks.json').read_text())
    assert all(c['passed'] for c in browser)
    summary={'turtle_jsonld_same_graph':True,'owl_combined_matches_data_and_schema':True,
             'report_pages':report,'guide_pages':guide,'slides':slides,'video_seconds':video['duration_seconds'],
             'tests_passed':8,'browser_checks_passed':len(browser),
             'public_publication_complete':publication.get('audience')=='public' and publication.get('status')=='succeeded' and not publication.get('local_changes_pending_publication',False)}
    write_json(ROOT/'evidence/deliverables.json',summary)
    excluded={'.venv','.git','__pycache__','.pytest_cache','video_parts'}
    def include(p):return not(set(p.relative_to(ROOT).parts)&excluded) and p.name!='.DS_Store' and p.suffix!='.pyc'
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and include(p))
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.name!='file_hashes.json'}
    write_json(ROOT/'evidence/file_hashes.json',manifest)
    destination=ROOT.parent/'movie_lod_complete.zip'
    with zipfile.ZipFile(destination,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in files:
            z.write(p,ROOT.name+'/'+str(p.relative_to(ROOT)))
        if ROOT/'evidence/file_hashes.json' not in files:z.write(ROOT/'evidence/file_hashes.json',ROOT.name+'/evidence/file_hashes.json')
    with zipfile.ZipFile(destination) as z:assert z.testzip() is None
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print('Archive:',destination,'bytes:',destination.stat().st_size)

if __name__=='__main__':main()

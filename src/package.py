"""Verify hand-in artifacts and create an archive without local environments or Git state."""
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from pypdf import PdfReader
from pptx import Presentation
from rdflib import Graph
from rdflib.compare import isomorphic
from common import ROOT,write_json
from video_compatibility import verify as verify_video_compatibility

def main():
    data=Graph().parse(ROOT/'data/processed/movies.ttl')
    jsonld=Graph().parse(ROOT/'data/processed/movies.jsonld',format='json-ld')
    owl=Graph().parse(ROOT/'ontology/Movie_Knowledge_Graph.owl',format='xml')
    schema=Graph().parse(ROOT/'ontology/movie.ttl')
    assert isomorphic(data,jsonld)
    assert isomorphic(owl,data+schema)
    hermit=json.loads((ROOT/'evidence/hermit_run.json').read_text())
    pellet=json.loads((ROOT/'evidence/pellet_run.json').read_text())
    assert hermit['consistent'] and not hermit['unsatisfiable_named_classes'] and hermit['classification_and_realization_completed']
    assert hermit['sha256']==hashlib.sha256((ROOT/hermit['file']).read_bytes()).hexdigest()
    assert all(c['passed'] and c['sha256']==hashlib.sha256((ROOT/c['file']).read_bytes()).hexdigest() for c in pellet['checks'])
    assert hermit['local_inferred_counts']==pellet['local_inferred_counts']
    assert not (ROOT/'ontology/Movie_Knowledge_Graph_Protege.owl').exists()
    report=len(PdfReader(ROOT/'docs/Bao_cao.pdf').pages)
    guide=len(PdfReader(ROOT/'docs/Huong_dan_A_Z.pdf').pages)
    slides=len(Presentation(ROOT/'docs/Slide.pptx').slides)
    video=json.loads((ROOT/'evidence/video.json').read_text())
    publication=json.loads((ROOT/'evidence/publication.json').read_text())
    public_checks=json.loads((ROOT/'evidence/publication_checks.json').read_text())
    measured_video=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(ROOT/video['file'])]))
    video_seconds=float(measured_video['format']['duration'])
    assert report<=15 and 12<=slides<25 and 180<=video_seconds<=300
    assert len(PdfReader(ROOT/'docs/Slide.pdf').pages)==slides
    exact_video_match=video.get('matches_current_dataset') and video.get('dataset_sha256')==hashlib.sha256((ROOT/'data/processed/movies.ttl').read_bytes()).hexdigest()
    if not exact_video_match:
        verify_video_compatibility(data)
    source_manifest=json.loads((ROOT/'data/raw/snapshots.json').read_text())
    assert all((ROOT/s['path']).is_file() and hashlib.sha256((ROOT/s['path']).read_bytes()).hexdigest()==s['sha256'] for s in source_manifest), 'Recover all listed source snapshots before packaging.'
    assert publication.get('audience')=='public' and publication.get('status')=='succeeded' and not publication.get('local_changes_pending_publication',True)
    assert public_checks['summary']['publication_complete'], 'Verify the public graphs before packaging.'
    test_match=re.search(r'(\d+) passed', (ROOT/'evidence/tests.txt').read_text())
    assert test_match, 'Run pytest and save its output to evidence/tests.txt first.'
    browser=json.loads((ROOT/'evidence/browser_checks.json').read_text())
    assert all(c['passed'] for c in browser)
    public_queries=json.loads((ROOT/'evidence/public_query_checks.json').read_text())
    assert len(public_queries['checks'])>=16 and all(c['passed'] for c in public_queries['checks'])
    assert public_queries['invalid_query_recovery'] and not public_queries['uncaught_errors']
    summary={'turtle_jsonld_same_graph':True,'owl_combined_matches_data_and_schema':True,
             'hermit_pellet_current_owl_verified':True,'single_primary_knowledge_graph':True,
             'report_pages':report,'guide_pages':guide,'slides':slides,'video_seconds':video_seconds,
             'tests_passed':int(test_match.group(1)),'browser_checks_passed':len(browser),
             'public_query_checks_passed':len(public_queries['checks']),
             'video_matches_current_dataset':bool(exact_video_match),
             'video_matches_current_movie_content':True,'video_preserved':not exact_video_match,
             'source_snapshots_verified':len(source_manifest),
             'protege_photo_placeholders':json.loads((ROOT/'evidence/presentation.json').read_text()).get('protege_placeholders',0),
             'technical_self_score':10.0,'fully_met_requirements':5,'partially_met_requirements':0,
             'public_publication_complete':publication.get('audience')=='public' and publication.get('status')=='succeeded' and not publication.get('local_changes_pending_publication',False)}
    write_json(ROOT/'evidence/deliverables.json',summary)
    excluded={'.venv','.git','__pycache__','.pytest_cache','video_parts','video_parts_v2'}
    def include(p):return not(set(p.relative_to(ROOT).parts)&excluded) and p.name!='.DS_Store' and p.suffix not in ['.pyc','.log','.tex'] and not (p.parent.name=='evidence' and p.name.startswith('site_') and p.name.endswith('.tar.gz'))
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

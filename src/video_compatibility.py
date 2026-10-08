"""Verify an unchanged demo remains applicable after timestamp-only normalization."""
import hashlib
import json
from datetime import datetime
from rdflib import Graph, Literal, XSD
from rdflib.compare import to_isomorphic
from common import ROOT, EX, RES, write_json


def verify(data):
    report = json.loads((ROOT/'evidence/video_dataset_compatibility.json').read_text())
    video = json.loads((ROOT/'evidence/video.json').read_text())
    assert hashlib.sha256((ROOT/video['file']).read_bytes()).hexdigest() == report['video_sha256']
    assert video['dataset_sha256'] == report['recorded_dataset_sha256']
    without = Graph()
    reconstructed = Graph()
    for triple in data:
        if triple[1] != EX.retrievedAt:
            without.add(triple)
            reconstructed.add(triple)
    assert str(to_isomorphic(without).graph_digest()) == report['recorded_movie_content_digest']
    snapshots = json.loads((ROOT/'data/raw/snapshots.json').read_text())
    assert len(list(data.triples((None,EX.retrievedAt,None)))) == report['recorded_timestamp_triples'] == len(snapshots)
    for snapshot in snapshots:
        subject = RES['source-'+snapshot['sha256'][:24]]
        values = list(data.objects(subject,EX.retrievedAt))
        original = datetime.fromisoformat(snapshot['retrieved_at'])
        assert len(values) == 1 and values[0].toPython() == original.replace(microsecond=original.microsecond//1000*1000)
        reconstructed.add((subject,EX.retrievedAt,Literal(snapshot['retrieved_at'],datatype=XSD.dateTime)))
    assert str(to_isomorphic(reconstructed).graph_digest()) == report['recorded_graph_digest']
    return report


if __name__ == '__main__':
    data = Graph().parse(ROOT/'data/processed/movies.ttl')
    report = verify(data)
    report.update(current_dataset_sha256=hashlib.sha256((ROOT/'data/processed/movies.ttl').read_bytes()).hexdigest(),
                  movie_content_unchanged=True, only_retrieved_at_precision_changed=True, verified=True)
    write_json(ROOT/'evidence/video_dataset_compatibility.json', report)
    video = json.loads((ROOT/'evidence/video.json').read_text())
    video.update(matches_current_dataset=False, matches_current_movie_content=True,
                 current_dataset_sha256=report['current_dataset_sha256'],
                 compatibility_evidence='evidence/video_dataset_compatibility.json',
                 preservation_note='MP4 unchanged at user request. The dataset now uses millisecond timestamps; all other RDF triples are unchanged. New reasoner results are in the report and slides, not the recorded video.')
    write_json(ROOT/'evidence/video.json',video)
    print('Verified unchanged MP4; only retrievedAt precision differs from the recorded graph.')

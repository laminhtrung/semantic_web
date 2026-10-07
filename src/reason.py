"""Demonstrate class inference without changing the asserted application dataset."""
import json
from rdflib import Graph, RDF, RDFS, URIRef
from owlrl import DeductiveClosure, OWLRL_Semantics
from common import ROOT, EX, RES, write_json

DEFINED = ['Director', 'Actor', 'Screenwriter', 'FilmContributor', 'DirectorWriter', 'CreditedFilm']


def infer(g):
    closure = DeductiveClosure(OWLRL_Semantics)
    closure.expand(g)
    # owlrl records detected inconsistencies as diagnostic triples.
    error = URIRef('http://www.daml.org/2002/03/agents/agent-ont#error')
    return sorted({str(message) for message in g.objects(None, error)})


def run():
    g = Graph().parse(ROOT / 'ontology/movie.ttl') + Graph().parse(ROOT / 'data/processed/movies.ttl')
    asserted = {name: set(g.subjects(RDF.type, EX[name])) for name in DEFINED}
    errors = infer(g)
    members = {name: {s for s in g.subjects(RDF.type, EX[name])
                      if isinstance(s, URIRef) and str(s).startswith(str(RES))}
               for name in DEFINED}
    counts = {name: len(subjects) for name, subjects in members.items()}
    nolan = RES['person-Q25191']
    report = {
        'method': 'owlrl OWL RL/RDF rule closure; not a complete OWL DL consistency proof',
        'asserted_counts': {name: len(values) for name, values in asserted.items()},
        'inferred_counts': counts,
        'count_scope': 'Local resource IRIs only; external sameAs aliases excluded',
        'nolan_inferred_classes': [name for name in DEFINED if (nolan, RDF.type, EX[name]) in g],
        'detected_errors': errors,
    }
    write_json(ROOT / 'evidence/ontology_reasoning.json', report)
    result = Graph()
    result.bind('ex', EX)
    result.bind('res', RES)
    for name in DEFINED:
        for subject in members[name]:
            result.add((subject, RDF.type, EX[name]))
            for label in g.objects(subject, RDFS.label):
                result.add((subject, RDFS.label, label))
    result.serialize(ROOT / 'data/processed/inferred_classes.ttl', format='turtle')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit('Reasoning detected errors; inspect evidence/ontology_reasoning.json')


if __name__ == '__main__':
    run()

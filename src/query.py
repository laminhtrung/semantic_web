"""SPARQL terminal: python src/query.py queries/01_films.rq [--reasoned]"""
import argparse
from pathlib import Path
from rdflib import Graph
from common import ROOT

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('file',type=Path)
    p.add_argument('--reasoned',action='store_true',help='also load ontology/movie.ttl (class hierarchy) and data/processed/inferred_classes.ttl (run src/reason.py first)')
    args=p.parse_args()
    g=Graph().parse(ROOT/'data/processed/movies.ttl')
    if args.reasoned:
        g.parse(ROOT/'ontology/movie.ttl')
        g.parse(ROOT/'data/processed/inferred_classes.ttl')
    result=g.query(args.file.read_text(encoding='utf-8'))
    serialized=result.serialize(format='json' if result.type in ['SELECT','ASK'] else 'turtle')
    print(serialized.decode() if isinstance(serialized,bytes) else serialized)

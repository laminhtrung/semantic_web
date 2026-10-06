"""SPARQL terminal: python src/query.py queries/01_films.rq"""
import argparse
from pathlib import Path
from rdflib import Graph
from common import ROOT

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('file',type=Path);args=p.parse_args()
    g=Graph().parse(ROOT/'data/processed/movies.ttl')
    result=g.query(args.file.read_text(encoding='utf-8'))
    serialized=result.serialize(format='json' if result.type in ['SELECT','ASK'] else 'turtle')
    print(serialized.decode() if isinstance(serialized,bytes) else serialized)

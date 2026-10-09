"""Read-only query runner for the version-3 asserted/reasoned/named graphs."""
import argparse
from rdflib import Graph,Dataset
from common import ROOT
p=argparse.ArgumentParser();p.add_argument('query');p.add_argument('--mode',choices=['asserted','reasoned','dataset'],default='reasoned');a=p.parse_args()
folder=ROOT/'evidence/ontology_design'
if a.mode=='dataset':g=Dataset().parse(folder/'before_after.trig',format='trig')
else:
    g=Graph().parse(folder/'asserted.ttl')
    if a.mode=='reasoned':g+=Graph().parse(folder/'schema.ttl')+Graph().parse(folder/'inferred.ttl')
r=g.query((ROOT/a.query).read_text())
print(r.serialize(format='json').decode() if r.type in ['SELECT','ASK'] else r.graph.serialize(format='turtle'))

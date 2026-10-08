"""Demonstrate class inference without changing the asserted application dataset."""
import json
from rdflib import Graph, RDF, RDFS, URIRef
from owlrl import DeductiveClosure, OWLRL_Semantics
from common import ROOT, EX, RES, write_json

# Inferred via owl:equivalentClass + owl:someValuesFrom / owl:unionOf / owl:hasValue (OWL RL covers these).
RL_DEFINED = ['ActingContribution', 'DirectingContribution', 'WritingContribution', 'ProducingContribution',
              'Actor', 'Filmmaker', 'AwardWinner',
              'ActionFilm', 'ComedyFilm', 'DramaFilm', 'ScienceFictionFilm', 'AwardWinningFilm']

# Inferred via owl:minQualifiedCardinality with N>=2. The W3C OWL 2 RL profile only has rules for
# qualified cardinality of 0 or 1 (see cls-maxqc1/cls-maxqc2 in the OWL 2 RL spec); N>=2 is a valid
# OWL DL construct requiring sufficiently many provably different fillers, but owlrl's rule-based
# DeductiveClosure silently skips it. We classify by distinct RDF terms with a SPARQL aggregate
# instead. This is an application rule, not the same OWL DL entailment: distinct IRIs need not
# denote different individuals unless the ontology establishes their inequality.
CARDINALITY_DEFINED = ['MultiGenreFilm', 'FilmStudio']
DEFINED = RL_DEFINED + CARDINALITY_DEFINED

#  owl:sameAs substitution (owlrl eq-rep rules) also projects every inferred triple onto each
#  film's external Wikidata/DBpedia alias, and duplicates the *same* local film across those
#  aliases. Both the typed subject and the counted object are restricted to local res: IRIs so
#  that alias duplicates of one film don't inflate the cardinality past the real local count.
CARDINALITY_QUERIES = {
    'MultiGenreFilm': '''
        PREFIX ex: <{ex}>
        PREFIX dbo: <http://dbpedia.org/ontology/>
        SELECT ?s WHERE {{
          ?s a dbo:Film ; ex:hasGenre ?g .
          FILTER(STRSTARTS(STR(?s), "{res}"))
          FILTER(STRSTARTS(STR(?g), "{res}"))
        }} GROUP BY ?s HAVING (COUNT(DISTINCT ?g) >= 2)
    ''',
    'FilmStudio': '''
        PREFIX ex: <{ex}>
        SELECT ?s WHERE {{
          ?s a ex:ProductionCompany ; ex:productionOf ?f .
          FILTER(STRSTARTS(STR(?s), "{res}"))
          FILTER(STRSTARTS(STR(?f), "{res}"))
        }} GROUP BY ?s HAVING (COUNT(DISTINCT ?f) >= 3)
    ''',
}


def infer(g):
    closure = DeductiveClosure(OWLRL_Semantics)
    closure.expand(g)
    # ex:productionOf is only materialized above (via the inverseOf rule), so the cardinality
    # queries must run after expand(), not before.
    for name in CARDINALITY_DEFINED:
        query = CARDINALITY_QUERIES[name].format(ex=str(EX), res=str(RES))
        for row in g.query(query):
            g.add((row.s, RDF.type, EX[name]))
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
        'method': 'owlrl OWL RL/RDF rule closure for RL_DEFINED; direct SPARQL aggregate materialization '
                  'for CARDINALITY_DEFINED (N>=2 qualified cardinality is outside the OWL RL profile); '
                  'not a complete OWL DL consistency proof',
        'rl_defined': RL_DEFINED,
        'cardinality_defined': CARDINALITY_DEFINED,
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

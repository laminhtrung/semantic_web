import sys
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL, URIRef
from rdflib.compare import isomorphic
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from common import ROOT, DBO, EX, RES
from build import schema
from reason import infer, DEFINED


def test_generated_schema_matches_owl_exports():
    expected = schema()
    assert isomorphic(expected, Graph().parse(ROOT / 'ontology/movie.ttl'))
    assert isomorphic(expected, Graph().parse(ROOT / 'ontology/Movie_Ontology.owl'))
    named = {c for c in expected.subjects(RDF.type, OWL.Class) if isinstance(c, URIRef)}
    assert len(named) == 15
    assert all(expected.value(c, RDFS.comment) for c in named)


def test_real_data_classification():
    data = Graph().parse(ROOT / 'data/processed/movies.ttl')
    g = schema() + data
    assert all(not any(data.subjects(RDF.type, EX[name])) for name in DEFINED)
    assert not infer(g)
    expected = {
        'Director': set(data.objects(None, DBO.director)),
        'Actor': set(data.objects(None, DBO.starring)),
        'Screenwriter': set(data.objects(None, DBO.writer)),
        'CreditedFilm': set(data.subjects(EX.hasCredit, None)),
    }
    expected['FilmContributor'] = expected['Director'] | expected['Actor'] | expected['Screenwriter']
    expected['DirectorWriter'] = expected['Director'] & expected['Screenwriter']
    for name, subjects in expected.items():
        local = {s for s in g.subjects(RDF.type, EX[name]) if str(s).startswith(str(RES))}
        assert local == subjects
    assert (RES['person-Q25191'], RDF.type, EX.DirectorWriter) in g


def test_overlap_open_world_and_disjointness():
    g = schema()
    person, film, other = map(URIRef, ['urn:test:person', 'urn:test:film', 'urn:test:other'])
    g.add((film, DBO.director, person))
    # DirectorWriter permits different films for the two roles.
    g.add((other, DBO.writer, person))
    assert not infer(g)
    assert (person, RDF.type, EX.DirectorWriter) in g
    assert (person, RDF.type, EX.FilmContributor) in g
    assert (person, RDF.type, EX.Actor) not in g
    assert (film, RDF.type, EX.CreditedFilm) not in g
    assert (DBO.Film, OWL.disjointWith, DBO.Country) in g
    g.add((film, RDF.type, DBO.Country))
    assert infer(g), 'A film typed as a country must produce an inconsistency diagnostic.'

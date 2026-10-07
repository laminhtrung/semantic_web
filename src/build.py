"""Build a richer OWL model, normalize collected claims, and publish static RDF pages."""
import csv
import hashlib
import html
import json
from decimal import Decimal, InvalidOperation
from pathlib import Path
from rdflib import Graph, URIRef, Literal, BNode, RDF, RDFS, OWL, XSD
from rdflib.collection import Collection
from common import ROOT, CONFIG, BASE, EX, RES, DBO, PROV, VOID, DCT, write_json
from collect import claim_ids

def graph():
    g = Graph()
    for name, ns in [('ex', EX), ('res',RES),('dbo',DBO),('prov',PROV),('void',VOID),('dct',DCT),('owl',OWL),('rdfs',RDFS),('xsd',XSD)]:
        g.bind(name, ns)
    return g

# Genres and awards are classified from the real labels Wikidata returned, not invented.
GENRE_KEYWORDS = [('documentary', EX.DocumentaryGenre), ('science fiction', EX.ScienceFictionGenre),
                   ('action', EX.ActionGenre), ('comedy', EX.ComedyGenre), ('drama', EX.DramaGenre)]
AWARD_KEYWORDS = [(('actor', 'actress'), EX.ActingAward), (('director', 'directing'), EX.DirectingAward),
                   (('screenplay', 'writing', 'screenwriting'), EX.WritingAward)]

def classify_genre(label):
    low = label.lower()
    return [iri for keyword, iri in GENRE_KEYWORDS if keyword in low]

def classify_award(label):
    low = label.lower()
    hits = [iri for keywords, iri in AWARD_KEYWORDS if any(k in low for k in keywords)]
    return hits or [EX.FilmAward]

def schema():
    g = graph()
    ontology = URIRef(BASE+'/ontology')
    g.add((ontology,RDF.type,OWL.Ontology))
    g.add((ontology,RDFS.label,Literal('MovieLOD — movie ontology',lang='en')))
    g.add((ontology,OWL.versionInfo,Literal('2.0.0')))
    g.add((ontology,DCT.license,URIRef(CONFIG['data_license'])))

    def cls(iri, label, comment, parent=None, equiv=None):
        g.add((iri, RDF.type, OWL.Class))
        g.add((iri, RDFS.label, Literal(label, lang='en')))
        g.add((iri, RDFS.comment, Literal(comment, lang='en')))
        if parent is not None:
            g.add((iri, RDFS.subClassOf, parent))
        if equiv is not None:
            g.add((iri, OWL.equivalentClass, equiv))
        return iri

    def intersection(*members):
        b = BNode(); g.add((b, RDF.type, OWL.Class))
        head = BNode(); g.add((b, OWL.intersectionOf, head)); Collection(g, head, list(members))
        return b

    def union(*members):
        b = BNode(); g.add((b, RDF.type, OWL.Class))
        head = BNode(); g.add((b, OWL.unionOf, head)); Collection(g, head, list(members))
        return b

    def some(prop, filler):
        r = BNode(); g.add((r, RDF.type, OWL.Restriction))
        g.add((r, OWL.onProperty, prop)); g.add((r, OWL.someValuesFrom, filler))
        return r

    def has_value(prop, individual):
        r = BNode(); g.add((r, RDF.type, OWL.Restriction))
        g.add((r, OWL.onProperty, prop)); g.add((r, OWL.hasValue, individual))
        return r

    def min_qualified(prop, n, filler_cls):
        r = BNode(); g.add((r, RDF.type, OWL.Restriction))
        g.add((r, OWL.onProperty, prop)); g.add((r, OWL.onClass, filler_cls))
        g.add((r, OWL.minQualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)))
        return r

    def exactly_one(prop, filler_cls):
        r = BNode(); g.add((r, RDF.type, OWL.Restriction))
        g.add((r, OWL.onProperty, prop)); g.add((r, OWL.onClass, filler_cls))
        g.add((r, OWL.qualifiedCardinality, Literal(1, datatype=XSD.nonNegativeInteger)))
        return r

    def all_values(prop, filler_cls):
        r = BNode(); g.add((r, RDF.type, OWL.Restriction))
        g.add((r, OWL.onProperty, prop)); g.add((r, OWL.allValuesFrom, filler_cls))
        return r

    # --- Top-level branches --------------------------------------------------
    cls(EX.CreativeWork, 'Creative work', 'A named work of authorship; the top-level branch for films.')
    cls(DBO.Film, 'Film', 'A film work, distinct from people, organizations and metadata records.', parent=EX.CreativeWork)
    cls(EX.Agent, 'Agent', 'An entity able to contribute to a creative work: a person or an organization.')
    cls(DBO.Person, 'Person', 'A human who may hold several film contribution roles.', parent=EX.Agent)
    cls(EX.Organization, 'Organization', 'A company able to produce films.', parent=EX.Agent)
    cls(EX.ProductionCompany, 'Production company', 'An organization credited with producing a film (wdt:P272).', parent=EX.Organization)
    cls(EX.Contribution, 'Contribution', 'A record connecting exactly one person, one film and one role.')
    cls(EX.ContributionRole, 'Contribution role', 'A role such as director, actor, writer or producer; not a person.')
    cls(EX.Genre, 'Genre', 'A category used to describe a film genre.', equiv=DBO.Genre)
    cls(EX.FictionGenre, 'Fiction genre', 'A genre denoting fictional narrative film.', parent=EX.Genre)
    cls(EX.NonFictionGenre, 'Non-fiction genre', 'A genre denoting non-fictional film.', parent=EX.Genre)
    cls(DBO.Country, 'Country', 'A country associated with film production.')
    cls(EX.Language, 'Language', 'A language associated with a film.', equiv=DBO.Language)
    cls(EX.Award, 'Award', 'A recognition received by a film or by a person for film work (wdt:P166).')
    cls(EX.SourceSnapshot, 'Source snapshot', 'A saved source response with a URL, retrieval time and SHA-256 hash.')
    cls(EX.Dataset, 'Dataset', 'The published collection of movie data, aligned with void:Dataset.', equiv=VOID.Dataset)

    # --- Film subclasses: explicit, asserted directly from Wikidata P31 (instance of) ---
    cls(EX.FeatureFilm, 'Feature film', 'A theatrically released narrative film; asserted for wd:Q11424 instances in this sample.', parent=DBO.Film)
    cls(EX.AnimatedFilm, 'Animated film', 'A film whose P31 instance-of is an animation kind (e.g. wd:Q20650540 anime film).', parent=DBO.Film)
    cls(EX.DocumentaryFilm, 'Documentary film', 'A non-fiction film. Defined for completeness; the current 30-film sample contains no documentaries (see docs).', parent=DBO.Film)

    # --- Genre subclasses: explicit, classified from the real Wikidata genre label (see classify_genre) ---
    cls(EX.ActionGenre, 'Action genre', 'A genre whose Wikidata label contains "action".', parent=EX.FictionGenre)
    cls(EX.ComedyGenre, 'Comedy genre', 'A genre whose Wikidata label contains "comedy".', parent=EX.FictionGenre)
    cls(EX.DramaGenre, 'Drama genre', 'A genre whose Wikidata label contains "drama".', parent=EX.FictionGenre)
    cls(EX.ScienceFictionGenre, 'Science fiction genre', 'A genre whose Wikidata label contains "science fiction".', parent=EX.FictionGenre)
    cls(EX.DocumentaryGenre, 'Documentary genre', 'A genre whose Wikidata label contains "documentary". Defined for completeness; 0 films in this sample carry it.', parent=EX.NonFictionGenre)

    # --- Award subclasses: explicit, classified from the real Wikidata award label (see classify_award) ---
    cls(EX.FilmAward, 'Film award', 'An award category not specific to one contribution role (e.g. Best Picture, Best Editing).', parent=EX.Award)
    cls(EX.ActingAward, 'Acting award', 'An award category for acting (label contains "actor"/"actress").', parent=EX.Award)
    cls(EX.DirectingAward, 'Directing award', 'An award category for directing (label contains "director"/"directing").', parent=EX.Award)
    cls(EX.WritingAward, 'Writing award', 'An award category for screenwriting (label contains "screenplay"/"writing").', parent=EX.Award)

    # --- Contribution-kind subclasses: INFERRED from ex:hasRole via owl:hasValue (see reason.py) ---
    cls(EX.ActingContribution, 'Acting contribution', 'A contribution whose role is ex:ActorRole.', parent=EX.Contribution,
        equiv=intersection(EX.Contribution, has_value(EX.hasRole, EX.ActorRole)))
    cls(EX.DirectingContribution, 'Directing contribution', 'A contribution whose role is ex:DirectorRole.', parent=EX.Contribution,
        equiv=intersection(EX.Contribution, has_value(EX.hasRole, EX.DirectorRole)))
    cls(EX.WritingContribution, 'Writing contribution', 'A contribution whose role is ex:WriterRole.', parent=EX.Contribution,
        equiv=intersection(EX.Contribution, has_value(EX.hasRole, EX.WriterRole)))
    cls(EX.ProducingContribution, 'Producing contribution', 'A contribution whose role is ex:ProducerRole.', parent=EX.Contribution,
        equiv=intersection(EX.Contribution, has_value(EX.hasRole, EX.ProducerRole)))

    # --- Person-level INFERRED classes, built on top of the Contribution model ---
    cls(EX.Actor, 'Actor', 'A person who holds at least one acting contribution.', parent=DBO.Person,
        equiv=intersection(DBO.Person, some(EX.hasContribution, EX.ActingContribution)))
    cls(EX.Filmmaker, 'Filmmaker', 'A person who directed, wrote or produced at least one film.', parent=DBO.Person,
        equiv=intersection(DBO.Person, union(some(EX.hasContribution, EX.DirectingContribution),
                                              some(EX.hasContribution, EX.WritingContribution),
                                              some(EX.hasContribution, EX.ProducingContribution))))
    cls(EX.AwardWinner, 'Award winner', 'A person who has received at least one award.', parent=DBO.Person,
        equiv=intersection(DBO.Person, some(EX.hasAward, EX.Award)))

    # --- Film-level INFERRED classes ---
    cls(EX.ActionFilm, 'Action film', 'A film that has at least one action genre.', parent=DBO.Film,
        equiv=intersection(DBO.Film, some(EX.hasGenre, EX.ActionGenre)))
    cls(EX.ComedyFilm, 'Comedy film', 'A film that has at least one comedy genre.', parent=DBO.Film,
        equiv=intersection(DBO.Film, some(EX.hasGenre, EX.ComedyGenre)))
    cls(EX.DramaFilm, 'Drama film', 'A film that has at least one drama genre.', parent=DBO.Film,
        equiv=intersection(DBO.Film, some(EX.hasGenre, EX.DramaGenre)))
    cls(EX.ScienceFictionFilm, 'Science fiction film', 'A film that has at least one science fiction genre.', parent=DBO.Film,
        equiv=intersection(DBO.Film, some(EX.hasGenre, EX.ScienceFictionGenre)))
    cls(EX.MultiGenreFilm, 'Multi-genre film', 'A film tagged with at least two distinct genres.', parent=DBO.Film,
        equiv=intersection(DBO.Film, min_qualified(EX.hasGenre, 2, EX.Genre)))
    cls(EX.AwardWinningFilm, 'Award-winning film', 'A film that has received at least one award.', parent=DBO.Film,
        equiv=intersection(DBO.Film, some(EX.hasAward, EX.Award)))

    # --- Organization-level INFERRED class ---
    cls(EX.FilmStudio, 'Film studio', 'A production company credited on at least three films in this dataset.', parent=EX.ProductionCompany,
        equiv=intersection(EX.ProductionCompany, min_qualified(EX.productionOf, 3, DBO.Film)))

    # --- Object properties ------------------------------------------------
    def obj_prop(iri, label, domain, ran, inverse=None, functional=False):
        g.add((iri, RDF.type, OWL.ObjectProperty))
        g.add((iri, RDFS.label, Literal(label, lang='en')))
        if domain is not None:
            g.add((iri, RDFS.domain, domain))
        g.add((iri, RDFS.range, ran))
        if inverse is not None:
            g.add((iri, OWL.inverseOf, inverse))
        if functional:
            g.add((iri, RDF.type, OWL.FunctionalProperty))

    obj_prop(EX.hasGenre, 'Has genre', DBO.Film, EX.Genre)
    obj_prop(EX.genreOf, 'Genre of', EX.Genre, DBO.Film, inverse=EX.hasGenre)
    obj_prop(EX.country, 'Production country', DBO.Film, DBO.Country)
    obj_prop(EX.language, 'Original language', DBO.Film, EX.Language)
    obj_prop(EX.sourceSnapshot, 'Source snapshot', None, EX.SourceSnapshot)

    obj_prop(EX.hasContribution, 'Has contribution', DBO.Person, EX.Contribution)
    obj_prop(EX.contributionBy, 'Contribution by', EX.Contribution, DBO.Person, inverse=EX.hasContribution, functional=True)
    obj_prop(EX.contributionTo, 'Contribution to', EX.Contribution, DBO.Film, functional=True)
    obj_prop(EX.contributionOf, 'Contribution of', DBO.Film, EX.Contribution, inverse=EX.contributionTo)
    obj_prop(EX.hasRole, 'Has role', EX.Contribution, EX.ContributionRole, functional=True)
    obj_prop(EX.roleOf, 'Role of', EX.ContributionRole, EX.Contribution, inverse=EX.hasRole)

    obj_prop(EX.hasProductionCompany, 'Has production company', DBO.Film, EX.ProductionCompany)
    obj_prop(EX.productionOf, 'Production of', EX.ProductionCompany, DBO.Film, inverse=EX.hasProductionCompany)

    obj_prop(EX.directed, 'Directed', DBO.Person, DBO.Film)
    obj_prop(EX.actedIn, 'Acted in', DBO.Person, DBO.Film)
    obj_prop(EX.wrote, 'Wrote', DBO.Person, DBO.Film)
    obj_prop(EX.produced, 'Produced', DBO.Person, DBO.Film)
    for prop, inv in [(DBO.director, EX.directed), (DBO.starring, EX.actedIn), (DBO.writer, EX.wrote), (DBO.producer, EX.produced)]:
        g.add((prop, RDF.type, OWL.ObjectProperty))
        g.add((prop, RDFS.domain, DBO.Film)); g.add((prop, RDFS.range, DBO.Person)); g.add((prop, OWL.inverseOf, inv))

    # hasAward/awardOf: a Film or a Person can receive an award, so the domain/range is a union class.
    award_subject = union(DBO.Film, DBO.Person)
    g.add((EX.hasAward, RDF.type, OWL.ObjectProperty)); g.add((EX.hasAward, RDFS.label, Literal('Has award', lang='en')))
    g.add((EX.hasAward, RDFS.domain, award_subject)); g.add((EX.hasAward, RDFS.range, EX.Award))
    g.add((EX.awardOf, RDF.type, OWL.ObjectProperty)); g.add((EX.awardOf, RDFS.label, Literal('Award of', lang='en')))
    g.add((EX.awardOf, RDFS.domain, EX.Award)); g.add((EX.awardOf, RDFS.range, award_subject)); g.add((EX.awardOf, OWL.inverseOf, EX.hasAward))

    # --- Datatype properties -----------------------------------------------
    for name, t in [('title', XSD.string), ('releaseYear', XSD.integer), ('runtimeMinutes', XSD.decimal)]:
        g.add((EX[name], RDF.type, OWL.DatatypeProperty)); g.add((EX[name], RDFS.domain, DBO.Film)); g.add((EX[name], RDFS.range, t))
    for name, t in [('sourceUrl', XSD.anyURI), ('retrievedAt', XSD.dateTime), ('sha256', XSD.string)]:
        g.add((EX[name], RDF.type, OWL.DatatypeProperty)); g.add((EX[name], RDFS.domain, EX.SourceSnapshot)); g.add((EX[name], RDFS.range, t))

    # --- Cardinality restrictions on the Contribution association class ----
    for prop, filler in [(EX.contributionBy, DBO.Person), (EX.contributionTo, DBO.Film), (EX.hasRole, EX.ContributionRole)]:
        g.add((EX.Contribution, RDFS.subClassOf, exactly_one(prop, filler)))
        g.add((EX.Contribution, RDFS.subClassOf, all_values(prop, filler)))

    # --- Contribution role individuals --------------------------------------
    for name, label in [('DirectorRole', 'Director'), ('ActorRole', 'Actor'), ('WriterRole', 'Writer'), ('ProducerRole', 'Producer')]:
        g.add((EX[name], RDF.type, EX.ContributionRole)); g.add((EX[name], RDF.type, OWL.NamedIndividual))
        g.add((EX[name], RDFS.label, Literal(label, lang='en')))
    b = BNode(); g.add((b, RDF.type, OWL.AllDifferent)); l = BNode(); g.add((b, OWL.distinctMembers, l))
    Collection(g, l, [EX.DirectorRole, EX.ActorRole, EX.WriterRole, EX.ProducerRole])

    # --- Disjointness across the base partition (not their parents/subclasses) ---
    base_classes = [DBO.Film, DBO.Person, EX.Organization, EX.Genre, DBO.Country, EX.Language,
                    EX.Contribution, EX.ContributionRole, EX.SourceSnapshot, EX.Dataset, EX.Award]
    distinct = BNode(); g.add((distinct, RDF.type, OWL.AllDisjointClasses))
    members = BNode(); g.add((distinct, OWL.members, members)); Collection(g, members, base_classes)

    return g

def preferred_values(entity,prop):
    claims = [c for c in entity.get('claims',{}).get(prop,[]) if c.get('rank')!='deprecated']
    preferred=[c for c in claims if c.get('rank')=='preferred']
    return [c['mainsnak']['datavalue']['value'] for c in (preferred or claims) if 'datavalue' in c.get('mainsnak',{})]

def build():
    source=json.loads((ROOT/'data/processed/collected.json').read_text())
    snapshots=json.loads((ROOT/'data/raw/snapshots.json').read_text())
    entities=source['entities']; sg=schema(); g=graph()
    for role in [EX.DirectorRole,EX.ActorRole,EX.WriterRole,EX.ProducerRole]:
        for t in sg.triples((role,None,None)):g.add(t)
    snapshot_iris={}
    for snap in snapshots:
        s=RES['source-'+snap['sha256'][:24]];snapshot_iris[snap['url']]=s
        g.add((s,RDF.type,EX.SourceSnapshot));g.add((s,EX.sourceUrl,Literal(snap['url'],datatype=XSD.anyURI)))
        g.add((s,EX.retrievedAt,Literal(snap['retrieved_at'],datatype=XSD.dateTime)))
        g.add((s,EX.sha256,Literal(snap['sha256'])));g.add((s,PROV.wasDerivedFrom,URIRef(snap['url'])))
        g.add((s,RDFS.label,Literal(snap['provider']+' source snapshot')))
    links, records, issues=[],[],[]
    def add_link(local,external,method):
        g.add((local,OWL.sameAs,URIRef(external)))
        links.append({'local':str(local),'external':external,'method':method})
    def add_entity(qid,kind):
        entity=entities.get(qid)
        if not entity or not entity.get('labels',{}).get('en'):
            issues.append({'entity':qid,'reason':'missing English label; omitted'})
            return None
        if kind=='person' and 'Q5' not in claim_ids(entity,'P31'):
            issues.append({'entity':qid,'reason':'not explicitly a human; omitted from Person'})
            return None
        local=RES[kind+'-'+qid]
        typ={'person':DBO.Person,'genre':EX.Genre,'country':DBO.Country,'language':EX.Language,
             'company':EX.ProductionCompany,'award':EX.Award}[kind]
        label=entity['labels']['en']['value']
        g.add((local,RDF.type,typ));g.add((local,RDFS.label,Literal(label,lang='en')))
        if kind=='genre':
            for extra in classify_genre(label):g.add((local,RDF.type,extra))
        if kind=='award':
            for extra in classify_award(label):g.add((local,RDF.type,extra))
        add_link(local,'http://www.wikidata.org/entity/'+qid,'exact Wikidata QID from source claim')
        if entity.get('_snapshot_url'):
            g.add((local,EX.sourceSnapshot,snapshot_iris[entity['_snapshot_url']]))
        return local
    for film in source['films']:
        entity=entities[film['qid']];local=RES['film-'+film['qid']]
        title=entity.get('labels',{}).get('en',{}).get('value',film['wiki_title'])
        g.add((local,RDF.type,DBO.Film));g.add((local,EX.title,Literal(title)));g.add((local,RDFS.label,Literal(title,lang='en')))
        # Film-kind subclass: explicit, from Wikidata P31 instance-of (see ontology/movie.ttl comments).
        film_types=claim_ids(entity,'P31')
        g.add((local,RDF.type,EX.AnimatedFilm if 'Q20650540' in film_types else EX.FeatureFilm))
        sn=snapshot_iris[film['wikidata_snapshot']];g.add((local,EX.sourceSnapshot,sn))
        g.add((local,PROV.wasDerivedFrom,URIRef('https://www.wikidata.org/wiki/'+film['qid'])))
        add_link(local,'http://www.wikidata.org/entity/'+film['qid'],'exact enwiki sitelink: '+film['wiki_title'])
        if film.get('dbpedia_uri'):
            add_link(local,film['dbpedia_uri'],'same enwiki title + DBpedia root rdf:type dbo:Film')
            g.add((local,EX.sourceSnapshot,snapshot_iris[film['dbpedia_snapshot']]))
        years=[]
        for value in preferred_values(entity,'P577'):
            if isinstance(value,dict) and value.get('time','').startswith('+') and value.get('precision',0)>=9 and value.get('calendarmodel','').endswith('Q1985727'):
                year=int(value['time'][1:5])
                if 1888<=year<=2100:years.append(year)
        year=min(years) if years else None
        if year:g.add((local,EX.releaseYear,Literal(year,datatype=XSD.integer)))
        minutes=[]
        for value in preferred_values(entity,'P2047'):
            if not isinstance(value,dict):continue
            try:
                amount=Decimal(value['amount']);unit=value.get('unit','')
                if unit.endswith('/Q7727'):m=amount
                elif unit.endswith('/Q11574'):m=amount/60
                elif unit.endswith('/Q25235'):m=amount*60
                else:continue
                if 0<m<1000:minutes.append(m)
            except (InvalidOperation,KeyError):continue
        runtime=minutes[0] if minutes else None
        if len(set(minutes))>1:issues.append({'film':title,'reason':'multiple runtimes; first non-deprecated/preferred claim retained','values':[str(m) for m in minutes]})
        if runtime is not None:
            decimal_text=format(runtime,'f')
            if '.' not in decimal_text:decimal_text+='.0'
            g.add((local,EX.runtimeMinutes,Literal(decimal_text,datatype=XSD.decimal)))
        for prop,kind,pred in [('P136','genre',EX.hasGenre),('P495','country',EX.country),('P364','language',EX.language),
                                ('P166','award',EX.hasAward),('P272','company',EX.hasProductionCompany)]:
            for qid in claim_ids(entity,prop):
                target=add_entity(qid,kind)
                if target:g.add((local,pred,target))
        people={'director':[],'actor':[],'writer':[],'producer':[]}
        for prop,kind,pred,role in [('P57','director',DBO.director,EX.DirectorRole),('P161','actor',DBO.starring,EX.ActorRole),
                                     ('P58','writer',DBO.writer,EX.WriterRole),('P162','producer',DBO.producer,EX.ProducerRole)]:
            for qid in claim_ids(entity,prop):
                target=add_entity(qid,'person')
                if not target:continue
                contribution=RES['contribution-'+film['qid']+'-'+qid+'-'+kind]
                for triple in [(local,pred,target),(local,EX.contributionOf,contribution),(contribution,RDF.type,EX.Contribution),
                               (contribution,EX.contributionTo,local),(contribution,EX.contributionBy,target),
                               (contribution,EX.hasRole,role),(target,EX.hasContribution,contribution),
                               (contribution,EX.sourceSnapshot,sn)]:g.add(triple)
                g.add((contribution,RDFS.label,Literal(title+' — '+kind+' — '+entities[qid]['labels']['en']['value'])))
                for award_qid in claim_ids(entities[qid],'P166'):
                    award_target=add_entity(award_qid,'award')
                    if award_target:g.add((target,EX.hasAward,award_target))
                people[kind].append({'name':entities[qid]['labels']['en']['value'],'uri':str(target)})
        records.append({'uri':str(local),'qid':film['qid'],'title':title,'year':year,'runtime_minutes':float(runtime) if runtime is not None else None, **people})
    dataset=URIRef(BASE+'/dataset')
    for triple in [(dataset,RDF.type,EX.Dataset),(dataset,RDF.type,VOID.Dataset),(dataset,DCT.title,Literal('MovieLOD course dataset')),
                   (dataset,DCT.license,URIRef(CONFIG['data_license'])),(dataset,DCT.source,URIRef('https://www.wikidata.org/')),
                   (dataset,DCT.source,URIRef('https://dbpedia.org/')),(dataset,VOID.dataDump,URIRef(BASE+'/data/movies.ttl')),
                   (dataset,RDFS.seeAlso,URIRef(BASE+'/#query'))]:g.add(triple)
    (ROOT/'ontology').mkdir(exist_ok=True)
    sg.serialize(ROOT/'ontology/movie.ttl',format='turtle');sg.serialize(ROOT/'ontology/Movie_Ontology.owl',format='xml')
    g.serialize(ROOT/'data/processed/movies.ttl',format='turtle');g.serialize(ROOT/'data/processed/movies.jsonld',format='json-ld')
    combined=g+sg;combined.serialize(ROOT/'ontology/Movie_Knowledge_Graph.owl',format='xml')
    # Remove repeated audit rows for reused people/terms.
    links=list({(x['local'],x['external']):x for x in links}.values())
    write_json(ROOT/'evidence/link_audit.json',sorted(links,key=lambda x:(x['local'],x['external'])))
    write_json(ROOT/'evidence/quality_issues.json',issues)
    with (ROOT/'data/processed/films.csv').open('w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=['qid','title','year','runtime_minutes','directors'])
        writer.writeheader()
        for r in records:writer.writerow({k:r.get(k) for k in ['qid','title','year','runtime_minutes']}|{'directors':'; '.join(x['name'] for x in r['director'])})
    stats={'films':len(records),'persons':len(set(g.subjects(RDF.type,DBO.Person))), 'contributions':len(set(g.subjects(RDF.type,EX.Contribution))),
           'genres':len(set(g.subjects(RDF.type,EX.Genre))),'countries':len(set(g.subjects(RDF.type,DBO.Country))),
           'languages':len(set(g.subjects(RDF.type,EX.Language))),'production_companies':len(set(g.subjects(RDF.type,EX.ProductionCompany))),
           'awards':len(set(g.subjects(RDF.type,EX.Award))),'snapshots':len(snapshots),'data_triples':len(g),'schema_triples':len(sg),
           'classes':len({c for c in sg.subjects(RDF.type,OWL.Class) if isinstance(c, URIRef)}),
           'reused_dbpedia_classes':['http://dbpedia.org/ontology/'+name for name in ['Film','Person','Country']],
           'same_as':len(links),'dbpedia_links':sum('dbpedia.org' in x['external'] for x in links),
           'wikidata_links':sum('wikidata.org' in x['external'] for x in links),
           'with_year':sum(r['year'] is not None for r in records),'with_runtime':sum(r['runtime_minutes'] is not None for r in records),
           'with_director':sum(bool(r['director']) for r in records),'base_url':BASE}
    write_json(ROOT/'evidence/statistics.json',stats)
    export_static(g,sg,records,stats)
    print(json.dumps(stats,ensure_ascii=False,indent=2))

def export_static(g,sg,records,stats):
    import shutil
    dist=ROOT/'web/dist';data=dist/'data';data.mkdir(parents=True,exist_ok=True)
    for name in ['movies.ttl','movies.jsonld','films.csv']:
        shutil.copy2(ROOT/'data/processed'/name,data/name)
    shutil.copy2(ROOT/'ontology/movie.ttl',dist/'ontology.ttl')
    shutil.copy2(ROOT/'ontology/Movie_Ontology.owl',dist/'Movie_Ontology.owl')
    shutil.copy2(ROOT/'ontology/Movie_Knowledge_Graph.owl',dist/'Movie_Knowledge_Graph.owl')
    write_json(data/'films.json',sorted(records,key=lambda x:x['title']))
    write_json(data/'statistics.json',stats)
    for s in set(g.subjects()):
        if isinstance(s,URIRef) and str(s).startswith(str(RES)):
            render_resource(g,s,dist/'resource'/str(s).removeprefix(str(RES)))
    render_resource(g,URIRef(BASE+'/dataset'),dist/'dataset')
    render_resource(sg,URIRef(BASE+'/ontology'),dist/'ontology',include_all=True)
    (dist/'_headers').write_text('/data/*\n  Access-Control-Allow-Origin: *\n/ontology.ttl\n  Content-Type: text/turtle; charset=utf-8\n/data/movies.ttl\n  Content-Type: text/turtle; charset=utf-8\n/resource/*/index.ttl\n  Content-Type: text/turtle; charset=utf-8\n',encoding='utf-8')

def render_resource(g,s,directory,include_all=False):
    directory.mkdir(parents=True,exist_ok=True)
    sub=g if include_all else graph()
    if not include_all:
        for triple in g.triples((s,None,None)):sub.add(triple)
    sub.serialize(directory/'index.ttl',format='turtle')
    label=str(g.value(s,RDFS.label) or g.value(s,DCT.title) or str(s).rsplit('/',1)[-1])
    def display(term):
        text=str(term);name=text.rsplit('#',1)[-1].rsplit('/',1)[-1]
        if isinstance(term,URIRef):
            href=text
            if text.startswith(BASE):href=text[len(BASE):] or '/'
            return '<a href="'+html.escape(href,quote=True)+'">'+html.escape(str(g.value(term,RDFS.label) or name))+'</a>'
        return html.escape(text)
    rows=''.join('<tr><td>'+display(p)+'</td><td>'+display(o)+'</td></tr>' for p,o in sorted(g.predicate_objects(s),key=lambda x:(str(x[0]),str(x[1]))))
    extra=''
    if include_all:
        for subject in sorted(set(g.subjects(RDF.type,OWL.Class))|set(g.subjects(RDF.type,EX.ContributionRole)),key=str):
            anchor=str(subject).split('#')[-1].rsplit('/',1)[-1]
            label2=str(g.value(subject,RDFS.label) or anchor)
            properties=''.join('<tr><td>'+display(p)+'</td><td>'+display(o)+'</td></tr>' for p,o in sorted(g.predicate_objects(subject),key=lambda x:(str(x[0]),str(x[1]))))
            extra+='<section id="'+html.escape(anchor,quote=True)+'"><h2>'+html.escape(anchor+' — '+label2)+'</h2><table>'+properties+'</table></section>'
    ld=sub.serialize(format='json-ld').replace('</','<\\/')
    path=str(s)[len(BASE):]
    body='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(label)+' · MovieLOD</title><link rel="stylesheet" href="/style.css"><link rel="alternate" type="text/turtle" href="'+path+'/index.ttl"><script type="application/ld+json">'+ld+'</script></head><body class="resource-page"><main><a href="/">← MovieLOD</a><h1>'+html.escape(label)+'</h1><p class="iri">'+html.escape(str(s))+'</p><p><a href="'+path+'/index.ttl">Download RDF (Turtle)</a></p><table><thead><tr><th>Property</th><th>Value</th></tr></thead><tbody>'+rows+'</tbody></table><footer>Source data: Wikidata, DBpedia. <a href="/LICENSE-DATA.txt">License and attribution</a>.</footer></main></body></html>'
    if extra:body=body.replace('<footer>',extra+'<footer>')
    (directory/'index.html').write_text(body,encoding='utf-8')

if __name__=='__main__':build()

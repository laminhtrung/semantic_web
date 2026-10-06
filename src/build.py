"""Build a small OWL model, normalize collected claims, and publish static RDF pages."""
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

def schema():
    g = graph()
    ontology = URIRef(BASE+'/ontology')
    g.add((ontology,RDF.type,OWL.Ontology))
    g.add((ontology,RDFS.label,Literal('MovieLOD — ontology điện ảnh tối giản',lang='vi')))
    g.add((ontology,OWL.versionInfo,Literal('1.0.0')))
    g.add((ontology,DCT.license,URIRef(CONFIG['data_license'])))
    classes = {
      'Film':('Phim',DBO.Film), 'Person':('Người',DBO.Person), 'Genre':('Thể loại',DBO.Genre),
      'Country':('Quốc gia',DBO.Country), 'Language':('Ngôn ngữ',DBO.Language),
      'Credit':('Bản ghi đóng góp',None), 'ContributionRole':('Vai trò đóng góp',None),
      'SourceSnapshot':('Bản ghi nguồn',None), 'Dataset':('Bộ dữ liệu',VOID.Dataset)}
    # Reuse these DBpedia class IRIs directly throughout the schema and data.
    reused = {'Film': DBO.Film, 'Person': DBO.Person, 'Country': DBO.Country}
    class_iris = {name: reused.get(name, EX[name]) for name in classes}
    for name,(label,alignment) in classes.items():
        class_iri = class_iris[name]
        g.add((class_iri, RDF.type,OWL.Class))
        g.add((class_iri,RDFS.label,Literal(label,lang='vi')))
        if alignment and class_iri != alignment:
            g.add((class_iri,OWL.equivalentClass,alignment))
    distinct = BNode()
    g.add((distinct,RDF.type,OWL.AllDisjointClasses))
    members = BNode()
    g.add((distinct,OWL.members,members))
    Collection(g,members,[class_iris[n] for n in classes])
    obj = {
      'inFilm':(EX.Credit,DBO.Film,'Thuộc phim'), 'participant':(EX.Credit,DBO.Person,'Người tham gia'),
      'role':(EX.Credit,EX.ContributionRole,'Vai trò'), 'hasCredit':(DBO.Film,EX.Credit,'Có đóng góp'),
      'hasGenre':(DBO.Film,EX.Genre,'Có thể loại'), 'country':(DBO.Film,DBO.Country,'Quốc gia sản xuất'),
      'language':(DBO.Film,EX.Language,'Ngôn ngữ gốc'), 'sourceSnapshot':(None,EX.SourceSnapshot,'Bản ghi nguồn'),
      'directed':(DBO.Person,DBO.Film,'Đã đạo diễn'), 'actedIn':(DBO.Person,DBO.Film,'Đã diễn xuất'),
      'wrote':(DBO.Person,DBO.Film,'Đã viết kịch bản')}
    for name,(domain,ran,label) in obj.items():
        g.add((EX[name],RDF.type,OWL.ObjectProperty))
        g.add((EX[name],RDFS.label,Literal(label,lang='vi')))
        if domain:g.add((EX[name],RDFS.domain,domain))
        g.add((EX[name],RDFS.range,ran))
    g.add((EX.inFilm,OWL.inverseOf,EX.hasCredit))
    for prop,inv in [(DBO.director,EX.directed),(DBO.starring,EX.actedIn),(DBO.writer,EX.wrote)]:
        g.add((prop,RDF.type,OWL.ObjectProperty))
        g.add((prop,RDFS.domain,DBO.Film));g.add((prop,RDFS.range,DBO.Person));g.add((prop,OWL.inverseOf,inv))
    for name,t in [('title',XSD.string),('releaseYear',XSD.integer),('runtimeMinutes',XSD.decimal)]:
        g.add((EX[name],RDF.type,OWL.DatatypeProperty));g.add((EX[name],RDFS.domain,DBO.Film));g.add((EX[name],RDFS.range,t))
    for name,t in [('sourceUrl',XSD.anyURI),('retrievedAt',XSD.dateTime),('sha256',XSD.string)]:
        g.add((EX[name],RDF.type,OWL.DatatypeProperty));g.add((EX[name],RDFS.domain,EX.SourceSnapshot));g.add((EX[name],RDFS.range,t))
    for prop,t in [(EX.inFilm,DBO.Film),(EX.participant,DBO.Person),(EX.role,EX.ContributionRole)]:
        g.add((prop,RDF.type,OWL.FunctionalProperty))
        r=BNode();g.add((EX.Credit,RDFS.subClassOf,r));g.add((r,RDF.type,OWL.Restriction))
        g.add((r,OWL.onProperty,prop));g.add((r,OWL.onClass,t));g.add((r,OWL.qualifiedCardinality,Literal(1,datatype=XSD.nonNegativeInteger)))
        r=BNode();g.add((EX.Credit,RDFS.subClassOf,r));g.add((r,RDF.type,OWL.Restriction))
        g.add((r,OWL.onProperty,prop));g.add((r,OWL.allValuesFrom,t))
    for name,label in [('DirectorRole','Đạo diễn'),('ActorRole','Diễn viên'),('WriterRole','Biên kịch')]:
        g.add((EX[name],RDF.type,EX.ContributionRole));g.add((EX[name],RDF.type,OWL.NamedIndividual))
        g.add((EX[name],RDFS.label,Literal(label,lang='vi')))
    b=BNode();g.add((b,RDF.type,OWL.AllDifferent));l=BNode();g.add((b,OWL.distinctMembers,l))
    Collection(g,l,[EX.DirectorRole,EX.ActorRole,EX.WriterRole])
    return g

def preferred_values(entity,prop):
    claims = [c for c in entity.get('claims',{}).get(prop,[]) if c.get('rank')!='deprecated']
    preferred=[c for c in claims if c.get('rank')=='preferred']
    return [c['mainsnak']['datavalue']['value'] for c in (preferred or claims) if 'datavalue' in c.get('mainsnak',{})]

def build():
    source=json.loads((ROOT/'data/processed/collected.json').read_text())
    snapshots=json.loads((ROOT/'data/raw/snapshots.json').read_text())
    entities=source['entities']; sg=schema(); g=graph()
    for role in [EX.DirectorRole,EX.ActorRole,EX.WriterRole]:
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
        typ={'person':DBO.Person,'genre':EX.Genre,'country':DBO.Country,'language':EX.Language}[kind]
        g.add((local,RDF.type,typ));g.add((local,RDFS.label,Literal(entity['labels']['en']['value'],lang='en')))
        add_link(local,'http://www.wikidata.org/entity/'+qid,'exact Wikidata QID from source claim')
        if entity.get('_snapshot_url'):
            g.add((local,EX.sourceSnapshot,snapshot_iris[entity['_snapshot_url']]))
        return local
    for film in source['films']:
        entity=entities[film['qid']];local=RES['film-'+film['qid']]
        title=entity.get('labels',{}).get('en',{}).get('value',film['wiki_title'])
        g.add((local,RDF.type,DBO.Film));g.add((local,EX.title,Literal(title)));g.add((local,RDFS.label,Literal(title,lang='en')))
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
        for prop,kind,pred in [('P136','genre',EX.hasGenre),('P495','country',EX.country),('P364','language',EX.language)]:
            for qid in claim_ids(entity,prop):
                target=add_entity(qid,kind)
                if target:g.add((local,pred,target))
        people={'director':[],'actor':[],'writer':[]}
        for prop,kind,pred,role in [('P57','director',DBO.director,EX.DirectorRole),('P161','actor',DBO.starring,EX.ActorRole),('P58','writer',DBO.writer,EX.WriterRole)]:
            for qid in claim_ids(entity,prop):
                target=add_entity(qid,'person')
                if not target:continue
                credit=RES['credit-'+film['qid']+'-'+qid+'-'+kind]
                for triple in [(local,pred,target),(local,EX.hasCredit,credit),(credit,RDF.type,EX.Credit),
                               (credit,EX.inFilm,local),(credit,EX.participant,target),(credit,EX.role,role),(credit,EX.sourceSnapshot,sn)]:g.add(triple)
                g.add((credit,RDFS.label,Literal(title+' — '+kind+' — '+entities[qid]['labels']['en']['value'])))
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
    stats={'films':len(records),'persons':len(set(g.subjects(RDF.type,DBO.Person))), 'credits':len(set(g.subjects(RDF.type,EX.Credit))),
           'genres':len(set(g.subjects(RDF.type,EX.Genre))),'countries':len(set(g.subjects(RDF.type,DBO.Country))),
           'languages':len(set(g.subjects(RDF.type,EX.Language))),'snapshots':len(snapshots),'data_triples':len(g),'schema_triples':len(sg),
           'classes':len(set(sg.subjects(RDF.type,OWL.Class))),
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
    body='<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(label)+' · MovieLOD</title><link rel="stylesheet" href="/style.css"><link rel="alternate" type="text/turtle" href="'+path+'/index.ttl"><script type="application/ld+json">'+ld+'</script></head><body class="resource-page"><main><a href="/">← MovieLOD</a><h1>'+html.escape(label)+'</h1><p class="iri">'+html.escape(str(s))+'</p><p><a href="'+path+'/index.ttl">Tải mô tả RDF (Turtle)</a></p><table><thead><tr><th>Quan hệ / thuộc tính</th><th>Đối tượng / giá trị</th></tr></thead><tbody>'+rows+'</tbody></table><footer>Dữ liệu nguồn: Wikidata, DBpedia. <a href="/LICENSE-DATA.txt">Giấy phép và ghi công</a>.</footer></main></body></html>'
    if extra:body=body.replace('<footer>',extra+'<footer>')
    (directory/'index.html').write_text(body,encoding='utf-8')

if __name__=='__main__':build()

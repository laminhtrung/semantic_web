"""Record real browser interactions plus actual command outputs, with Vietnamese narration.

Requires Playwright, Chrome/Chromium, FFmpeg and macOS voice Linh. Run the local server
on --port first. Evidence viewers are temporary localhost pages, not product features.
"""
import argparse,html,json,subprocess,time,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
from common import ROOT,EX,RES,DBO,write_json
from rdflib import Graph,RDF,RDFS,OWL

SCENES=[
 ('intro',15,'MovieLOD · dữ liệu điện ảnh liên kết','Đây là Movie L O D, ứng dụng dữ liệu phim liên kết. Nhóm sẽ minh họa năm yêu cầu bằng ontology, dữ liệu thật, R D F, liên kết bên ngoài và các truy vấn chạy trực tiếp.'),
 ('ontology',35,'YC1 · Ontology và mô hình Contribution','Ontology có bốn mươi hai lớp và dùng trực tiếp Film, Person, Country của DBpedia. Mô hình Contribution ghi một người giữ một vai trò trong một phim. Ba quan hệ contribution By, contribution To và has Role có ràng buộc đúng một giá trị. Bốn vai trò là đạo diễn, diễn viên, biên kịch và nhà sản xuất. Một người có thể giữ nhiều vai trò bằng các bản ghi riêng. Các lớp Actor và Filmmaker được phân loại từ định nghĩa thay vì nhập sẵn.'),
 ('sources',25,'YC2 · Phản hồi nguồn thật và SHA-256','Mã thu thập lấy Wikidata và DBpedia, xác định phim qua sitelink Wikipedia chính xác. Trên màn hình là metadata và một phản hồi nguồn thật, có địa chỉ, thời điểm và mã băm. Các phản hồi được giữ để kiểm tra và chạy lại. SHA hai trăm năm mươi sáu kiểm tra toàn vẹn nội dung, không tự chứng minh mọi phát biểu ngoài đời đều đúng.'),
 ('rdf',30,'YC3 · RDF, HTTP IRI và giấy phép mở','Dữ liệu được chuyển thành các bộ ba: chủ thể, quan hệ và đối tượng hoặc giá trị. Inception có đạo diễn Christopher Nolan, năm hai nghìn mười và thời lượng một trăm bốn mươi tám phút. Định danh H T T P mở được trang mô tả và bản R D F để tải. Dữ liệu có Turtle, JSON L D và giấy phép C C BY S A bốn chấm không. Phần công bố được đối chiếu với bản cục bộ trong biên bản kiểm tra.'),
 ('links',25,'YC4 · sameAs đến Wikidata và DBpedia','Inception nối tới Wikidata và DBpedia bằng owl same As. Hai định danh này cùng chỉ một thực thể. Tổng dataset có một nghìn bảy trăm hai mươi bảy liên kết; bảng theo phim có năm mươi tám dòng. Câu ASK trả True cho liên kết Wikidata. Quan hệ nguồn dữ liệu được ghi riêng và không thay thế same As.'),
 ('queries',40,'YC5 · Inception, phim Nolan và các vai trò','Truy vấn Inception trả năm phát hành, thời lượng và tên đạo diễn. Đổi câu hỏi sang phim do Nolan đạo diễn, chúng ta có tám dòng trong bộ dữ liệu. Truy vấn đóng góp Inception trả hai mươi lăm bản ghi, có các vai trò Actor, Director, Writer và Producer. Nolan xuất hiện ở những công việc khác nhau trong cùng phim. Các kết quả được S P A R Q L tính từ đồ thị. Người dùng có thể sửa câu hỏi rồi bấm Run query để chạy lại.'),
 ('extras',25,'YC5 · Công ty, giải thưởng và tải kết quả','Ứng dụng còn có câu hỏi về công ty sản xuất, giải thưởng và nguồn. Inception có bốn công ty trong dữ liệu. The Godfather có bảy giải được ghi nhận. Nút Download results tải kết quả đang hiển thị. Có thể dùng dữ liệu này để kiểm tra lại bằng một công cụ khác.'),
 ('endpoint',30,'YC5 · Kết quả thật từ endpoint và terminal','Đây là kết quả các lệnh đã chạy thật. P O S T tới endpoint trả J S O N có Inception và Christopher Nolan. Cùng câu hỏi chạy được bằng file S P A R Q L ở terminal. Khi gửi Accept text turtle tới định danh phim cục bộ, server trả chuyển hướng ba trăm linh ba; curl trừ L theo chuyển hướng và nhận mô tả R D F. Giao diện, endpoint và terminal dùng cùng dữ liệu khai báo.'),
 ('inference',40,'YC1 + YC5 · Kiểu gốc và kiểu được phân loại','Trên dữ liệu gốc, Nolan chỉ được khai báo là Person. Chạy cùng câu với reasoned, kết quả bổ sung Filmmaker và AwardWinner từ file phân loại. Contribution có DirectorRole được phân loại DirectingContribution; người có đóng góp đó được phân loại Filmmaker. Có mười hai ActionFilm trong mẫu. Mười hai lớp dùng luật O W L R L. Hai lớp có ngưỡng số lượng dùng truy vấn đếm I R I bổ sung; phần này chưa phải bằng chứng phân loại O W L D L đầy đủ.'),
 ('checks',25,'Đối chiếu minh chứng và bộ bài nộp','Bài có ontology, dữ liệu thật, R D F, liên kết và ba cách truy vấn. Các kiểm tra nguồn, truy vấn, test và bản công khai được lưu trong evidence để đối chiếu. Báo cáo, mười ba slide và video này cùng dùng mô hình hai chấm không. Bảng tự chấm ghi điểm theo minh chứng, không phải điểm chính thức của giảng viên.')
]

def command(args):
    result=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,check=True)
    return result.stdout

def proof(title,blocks):
    return '<!doctype html><meta charset="utf-8"><style>body{background:#f3f6f7;color:#152b3a;font:21px Arial,sans-serif;margin:0;padding:35px}h1{font-size:32px;color:#007f82;margin:0 0 24px}h2{font-size:23px}section{background:white;padding:20px 26px;border-radius:12px;margin:16px 0}pre{font:17px Menlo,monospace;white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.4;margin:8px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}.meta{color:#506776;font-size:17px}</style><h1>'+html.escape(title)+'</h1><p class="meta">Minh chứng đọc từ file / kết quả lệnh thực thi thật của MovieLOD 2.0</p>'+''.join('<section><h2>'+html.escape(name)+'</h2><pre>'+html.escape(text)+'</pre></section>' for name,text in blocks)

def prepare_proofs(out,port):
    g=Graph().parse(ROOT/'ontology/movie.ttl')
    contribution=list(g.predicate_objects(EX.Contribution))
    restrictions=[]
    for node in g.objects(EX.Contribution,RDFS.subClassOf):
        prop=g.value(node,OWL.onProperty)
        cardinality=g.value(node,OWL.qualifiedCardinality)
        if prop and cardinality is not None:
            filler=g.value(node,OWL.onClass)
            restrictions.append(str(prop).split('#')[-1]+' : exactly '+str(cardinality)+' '+str(filler).rsplit('/',1)[-1].split('#')[-1])
    assert len(restrictions)==3 and all('exactly 1' in value for value in restrictions)
    body=proof('YC1 · Ontology 2.0: lớp, quan hệ và ràng buộc',[
        ('42 lớp có tên · 3 lớp DBpedia dùng trực tiếp','dbo:Film     http://dbpedia.org/ontology/Film\ndbo:Person   http://dbpedia.org/ontology/Person\ndbo:Country  http://dbpedia.org/ontology/Country'),
        ('Contribution · các restriction đọc trực tiếp từ ontology/movie.ttl','\n'.join(restrictions)),
        ('Các vai trò có trong ontology','\n'.join(str(role).split('#')[-1] for role in g.subjects(RDF.type,EX.ContributionRole))),
        ('Định nghĩa Filmmaker','Person AND hasContribution SOME\n(DirectingContribution OR WritingContribution OR ProducingContribution)')])
    (out/'ontology.html').write_text(body)
    snapshots=json.loads((ROOT/'data/raw/snapshots.json').read_text());row=next(r for r in snapshots if 'titles=' in r['url'] and (ROOT/r['path']).exists())
    payload=json.loads((ROOT/row['path']).read_text());entity=payload['entities'].get('Q25188',next(iter(payload['entities'].values())))
    sample={'id':entity.get('id'),'labels':entity.get('labels'),'P57_director':entity.get('claims',{}).get('P57',[])[:1]}
    (out/'sources.html').write_text(proof('YC2 · metadata và phản hồi Wikidata thật',[('Metadata phản hồi',json.dumps(row,ensure_ascii=False,indent=2)),('Trích dữ liệu gốc (giữ nguyên các giá trị)',json.dumps(sample,ensure_ascii=False,indent=2))]))
    dataset=Graph().parse(ROOT/'data/processed/movies.ttl');sub=Graph()
    for triple in dataset.triples((RES['film-Q25188'],None,None)):
        if triple[1] in [RDF.type,EX.title,EX.releaseYear,EX.runtimeMinutes,DBO.director,OWL.sameAs]:sub.add(triple)
    (out/'rdf.html').write_text(proof('YC3 · trích RDF và giấy phép',[('Inception: triple thực tế',sub.serialize(format='turtle')),('LICENSE-DATA.txt',(ROOT/'LICENSE-DATA.txt').read_text())]))
    endpoint=command(['curl','-s','-X','POST',f'http://127.0.0.1:{port}/sparql','-H','Content-Type: application/sparql-query','--data-binary','@queries/02_inception.rq'])
    dereference=command(['curl','-s','-D','-','-o','/dev/null','-H','Accept: text/turtle',f'http://127.0.0.1:{port}/resource/film-Q25188'])
    terminal=command([str(ROOT/'.venv/bin/python'),'src/query.py','queries/02_inception.rq'])
    (out/'endpoint.html').write_text(proof('YC5 · endpoint và terminal: đầu vào / đầu ra thật',[
        ('POST /sparql · JSON nhận từ server',json.dumps(json.loads(endpoint),indent=2)),
        ('query.py queries/02_inception.rq',terminal),('Tra cứu RDF · header trả về',dereference)]))
    inferred=[]
    for flag in [[],['--reasoned']]:
        args=[str(ROOT/'.venv/bin/python'),'src/query.py','queries/24_nolan_asserted_types_only.rq']+flag
        data=json.loads(command(args));types=[binding['type']['value'] for binding in data['results']['bindings']]
        inferred.append(('query.py queries/24_nolan_asserted_types_only.rq '+' '.join(flag),'\n'.join(types)))
    action=json.loads(command([str(ROOT/'.venv/bin/python'),'src/query.py','queries/19_inferred_action_films.rq','--reasoned']))
    inferred.append(('query.py queries/19_inferred_action_films.rq --reasoned',str(len(action['results']['bindings']))+' phim ActionFilm\n'+'\n'.join(next(v['value'] for k,v in row.items() if k=='title') for row in action['results']['bindings'])))
    (out/'inference.html').write_text(proof('YC1 + YC5 · cùng truy vấn, kiểu gốc và kiểu phân loại',inferred))
    checks=[('src/validate.py',command([str(ROOT/'.venv/bin/python'),'src/validate.py'])),('pytest',(ROOT/'evidence/tests.txt').read_text()),('Đối chiếu bản công khai',(ROOT/'evidence/publication_checks.json').read_text())]
    # A compact extract of the complete evidence; the full output is retained in evidence.
    data=json.loads(checks[0][1]);checks[0]=(checks[0][0],json.dumps({k:v for k,v in data.items() if k!='source_hash_checks'},indent=2))
    publication=json.loads(checks[2][1]);checks[2]=(checks[2][0],json.dumps(publication.get('summary',publication),ensure_ascii=False,indent=2))
    (out/'checks.html').write_text(proof('Kiểm tra nguồn, ứng dụng và công bố',checks))

def record(port=8002,only_scene=None):
    out=ROOT/'docs/video_parts_v2';out.mkdir(exist_ok=True)
    proof_dir=ROOT/'evidence/demo';proof_dir.mkdir(exist_ok=True)
    prepare_proofs(proof_dir,port)
    base=f'http://127.0.0.1:{port}'
    chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    segments=[];records=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=str(chrome) if chrome.exists() else None)
        for index,(name,seconds,title,speech) in enumerate(SCENES,1):
            if only_scene and only_scene!=name:
                segment=out/f'{index:02d}.mp4'
                assert segment.exists(), 'Record the complete demo before replacing an individual scene.'
                segments.append(segment)
                records.append({'scene':name,'duration_seconds':seconds,'title':title,'speech':speech,'screenshot':str((proof_dir/f'{index:02d}_{name}.png').relative_to(ROOT))})
                continue
            if name=='checks':
                validation=json.loads((ROOT/'evidence/validation.json').read_text())
                publication=json.loads((ROOT/'evidence/publication_checks.json').read_text())
                assert publication['summary']['publication_complete'], 'Finish the public graph verification before recording the final evidence scene.'
                blocks=[('src/validate.py',json.dumps({k:v for k,v in validation.items() if k!='source_hash_checks'},indent=2)),('pytest',(ROOT/'evidence/tests.txt').read_text()),('Đối chiếu bản công khai',json.dumps(publication['summary'],ensure_ascii=False,indent=2))]
                (proof_dir/'checks.html').write_text(proof('Kiểm tra nguồn, ứng dụng và công bố',blocks))
            context=browser.new_context(viewport={'width':1440,'height':810},record_video_dir=str(out),record_video_size={'width':1440,'height':810},accept_downloads=True)
            page=context.new_page()
            started=time.monotonic()
            def go(path):
                page.goto(base+path,wait_until='networkidle')
                page.evaluate("([title])=>{const el=document.createElement('div');el.textContent=title;el.style='position:fixed;bottom:0;left:0;right:0;z-index:99999;padding:9px 24px;color:white;background:#007f82;font:bold 17px Arial';document.body.append(el)}",[title])
            def sample(file):
                option=next(i for i,q in enumerate(json.loads((ROOT/'web/dist/data/queries.json').read_text())) if q['file']==file)
                page.select_option('#sample',str(option));page.wait_for_function("!document.querySelector('#run').disabled")
            if name=='intro':
                go('/');page.wait_for_function("!document.querySelector('#run').disabled");page.mouse.move(320,360)
            elif name=='ontology':
                go('/demo-proof/ontology');page.wait_for_timeout(18000);page.mouse.wheel(0,420)
            elif name=='sources':
                go('/demo-proof/sources');page.wait_for_timeout(13000);page.mouse.wheel(0,390)
            elif name=='rdf':
                go('/resource/film-Q25188');page.wait_for_timeout(12000);go('/demo-proof/rdf');page.wait_for_timeout(10000);page.mouse.wheel(0,480)
            elif name=='links':
                go('/');page.wait_for_function("!document.querySelector('#run').disabled");sample('05_external_links.rq');page.wait_for_timeout(14000);sample('08_ask.rq')
            elif name=='queries':
                go('/');page.wait_for_function("!document.querySelector('#run').disabled");page.wait_for_timeout(10000);sample('03_nolan.rq');page.wait_for_timeout(13000);sample('04_credits.rq');page.wait_for_timeout(9000);page.locator('#results').evaluate('(el)=>el.scrollTop=600')
            elif name=='extras':
                go('/');page.wait_for_function("!document.querySelector('#run').disabled");sample('10_production_companies_of_a_film.rq');page.wait_for_timeout(10000);sample('11_awards_received_by_a_film.rq')
                with page.expect_download() as download:page.click('#export')
                download.value.save_as(proof_dir/'query_results_awards.json')
            elif name=='endpoint':
                go('/demo-proof/endpoint');page.wait_for_timeout(15000);page.mouse.wheel(0,500);page.wait_for_timeout(7000);page.mouse.wheel(0,500)
            elif name=='inference':
                go('/demo-proof/inference');page.wait_for_timeout(20000);page.mouse.wheel(0,450)
            elif name=='checks':
                go('/demo-proof/checks');page.wait_for_timeout(11000);page.mouse.wheel(0,450)
            remaining=seconds-(time.monotonic()-started)
            if remaining>0:page.wait_for_timeout(remaining*1000)
            screenshot=proof_dir/f'{index:02d}_{name}.png';page.screenshot(path=str(screenshot))
            video=page.video;context.close();raw=Path(video.path())
            txt=out/f'{index:02d}.txt';txt.write_text(speech)
            aiff=out/f'{index:02d}.aiff';subprocess.run(['say','-v','Linh','-r','180','-f',str(txt),'-o',str(aiff)],check=True)
            audio_seconds=float(command(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(aiff)]))
            rate=max(1,audio_seconds/(seconds-1));filters=[]
            while rate>2:filters.append('atempo=2');rate/=2
            filters.extend([f'atempo={rate:.6f}','apad'])
            segment=out/f'{index:02d}.mp4'
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(raw),'-i',str(aiff),'-t',str(seconds),'-vf','scale=1280:720,format=yuv420p','-af',','.join(filters),'-c:v','libx264','-preset','veryfast','-crf','21','-r','30','-c:a','aac','-b:a','128k',str(segment)],check=True)
            segments.append(segment);records.append({'scene':name,'duration_seconds':seconds,'title':title,'speech':speech,'screenshot':str(screenshot.relative_to(ROOT))})
            print('Recorded scene',index,'/',len(SCENES),name,flush=True)
        browser.close()
    concat=out/'concat.txt';concat.write_text(''.join("file '"+str(f)+"'\n" for f in segments))
    video_path=ROOT/'docs/Video_demo.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(video_path)],check=True)
    info=json.loads(command(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(video_path)]));duration=float(info['format']['duration'])
    assert 180<=duration<=300
    write_json(ROOT/'evidence/video.json',{'file':'docs/Video_demo.mp4','duration_seconds':duration,'width':1280,'height':720,'ontology_version':'2.0.0','narration':'Vietnamese synthetic voice Linh; not a recording of a student','capture':'Real Playwright browser interactions and localhost viewers of actual source files and command outputs; not a Protégé desktop recording','live_browser_recording':True,'scenes':records,'covers_requirements':['YC1','YC2','YC3','YC4','YC5'],'matches_current_dataset':True,'dataset_sha256':hashlib.sha256((ROOT/'data/processed/movies.ttl').read_bytes()).hexdigest()})
    print('Created demo video:',duration,'seconds',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8002);parser.add_argument('--only-scene',choices=[s[0] for s in SCENES]);args=parser.parse_args();record(args.port,args.only_scene)

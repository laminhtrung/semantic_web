import json
import shutil
from common import ROOT,write_json

labels={
 '02_inception.rq':'Inception: năm, thời lượng và đạo diễn',
 '01_films.rq':'Tất cả phim đã thu thập',
 '03_nolan.rq':'Các phim do Christopher Nolan đạo diễn',
 '04_credits.rq':'Ai làm việc gì trong Inception?',
 '05_external_links.rq':'Các phim liên kết tới đâu?',
 '06_genres.rq':'Thống kê phim theo thể loại',
 '07_source.rq':'Nguồn và mã băm của Inception',
 '08_ask.rq':'Inception có liên kết đúng với Wikidata không?'}
queries=[{'file':name,'label':label,'query':(ROOT/'queries'/name).read_text()} for name,label in labels.items()]
write_json(ROOT/'web/dist/data/queries.json',queries)
shutil.copy2(ROOT/'LICENSE-DATA.txt',ROOT/'web/dist/LICENSE-DATA.txt')
docs=ROOT/'web/dist/docs';docs.mkdir(exist_ok=True)
for name in ['Bao_cao.pdf','Huong_dan_A_Z.pdf','Huong_dan_thao_tac_chi_tiet.pdf','Slide.pdf']:
    if (ROOT/'docs'/name).exists():shutil.copy2(ROOT/'docs'/name,docs/name)
print('Web assets ready')

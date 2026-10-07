import json
import shutil
from common import ROOT,write_json

labels={
 '02_inception.rq':'Inception: year, runtime and director',
 '01_films.rq':'All films in the dataset',
 '03_nolan.rq':'Films directed by Christopher Nolan',
 '04_credits.rq':'Who contributed to Inception, and in which role?',
 '05_external_links.rq':'External links for each film',
 '06_genres.rq':'Film counts by genre',
 '07_source.rq':'Inception: source URLs and SHA-256 hashes',
 '08_ask.rq':'Is Inception linked to its Wikidata entity?'}
queries=[{'file':name,'label':label,'query':(ROOT/'queries'/name).read_text()} for name,label in labels.items()]
write_json(ROOT/'web/dist/data/queries.json',queries)
shutil.copy2(ROOT/'LICENSE-DATA.txt',ROOT/'web/dist/LICENSE-DATA.txt')
docs=ROOT/'web/dist/docs';docs.mkdir(exist_ok=True)
for name in ['Bao_cao.pdf','Huong_dan_A_Z.pdf','Huong_dan_thao_tac_chi_tiet.pdf','Slide.pdf']:
    if (ROOT/'docs'/name).exists():shutil.copy2(ROOT/'docs'/name,docs/name)
print('Web assets ready')

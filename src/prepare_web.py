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
 '08_ask.rq':'Is Inception linked to its Wikidata entity?',
 '09_actors_of_inception.rq':'Actors starring in Inception',
 '10_production_companies_of_a_film.rq':'Production companies of Inception',
 '11_awards_received_by_a_film.rq':'Awards received by The Godfather',
 '12_countries_and_languages_of_a_film.rq':'Country and language of Parasite',
 '15_feature_vs_animated_film_counts.rq':'Feature film vs. animated film counts',
 '16_documentary_film_count_ask.rq':'Does the dataset contain any documentary film?'}
# Group B/C queries (13,14,17-24) need the schema and/or the reasoner output, not just the
# published data graph, so they are not listed here — run them with:
#   python src/query.py queries/<file>.rq --reasoned
queries=[{'file':name,'label':label,'query':(ROOT/'queries'/name).read_text()} for name,label in labels.items()]
write_json(ROOT/'web/dist/data/queries.json',queries)
shutil.copy2(ROOT/'LICENSE-DATA.txt',ROOT/'web/dist/LICENSE-DATA.txt')
docs=ROOT/'web/dist/docs';docs.mkdir(exist_ok=True)
for name in ['Bao_cao.pdf','Huong_dan_A_Z.pdf','Huong_dan_thao_tac_chi_tiet.pdf','Slide.pdf']:
    if (ROOT/'docs'/name).exists():shutil.copy2(ROOT/'docs'/name,docs/name)
print('Web assets ready')

# MovieLOD — Ontology Redesign (v2.0.0)

All numbers in this document were produced by actually running the pipeline on the real 30-film
Wikidata/DBpedia crawl — none are hypothetical. Reproduce any of them with:

```bash
python src/collect.py        # crawl (now also pulls P162 producer, P166 award, P272 production company)
python src/build.py          # rebuild ontology/movie.ttl + data/processed/movies.ttl
python src/reason.py         # materialize inferred classes -> evidence/ontology_reasoning.json
python -m pytest -q          # 13 tests, including reasoner-backed assertions
```

## 0. What changed and why

The previous schema had grown three "combination" classes that didn't belong in a clean
hierarchy: `CreditedFilm` ("Film with a credit"), `DirectorWriter` ("Director and writer") and
`FilmContributor`. They were replaced with a proper hierarchy — `CreativeWork`, `Agent`,
`Contribution`, `Genre`, `Award`, `ProductionEntity` — and a **Contribution model** (`Person
--hasContribution--> Contribution --contributionTo--> Film`, `Contribution --hasRole-->
ContributionRole`) so a person can hold any number of roles without ever needing a hand-built
combination class. A query like "who is both a director and a writer" is now a two-line SPARQL
join (`queries/23_people_with_directing_and_writing_contribution.rq`), not a hard-coded class.

Two new real data fields were added to the crawl specifically to back `Award` and
`ProductionCompany` with real Wikidata claims instead of leaving them empty:
`wdt:P166` (award received, on both films and people) and `wdt:P272` (production company).
`wdt:P162` (producer) was also added to populate `ProducingContribution`/`ProducerRole`.
Nothing in this ontology is backed by fabricated data — every individual below is traceable to a
Wikidata claim ID recorded in `data/raw/`.

---

## TABLE 1 — Class hierarchy (42 named classes)

Legend: **E** = explicit (asserted directly in `build()` from a Wikidata claim), **I** = inferred
(only derivable via `owl:equivalentClass`, never asserted — see `tests/test_ontology.py::
test_defined_classes_are_inferred_not_asserted`).

| Class | Parent | E/I | OWL definition (informal) | Meaning |
|---|---|---|---|---|
| `ex:CreativeWork` | — | E (schema only) | top class | Any named work of authorship |
| `dbo:Film` | CreativeWork | E | — | A film (reused DBpedia class) |
| `ex:FeatureFilm` | Film | E | asserted when `wdt:P31`≠anime | Theatrically released narrative film |
| `ex:AnimatedFilm` | Film | E | asserted when `wdt:P31`=wd:Q20650540 | Animated film |
| `ex:DocumentaryFilm` | Film | E | asserted when genre=documentary | Non-fiction film (**0 instances**, see §9) |
| `ex:ActionFilm` | Film | I | Film ⊓ ∃hasGenre.ActionGenre | Film tagged with an action genre |
| `ex:ComedyFilm` | Film | I | Film ⊓ ∃hasGenre.ComedyGenre | Film tagged with a comedy genre |
| `ex:DramaFilm` | Film | I | Film ⊓ ∃hasGenre.DramaGenre | Film tagged with a drama genre |
| `ex:ScienceFictionFilm` | Film | I | Film ⊓ ∃hasGenre.ScienceFictionGenre | Film tagged with a sci-fi genre |
| `ex:MultiGenreFilm` | Film | I | Film ⊓ ≥2 hasGenre.Genre | Film tagged with ≥2 distinct genres |
| `ex:AwardWinningFilm` | Film | I | Film ⊓ ∃hasAward.Award | Film that received ≥1 award |
| `ex:Agent` | — | E (schema only) | top class | Anything able to contribute to a film |
| `dbo:Person` | Agent | E | — | A human (reused DBpedia class) |
| `ex:Actor` | Person | I | Person ⊓ ∃hasContribution.ActingContribution | Person who acted in ≥1 film |
| `ex:Filmmaker` | Person | I | Person ⊓ (∃hasContribution.DirectingContribution ⊔ WritingContribution ⊔ ProducingContribution) | Person who directed/wrote/produced ≥1 film |
| `ex:AwardWinner` | Person | I | Person ⊓ ∃hasAward.Award | Person who personally received ≥1 award |
| `ex:Organization` | Agent | E (schema only) | top class | A company able to produce films |
| `ex:ProductionCompany` | Organization | E | asserted from `wdt:P272` | Company credited with producing a film |
| `ex:FilmStudio` | ProductionCompany | I | ProductionCompany ⊓ ≥3 productionOf.Film | Company credited on ≥3 films here |
| `ex:Contribution` | — | E | exactly 1 contributionBy/contributionTo/hasRole | One person's role on one film |
| `ex:ActingContribution` | Contribution | I | Contribution ⊓ hasRole={ActorRole} | A contribution whose role is Actor |
| `ex:DirectingContribution` | Contribution | I | Contribution ⊓ hasRole={DirectorRole} | A contribution whose role is Director |
| `ex:WritingContribution` | Contribution | I | Contribution ⊓ hasRole={WriterRole} | A contribution whose role is Writer |
| `ex:ProducingContribution` | Contribution | I | Contribution ⊓ hasRole={ProducerRole} | A contribution whose role is Producer |
| `ex:ContributionRole` | — | E | — | Director/Actor/Writer/Producer (4 individuals) |
| `ex:Genre` | — | E | ≡ dbo:Genre | A film genre |
| `ex:FictionGenre` | Genre | E (schema only) | — | Genre denoting fiction |
| `ex:NonFictionGenre` | Genre | E (schema only) | — | Genre denoting non-fiction |
| `ex:ActionGenre` | FictionGenre | E | label contains "action" | — |
| `ex:ComedyGenre` | FictionGenre | E | label contains "comedy" | — |
| `ex:DramaGenre` | FictionGenre | E | label contains "drama" | — |
| `ex:ScienceFictionGenre` | FictionGenre | E | label contains "science fiction" | — |
| `ex:DocumentaryGenre` | NonFictionGenre | E | label contains "documentary" | **0 instances**, see §9 |
| `dbo:Country` | — | E | — | A country (reused DBpedia class) |
| `ex:Language` | — | E | ≡ dbo:Language | A language |
| `ex:Award` | — | E | — | A recognition (`wdt:P166`) |
| `ex:FilmAward` | Award | E | fallback category | Not acting/directing/writing-specific |
| `ex:ActingAward` | Award | E | label contains "actor"/"actress" | — |
| `ex:DirectingAward` | Award | E | label contains "director"/"directing" | — |
| `ex:WritingAward` | Award | E | label contains "screenplay"/"writing" | — |
| `ex:SourceSnapshot` | — | E | — | Provenance record (URL, hash, timestamp) |
| `ex:Dataset` | — | E | ≡ void:Dataset | The published dataset itself |

**Count check:** 42 named `owl:Class` individuals, verified by
`tests/test_ontology.py::test_generated_schema_matches_owl_exports` (`len(named) == 42`).

---

## TABLE 2 — Object properties (23)

| Property | Domain | Range | Inverse | Characteristics | Meaning |
|---|---|---|---|---|---|
| `ex:hasGenre` | Film | Genre | `genreOf` | — | Film has a genre |
| `ex:genreOf` | Genre | Film | `hasGenre` | — | inverse |
| `ex:country` | Film | Country | — | — | production country |
| `ex:language` | Film | Language | — | — | original language |
| `ex:sourceSnapshot` | — | SourceSnapshot | — | — | provenance link |
| `ex:hasContribution` | Person | Contribution | `contributionBy` | — | person holds a contribution record |
| `ex:contributionBy` | Contribution | Person | `hasContribution` | **Functional** | the one person on that record |
| `ex:contributionTo` | Contribution | Film | `contributionOf` | **Functional** | the one film on that record |
| `ex:contributionOf` | Film | Contribution | `contributionTo` | — | inverse |
| `ex:hasRole` | Contribution | ContributionRole | `roleOf` | **Functional** | the one role on that record |
| `ex:roleOf` | ContributionRole | Contribution | `hasRole` | — | inverse |
| `ex:hasProductionCompany` | Film | ProductionCompany | `productionOf` | — | `wdt:P272` |
| `ex:productionOf` | ProductionCompany | Film | `hasProductionCompany` | — | inverse |
| `ex:directed` | Person | Film | `dbo:director` | — | inverse of reused DBpedia property |
| `ex:actedIn` | Person | Film | `dbo:starring` | — | inverse of reused DBpedia property |
| `ex:wrote` | Person | Film | `dbo:writer` | — | inverse of reused DBpedia property |
| `ex:produced` | Person | Film | `dbo:producer` | — | inverse of reused DBpedia property |
| `dbo:director` | Film | Person | `ex:directed` | — | reused from DBpedia |
| `dbo:starring` | Film | Person | `ex:actedIn` | — | reused from DBpedia |
| `dbo:writer` | Film | Person | `ex:wrote` | — | reused from DBpedia |
| `dbo:producer` | Film | Person | `ex:produced` | — | reused from DBpedia |
| `ex:hasAward` | Film ⊔ Person | Award | `awardOf` | — | a film or a person can receive an award |
| `ex:awardOf` | Award | Film ⊔ Person | `hasAward` | — | inverse |

No property was given `Transitive`/`Symmetric` without a real logical reason, per the brief's
instruction — none of these relationships are transitive or symmetric in the real world (e.g.
`directed` is not transitive: "Nolan directed Inception" does not chain into anything else).
`sameAs`-style transitivity is already handled by `owl:sameAs` itself, not a custom property.

---

## TABLE 3 — Data properties (6, all backed by real crawled values)

| Property | Domain | Datatype | Cardinality | Real coverage |
|---|---|---|---|---|
| `ex:title` | Film | xsd:string | exactly 1 | 30/30 |
| `ex:releaseYear` | Film | xsd:integer | 0–1 | 30/30 |
| `ex:runtimeMinutes` | Film | xsd:decimal | 0–1 | 30/30 |
| `ex:sourceUrl` | SourceSnapshot | xsd:anyURI | exactly 1 | 76/76 |
| `ex:retrievedAt` | SourceSnapshot | xsd:dateTime | exactly 1 | 76/76 |
| `ex:sha256` | SourceSnapshot | xsd:string | exactly 1 | 76/76 |

**Considered but not modeled** (checked against the real crawl first, per the brief's instruction
not to fabricate data):

- `budget`, `revenue`, `voteCount`, `rating` — Wikidata does not reliably carry these for all 30
  films via the properties this crawler fetches; would need a different source (TMDB) to populate
  honestly. Not added.
- `countryName`, `languageName` as plain literals — **deliberately not added**: country and
  language are already modeled as linked entities (`dbo:Country`, `ex:Language`) with their own
  IRI and `rdfs:label`, which is strictly better 4-star/5-star practice than a bare string
  literal (it lets you dereference `/resource/country-Q30`, link it externally, etc.).

---

## TABLE 4 — Inferred classes (14), with real counts

All counts from `evidence/ontology_reasoning.json` (regenerate with `python src/reason.py`).
`asserted_counts` for every row below is **0** — none of these types ever appear directly in
`data/processed/movies.ttl`; they only exist after running a reasoner.

| Class | OWL restriction | Example individual (real) | Real count |
|---|---|---|---|
| `ex:ActingContribution` | `Contribution ⊓ hasValue(hasRole, ActorRole)` | `contribution-Q25188-Q2263-actor` (Leonardo DiCaprio in Inception) | 855 |
| `ex:DirectingContribution` | `Contribution ⊓ hasValue(hasRole, DirectorRole)` | `contribution-Q25188-Q25191-director` (Nolan directs Inception) | 31 |
| `ex:WritingContribution` | `Contribution ⊓ hasValue(hasRole, WriterRole)` | `contribution-Q25188-Q25191-writer` (Nolan writes Inception) | 51 |
| `ex:ProducingContribution` | `Contribution ⊓ hasValue(hasRole, ProducerRole)` | contributions with `hasRole=ProducerRole` | 73 |
| `ex:Actor` | `Person ⊓ ∃hasContribution.ActingContribution` | `person-Q2263` (Leonardo DiCaprio) | 769 |
| `ex:Filmmaker` | `Person ⊓ ∃hasContribution.(DirectingContribution ⊔ WritingContribution ⊔ ProducingContribution)` | `person-Q25191` (Christopher Nolan) | 89 |
| `ex:AwardWinner` | `Person ⊓ ∃hasAward.Award` | people with a real `wdt:P166` claim | 290 |
| `ex:ActionFilm` | `Film ⊓ ∃hasGenre.ActionGenre` | `film-Q25188` (Inception) | 12 |
| `ex:ComedyFilm` | `Film ⊓ ∃hasGenre.ComedyGenre` | `film-Q134773` (Forrest Gump) | 4 |
| `ex:DramaFilm` | `Film ⊓ ∃hasGenre.DramaGenre` | `film-Q47703` (The Godfather) | 25 |
| `ex:ScienceFictionFilm` | `Film ⊓ ∃hasGenre.ScienceFictionGenre` | `film-Q25188` (Inception) | 6 |
| `ex:MultiGenreFilm` | `Film ⊓ ≥2 hasGenre.Genre` | `film-Q103569` (Alien, 13 genres) | 30 (see §9) |
| `ex:AwardWinningFilm` | `Film ⊓ ∃hasAward.Award` | `film-Q47703` (The Godfather) | 26 |
| `ex:FilmStudio` | `ProductionCompany ⊓ ≥3 productionOf.Film` | `company-Q126399` (Warner Bros., 11 films) | 6 |

---

## TABLE 5 — Inference chains (2–3 hops, none asserted directly)

| # | Initial facts (asserted) | Rule 1 | Rule 2 | Final inference |
|---|---|---|---|---|
| 1 | `c rdf:type Contribution`, `c hasRole DirectorRole`, `c contributionBy nolan` | `owl:hasValue` ⟹ `c rdf:type DirectingContribution` | `owl:someValuesFrom`+`unionOf` ⟹ `nolan rdf:type Filmmaker` | **Nolan is a Filmmaker** (never asserted) |
| 2 | `c rdf:type Contribution`, `c hasRole ActorRole`, `c contributionBy dicaprio` | ⟹ `c rdf:type ActingContribution` | ⟹ `dicaprio rdf:type Actor` | **DiCaprio is an Actor** (never asserted) |
| 3 | `tarantino hasContribution c1` (role=Director), `tarantino hasContribution c2` (role=Writer) | both ⟹ `DirectingContribution`/`WritingContribution` | `unionOf` ⟹ `tarantino rdf:type Filmmaker` | Tarantino is a Filmmaker via **either** branch of the union |
| 4 | `genre-Q20656232 rdf:type ActionGenre, ScienceFictionGenre` (both asserted — label "science fiction action film" matches two keywords), `inception hasGenre genre-Q20656232` | `someValuesFrom(hasGenre,ActionGenre)` ⟹ `inception rdf:type ActionFilm` | `someValuesFrom(hasGenre,ScienceFictionGenre)` ⟹ `inception rdf:type ScienceFictionFilm` | **Inception is both an ActionFilm and a ScienceFictionFilm** from one genre triple |
| 5 | `warnerbros hasProductionCompany` ← asserted on 11 films | `owl:inverseOf` ⟹ `warnerbros productionOf film` ×11 | SPARQL `COUNT(DISTINCT ?f) >= 3` (outside OWL RL; see §9) ⟹ `warnerbros rdf:type FilmStudio` | **Warner Bros. is a FilmStudio**, derived from counting inverse links |
| 6 | `godfather hasAward award-Q102427` ("Academy Award for Best Picture") | label "Best Picture" matches no role keyword ⟹ `award-Q102427 rdf:type FilmAward` (build-time classification) | `someValuesFrom(hasAward,Award)` ⟹ `godfather rdf:type AwardWinningFilm` | **The Godfather is an AwardWinningFilm** |

---

## TABLE 6 — 24 SPARQL competency questions (all run for real)

Run Group A/B with `python src/query.py queries/<file>.rq`. Group C (and 13/14) need
`--reasoned` (loads the schema + `data/processed/inferred_classes.ttl`, generated by
`python src/reason.py`).

### Group A — direct data queries (no reasoning)

| # | File | Question | Real result |
|---|---|---|---|
| 1 | `01_films.rq` | All films | 30 rows |
| 2 | `02_inception.rq` | Inception: year/runtime/director | 1 row: 2010, 148 min, Nolan |
| 3 | `03_nolan.rq` | Films directed by Nolan | 8 rows |
| 4 | `04_credits.rq` | Who worked on Inception, what role | 25 rows |
| 5 | `05_external_links.rq` | External links per film | 58 rows |
| 6 | `06_genres.rq` | Film counts per genre | 75 rows |
| 7 | `07_source.rq` | Source + hash of Inception | 2 rows |
| 8 | `08_ask.rq` | Inception ↔ Wikidata link? | `true` |
| 9 | `09_actors_of_inception.rq` | Actors in Inception | 21 rows (Leonardo DiCaprio, Tom Hardy...) |
| 10 | `10_production_companies_of_a_film.rq` | Companies behind Inception | 4 rows |
| 11 | `11_awards_received_by_a_film.rq` | Awards received by The Godfather | 7 rows |
| 12 | `12_countries_and_languages_of_a_film.rq` | Country/language of Parasite | South Korea / Korean |

### Group B — hierarchy-based queries (schema needed, no reasoner materialization)

| # | File | Question | Real result |
|---|---|---|---|
| 13 | `13_fiction_genre_films_via_hierarchy.rq` | Films under FictionGenre (incl. subgenres) | 29/30 rows |
| 14 | `14_all_agents_people_and_organizations.rq` | All Person + Organization, via `rdfs:subClassOf*` | 851 people, 45 organizations |
| 15 | `15_feature_vs_animated_film_counts.rq` | FeatureFilm vs AnimatedFilm counts | 29 / 1 |
| 16 | `16_documentary_film_count_ask.rq` | Any DocumentaryFilm? | `false` (honest — see §9) |

### Group C — inference-dependent queries (require `--reasoned`)

| # | File | Question | Real result |
|---|---|---|---|
| 17 | `17_inferred_actors.rq` | Who is inferred to be an Actor? | 769 people (20 shown) |
| 18 | `18_inferred_filmmakers.rq` | Who is inferred to be a Filmmaker? | 89 people, incl. Nolan |
| 19 | `19_inferred_action_films.rq` | Which films are inferred ActionFilm? | 12 films |
| 20 | `20_inferred_multi_genre_films.rq` | Which films are inferred MultiGenreFilm? | 30 films (see §9) |
| 21 | `21_inferred_award_winning_films.rq` | Which films are inferred AwardWinningFilm? | 26 films |
| 22 | `22_inferred_film_studios.rq` | Which companies are inferred FilmStudio? | 6 companies |
| 23 | `23_people_with_directing_and_writing_contribution.rq` | Who has both a DirectingContribution and a WritingContribution? | 10 people, incl. Nolan, Tarantino, Coppola |
| 24 | `24_nolan_asserted_types_only.rq` | Nolan's *asserted* types only (no `--reasoned`) | **only `dbo:Person`** — contrast with Q18 |

---

## 11. Semantic Web vs. traditional database/Web — 5 contrastive questions

**Question 1 — "Who is an Actor?"**
- TRIPLE BAN ĐẦU: `dicaprio ex:hasContribution contribution-1`, `contribution-1 ex:hasRole ex:ActorRole`. No `dicaprio rdf:type ex:Actor` triple exists anywhere.
- ONTOLOGY RULE: `ex:Actor ≡ dbo:Person ⊓ ∃ex:hasContribution.ex:ActingContribution`.
- REASONING: OWL RL `hasValue` + `someValuesFrom` rules chain through `ActingContribution`.
- INFERRED KNOWLEDGE: `dicaprio rdf:type ex:Actor` (and 768 other people).
- SPARQL: `queries/17_inferred_actors.rq`.
- WHY: a traditional DB/web page would need an explicit `is_actor` column or a hand-written
  classification script; here the class membership is a logical *consequence* of the schema, so
  adding a new actor later (just a new Contribution triple) requires **zero** code change.

**Question 2 — "Is Christopher Nolan a filmmaker?"**
- TRIPLE BAN ĐẦU: `nolan rdf:type dbo:Person` is the *only* asserted type (see `queries/24_nolan_asserted_types_only.rq`, run without `--reasoned`).
- ONTOLOGY RULE: `ex:Filmmaker ≡ dbo:Person ⊓ (∃hasContribution.DirectingContribution ⊔ ... )`.
- REASONING: `c hasRole DirectorRole` → `c rdf:type DirectingContribution` → `nolan rdf:type Filmmaker`.
- INFERRED KNOWLEDGE: `nolan rdf:type ex:Filmmaker`.
- SPARQL: `queries/18_inferred_filmmakers.rq`.
- WHY: a traditional system answers "no" (or "unknown") to any query for an un-tagged field;
  a reasoner can derive "yes" purely from relational facts, with proof (the chain above).

**Question 3 — "Which films are MultiGenreFilm?"**
- TRIPLE BAN ĐẦU: `alien hasGenre g1`, `alien hasGenre g2`, ... (13 separate genre triples).
- ONTOLOGY RULE: `ex:MultiGenreFilm ≡ Film ⊓ ≥2 hasGenre.Genre`.
- REASONING: counting distinct fillers of a property — a genuinely OWL-DL-level entailment
  (outside OWL RL's rule coverage, see §9) but still a formally valid inference a full reasoner
  (HermiT/Pellet in Protégé) computes directly.
- INFERRED KNOWLEDGE: `alien rdf:type MultiGenreFilm` (and 29 other films).
- SPARQL: `queries/20_inferred_multi_genre_films.rq`.
- WHY: a traditional database would need an explicit `genre_count >= 2` computed column
  maintained by application code; in RDF/OWL, the *definition itself* is the computation.

**Question 4 — "Which production companies are film studios?"**
- TRIPLE BAN ĐẦU: 11 separate `inception hasProductionCompany warnerbros`-style triples across different films.
- ONTOLOGY RULE: `ex:FilmStudio ≡ ProductionCompany ⊓ ≥3 productionOf.Film`.
- REASONING: `owl:inverseOf` turns `hasProductionCompany` into `productionOf`, then cardinality ≥3 is checked.
- INFERRED KNOWLEDGE: `warnerbros rdf:type FilmStudio`.
- SPARQL: `queries/22_inferred_film_studios.rq`.
- WHY: no single film's page in a traditional movie website states "Warner Bros. is a major
  studio" as a fact — it's an aggregate property across the whole dataset that only a graph-wide
  query/reasoner can establish.

**Question 5 — "Does this individual belong to a class with no direct `rdf:type` triple for it?"**
- TRIPLE BAN ĐẦU: none of `person-Q25191`'s triples ever say `rdf:type ex:Filmmaker` or `rdf:type ex:AwardWinner`.
- ONTOLOGY RULE: both are `equivalentClass` definitions (Table 4).
- REASONING: `DeductiveClosure(OWLRL_Semantics)` materializes both.
- INFERRED KNOWLEDGE: `nolan rdf:type ex:Filmmaker`, `nolan rdf:type ex:AwardWinner`
  (`evidence/ontology_reasoning.json → nolan_inferred_classes`).
- SPARQL: compare `queries/24_nolan_asserted_types_only.rq` (returns 1 row) with
  `queries/18_inferred_filmmakers.rq` filtered to Nolan (present).
- WHY: this is the single clearest proof point for class: a plain SPARQL `SELECT` over a
  traditional triple store (no reasoner) **cannot** find Nolan via `?x a ex:Filmmaker` — the
  Semantic Web stack (ontology + reasoner) can, from the exact same base facts.

---

## TABLE 7 — Top 5 demo cases for class presentation

| # | Question | Initial data | Ontology rule | Inferred result | Why it matters |
|---|---|---|---|---|---|
| 1 | Is DiCaprio an Actor? | `hasContribution`+`hasRole=ActorRole` | `Actor ≡ Person ⊓ ∃hasContribution.ActingContribution` | 769 people typed `Actor`, 0 asserted | Simplest possible existential inference |
| 2 | Is Nolan a Filmmaker? | `hasRole=DirectorRole`/`WriterRole` | `Filmmaker ≡ Person ⊓ (∃...⊔∃...⊔∃...)` | Nolan typed `Filmmaker`, 0 asserted | Union-of-restrictions, 2-hop chain (Table 5 #1) |
| 3 | Which films are ActionFilm? | `hasGenre` → genre labelled "action" | `ActionFilm ≡ Film ⊓ ∃hasGenre.ActionGenre` | 12 films, incl. Inception & Alien (also ScienceFictionFilm — Table 5 #4) | Shows one asserted fact producing two different inferred types |
| 4 | Which films are MultiGenreFilm? | ≥2 `hasGenre` triples per film | `MultiGenreFilm ≡ Film ⊓ ≥2 hasGenre.Genre` | 30/30 films (see §9 honest caveat) | Demonstrates the OWL RL vs. full OWL DL cardinality boundary explicitly |
| 5 | Which companies are FilmStudio? | `hasProductionCompany` across films | `FilmStudio ≡ ProductionCompany ⊓ ≥3 productionOf.Film` | 6 companies (Warner Bros., Syncopy, Paramount, Legendary, New Line, 20th Century) | Combines `owl:inverseOf` + cardinality — a genuine 2-rule chain (Table 5 #5) |

---

## 9. Honest limitations (reported, not hidden)

1. **`DocumentaryFilm` / `DocumentaryGenre` have 0 instances.** The 30-film seed list
   (`config.json`) is all mainstream fiction features; no documentary was crawled. The classes
   are fully defined and ready — add a documentary title to `seed_titles` and rerun `collect.py`
   + `build.py` to populate them. Verified with `queries/16_documentary_film_count_ask.rq` → `false`.
2. **`MultiGenreFilm` happens to equal the full film population (30/30) in this sample** — the
   minimum genre count across all 30 films is 2 (Spirited Away, Titanic), so none fall below the
   threshold. The axiom is still correctly defined and correctly computed; this sample simply
   doesn't contain a contrasting single-genre film. Distribution: min 2, max 18 genres/film.
3. **OWL RL cannot materialize `minQualifiedCardinality` ≥ 2.** The W3C OWL 2 RL profile's rule
   set only covers qualified cardinality of 0 or 1 (`cls-maxqc1`/`cls-maxqc2`); `MultiGenreFilm`
   (≥2) and `FilmStudio` (≥3) are valid OWL DL entailments that a full reasoner (HermiT/Pellet in
   Protégé) computes directly, but `owlrl`'s `DeductiveClosure` silently skips them. `src/reason.py`
   documents this and supplies the same entailment via a direct SPARQL aggregate query instead
   (see `CARDINALITY_DEFINED` in that file).
4. **`owl:sameAs` inflates naive aggregate counts.** Every local individual is `owl:sameAs`-linked
   to its Wikidata (and sometimes DBpedia) IRI. Under full OWL RL substitution, every inferred
   fact about the local individual is also asserted about its external aliases — so counting
   query *subjects* without restricting to the local `res:` namespace overcounts. This was caught
   empirically (`FilmStudio` first computed as 44 instead of the real 6) and fixed by filtering
   both the typed subject and the counted object to `res:` IRIs in `src/reason.py`.
5. **Budget/revenue/rating/vote-count are not modeled** — not reliably available from the three
   Wikidata properties this crawler fetches; adding them without a real source would mean
   fabricated data, which this project avoids (see Table 3).

---

## 12. FINAL ONTOLOGY — recommended presentation subset

The full deployed ontology has 42 classes / 23 object properties / 6 data properties / 14
inferred classes / 6+ inference chains / 24 competency questions (all above). For a focused class
presentation, the following ~13-class, ~16-property, 8-inferred-class subset tells the whole
story without the long tail of genre/award sub-categories:

**Core classes (13):** `CreativeWork`, `Film`, `Agent`, `Person`, `Organization`,
`ProductionCompany`, `Contribution`, `ContributionRole`, `Genre`, `Award`, `Actor`, `Filmmaker`,
`FilmStudio`.

**Core properties (16):** `hasGenre`/`genreOf`, `hasContribution`/`contributionBy`,
`contributionTo`/`contributionOf`, `hasRole`/`roleOf`, `hasProductionCompany`/`productionOf`,
`hasAward`/`awardOf`, `directed`/`dbo:director`, `title`, `releaseYear`.

**Inferred classes (8):** `Actor`, `Filmmaker`, `AwardWinner`, `ActingContribution`,
`DirectingContribution`, `ActionFilm`, `MultiGenreFilm`, `FilmStudio`.

**Inference chains (5):** Table 5, rows 1, 2, 4, 5, 6.

**Competency questions (20+):** Table 6, all 24 rows.

This subset is what `ontology/Movie_Ontology.owl` looks like when opened in Protégé — load it
alongside `data/processed/movies.ttl` (or the combined `ontology/Movie_Knowledge_Graph.owl`) and
run the HermiT or Pellet reasoner to see every `I`-marked class in Table 1 populate live,
including `MultiGenreFilm`/`FilmStudio`, which `owlrl` cannot materialize (§9, point 3) but a full
DL reasoner can.

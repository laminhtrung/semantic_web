---
title: "MovieLOD: ontology 2.0 đầy đủ bằng tiếng Việt"
date: "MovieLOD 2.0 · Đối chiếu 08/10/2026"
---

## 1. Mô hình hiện tại và cách đọc

Tài liệu này trình bày đầy đủ **42 lớp**, **23 object property**, **6 datatype property**, **14 lớp phân loại** và **24 truy vấn** của ontology 2.0. Tên kỹ thuật giữ nguyên để đối chiếu mã nguồn; giải thích bằng tiếng Việt. Các bảng sinh từ `ontology/movie.ttl` và biên bản đã kiểm tra ngày 08/10/2026.

`dbo:` là từ vựng DBpedia; `ex:` là namespace ontology của bài. “Lớp có tên” nghĩa là IRI được khai báo owl:Class trong lược đồ. Có các lớp nền chỉ mô tả cây lớp, không gán trực tiếp cho cá thể. “Phân loại” nghĩa là kiểu không có sẵn trong graph khai báo và được bổ sung ở file inferred_classes.ttl.

Bản cũ dùng Credit/participant/hasCredit/DirectorWriter. Bản 2.0 dùng Contribution/contributionBy/contributionTo/hasRole và thêm Producer, Award, ProductionCompany. **Website công khai đã được đồng bộ và kiểm tra graph bản 2.0.**

## 2. Toàn bộ lớp và cây cha

| Lớp | Lớp cha được khai báo | Cách có kiểu | Ý nghĩa |
|:--|:--|:--|:--|
| `dbo:Country` | — | Nền / khai báo | Quốc gia; dùng lớp DBpedia |
| `dbo:Film` | ex:CreativeWork | Nền / khai báo | Phim; dùng lớp DBpedia |
| `dbo:Person` | ex:Agent | Nền / khai báo | Người; dùng lớp DBpedia |
| `ex:ActingAward` | ex:Award | Nền / khai báo | Giải có nhãn actor/actress |
| `ex:ActingContribution` | ex:Contribution | OWL RL | Đóng góp diễn xuất |
| `ex:ActionFilm` | dbo:Film | OWL RL | Phim có thể loại ActionGenre |
| `ex:ActionGenre` | ex:FictionGenre | Nền / khai báo | Nhãn thể loại chứa action |
| `ex:Actor` | dbo:Person | OWL RL | Người có đóng góp diễn xuất |
| `ex:Agent` | — | Nền / khai báo | Chủ thể có thể đóng góp |
| `ex:AnimatedFilm` | dbo:Film | Nền / khai báo | Phim hoạt hình theo P31 |
| `ex:Award` | — | Nền / khai báo | Thực thể giải thưởng, không phải một lần trao |
| `ex:AwardWinner` | dbo:Person | OWL RL | Người có giải thưởng riêng |
| `ex:AwardWinningFilm` | dbo:Film | OWL RL | Phim có liên kết tới giải thưởng |
| `ex:ComedyFilm` | dbo:Film | OWL RL | Phim có thể loại ComedyGenre |
| `ex:ComedyGenre` | ex:FictionGenre | Nền / khai báo | Nhãn thể loại chứa comedy |
| `ex:Contribution` | — | Nền / khai báo | Một người giữ một vai trò trong một phim |
| `ex:ContributionRole` | — | Nền / khai báo | Loại vai trò; có 4 cá thể vai trò |
| `ex:CreativeWork` | — | Nền / khai báo | Tác phẩm sáng tạo |
| `ex:Dataset` | — | Nền / khai báo | Bộ dữ liệu công bố |
| `ex:DirectingAward` | ex:Award | Nền / khai báo | Giải có nhãn director/directing |
| `ex:DirectingContribution` | ex:Contribution | OWL RL | Đóng góp đạo diễn |
| `ex:DocumentaryFilm` | dbo:Film | Nền / khai báo | Phim có thể loại tài liệu; mẫu hiện không có |
| `ex:DocumentaryGenre` | ex:NonFictionGenre | Nền / khai báo | Nhãn thể loại chứa documentary |
| `ex:DramaFilm` | dbo:Film | OWL RL | Phim có thể loại DramaGenre |
| `ex:DramaGenre` | ex:FictionGenre | Nền / khai báo | Nhãn thể loại chứa drama |
| `ex:FeatureFilm` | dbo:Film | Nền / khai báo | Nhóm phim dài theo cách ánh xạ P31 của bài |
| `ex:FictionGenre` | ex:Genre | Nền / khai báo | Nhóm thể loại hư cấu |
| `ex:FilmAward` | ex:Award | Nền / khai báo | Nhóm giải mặc định khi chưa khớp nhóm nghề nghiệp |
| `ex:FilmStudio` | ex:ProductionCompany | Đếm IRI | Công ty có ít nhất 3 IRI phim trong mẫu; quy tắc bài |
| `ex:Filmmaker` | dbo:Person | OWL RL | Người có đóng góp đạo diễn, biên kịch hoặc sản xuất |
| `ex:Genre` | — | Nền / khai báo | Thể loại |
| `ex:Language` | — | Nền / khai báo | Ngôn ngữ |
| `ex:MultiGenreFilm` | dbo:Film | Đếm IRI | Phim có từ 2 IRI thể loại; quy tắc đếm bổ sung |
| `ex:NonFictionGenre` | ex:Genre | Nền / khai báo | Nhóm thể loại phi hư cấu |
| `ex:Organization` | ex:Agent | Nền / khai báo | Tổ chức |
| `ex:ProducingContribution` | ex:Contribution | OWL RL | Đóng góp nhà sản xuất |
| `ex:ProductionCompany` | ex:Organization | Nền / khai báo | Công ty sản xuất lấy từ P272 |
| `ex:ScienceFictionFilm` | dbo:Film | OWL RL | Phim có thể loại ScienceFictionGenre |
| `ex:ScienceFictionGenre` | ex:FictionGenre | Nền / khai báo | Nhãn thể loại chứa science fiction |
| `ex:SourceSnapshot` | — | Nền / khai báo | Metadata của phản hồi nguồn |
| `ex:WritingAward` | ex:Award | Nền / khai báo | Giải có nhãn screenplay/writing |
| `ex:WritingContribution` | ex:Contribution | OWL RL | Đóng góp biên kịch |

## 3. Các quan hệ đối tượng

Quan hệ đối tượng nối **hai thực thể**; inverse là đường đi ngược. Functional nghĩa là nhiều nhất một đối tượng trong ngữ nghĩa OWL; không tự thay thế kiểm tra số trường trong file. Domain/range hỗ trợ suy ra kiểu, không phải cơ chế từ chối nhập liệu.

| Quan hệ | Domain | Range | Inverse / đặc tính |
|:--|:--|:--|:--|
| `dbo:director` | dbo:Film | dbo:Person | ex:directed |
| `dbo:producer` | dbo:Film | dbo:Person | ex:produced |
| `dbo:starring` | dbo:Film | dbo:Person | ex:actedIn |
| `dbo:writer` | dbo:Film | dbo:Person | ex:wrote |
| `ex:actedIn` | dbo:Person | dbo:Film | — |
| `ex:awardOf` | ex:Award | (dbo:Film HOẶC dbo:Person) | ex:hasAward |
| `ex:contributionBy` | ex:Contribution | dbo:Person | ex:hasContribution, functional |
| `ex:contributionOf` | dbo:Film | ex:Contribution | ex:contributionTo |
| `ex:contributionTo` | ex:Contribution | dbo:Film | functional |
| `ex:country` | dbo:Film | dbo:Country | — |
| `ex:directed` | dbo:Person | dbo:Film | — |
| `ex:genreOf` | ex:Genre | dbo:Film | ex:hasGenre |
| `ex:hasAward` | (dbo:Film HOẶC dbo:Person) | ex:Award | — |
| `ex:hasContribution` | dbo:Person | ex:Contribution | — |
| `ex:hasGenre` | dbo:Film | ex:Genre | — |
| `ex:hasProductionCompany` | dbo:Film | ex:ProductionCompany | — |
| `ex:hasRole` | ex:Contribution | ex:ContributionRole | functional |
| `ex:language` | dbo:Film | ex:Language | — |
| `ex:produced` | dbo:Person | dbo:Film | — |
| `ex:productionOf` | ex:ProductionCompany | dbo:Film | ex:hasProductionCompany |
| `ex:roleOf` | ex:ContributionRole | ex:Contribution | ex:hasRole |
| `ex:sourceSnapshot` | — | ex:SourceSnapshot | — |
| `ex:wrote` | dbo:Person | dbo:Film | — |

**Luồng chính:** Person → hasContribution → Contribution → contributionTo → Film. Contribution → hasRole → Role; contributionBy đi ngược đến Person. Film → hasProductionCompany → Company; Film/Person → hasAward → Award. `dbo:director`, `dbo:writer`, `dbo:starring`, `dbo:producer` là các quan hệ trực tiếp bổ sung để truy vấn thuận tiện.

## 4. Thuộc tính giá trị

Thuộc tính giá trị nối một thực thể với chuỗi, số hoặc thời điểm. Metadata nguồn còn có thuộc tính từ Dublin Core/PROV hoặc từ vựng RDF khác, không tính vào 6 datatype property tự khai báo dưới đây.

| Thuộc tính | Domain | Datatype |
|:--|:--|:--|
| `ex:releaseYear` | dbo:Film | xsd:integer |
| `ex:retrievedAt` | ex:SourceSnapshot | xsd:dateTime |
| `ex:runtimeMinutes` | dbo:Film | xsd:decimal |
| `ex:sha256` | ex:SourceSnapshot | xsd:string |
| `ex:sourceUrl` | ex:SourceSnapshot | xsd:anyURI |
| `ex:title` | dbo:Film | xsd:string |

## 5. Định nghĩa và số liệu 14 lớp phân loại

Các lớp sau có **0 cá thể gán sẵn** trong graph khai báo. Số bên dưới lấy từ `ontology_reasoning.json`, đếm tài nguyên nội bộ, loại alias sameAs. Các truy vấn Actor/Filmmaker có LIMIT 20 nên bảng hiển thị chỉ 20 dòng.

| Lớp | Định nghĩa đọc bằng lời | Số cá thể | Phương pháp |
|:--|:--|--:|:--|
| `ActingContribution` | (ex:Contribution VÀ ex:hasRole có giá trị ex:ActorRole) | 855 | OWL RL |
| `DirectingContribution` | (ex:Contribution VÀ ex:hasRole có giá trị ex:DirectorRole) | 31 | OWL RL |
| `WritingContribution` | (ex:Contribution VÀ ex:hasRole có giá trị ex:WriterRole) | 51 | OWL RL |
| `ProducingContribution` | (ex:Contribution VÀ ex:hasRole có giá trị ex:ProducerRole) | 73 | OWL RL |
| `Actor` | (dbo:Person VÀ ex:hasContribution tồn tại ex:ActingContribution) | 769 | OWL RL |
| `Filmmaker` | (dbo:Person VÀ (ex:hasContribution tồn tại ex:DirectingContribution HOẶC ex:hasContribution tồn tại ex:WritingContribution HOẶC ex:hasContribution tồn tại ex:ProducingContribution)) | 89 | OWL RL |
| `AwardWinner` | (dbo:Person VÀ ex:hasAward tồn tại ex:Award) | 290 | OWL RL |
| `ActionFilm` | (dbo:Film VÀ ex:hasGenre tồn tại ex:ActionGenre) | 12 | OWL RL |
| `ComedyFilm` | (dbo:Film VÀ ex:hasGenre tồn tại ex:ComedyGenre) | 4 | OWL RL |
| `DramaFilm` | (dbo:Film VÀ ex:hasGenre tồn tại ex:DramaGenre) | 25 | OWL RL |
| `ScienceFictionFilm` | (dbo:Film VÀ ex:hasGenre tồn tại ex:ScienceFictionGenre) | 6 | OWL RL |
| `AwardWinningFilm` | (dbo:Film VÀ ex:hasAward tồn tại ex:Award) | 26 | OWL RL |
| `MultiGenreFilm` | (dbo:Film VÀ ex:hasGenre ít nhất 2 (ex:Genre)) | 30 | SPARQL đếm IRI |
| `FilmStudio` | (ex:ProductionCompany VÀ ex:productionOf ít nhất 3 (dbo:Film)) | 6 | SPARQL đếm IRI |

**Giới hạn cần nói đúng:** `MultiGenreFilm` và `FilmStudio` được `src/reason.py` thêm kiểu bằng COUNT DISTINCT sau khi chạy OWL RL. Ngưỡng 2/3 không được owlrl xử lý như yêu cầu của bài. Đếm IRI khác nhau là quy tắc ứng dụng; dưới ngữ nghĩa OWL, hai tên khác nhau có thể cùng chỉ một cá thể. Muốn khẳng định cardinality theo OWL DL cần căn cứ phân biệt cá thể hoặc kết quả reasoner phù hợp. Đã chạy HermiT và Pellet: ontology nhất quán, 12 lớp đầu có số lượng khớp OWL RL; hai lớp cardinality có 0 cá thể được suy luận DL, còn số 30/6 là quy tắc ứng dụng. Không nói “HermiT chắc chắn suy ra cả hai lớp” chỉ dựa vào số IRI.

## 6. Chuỗi minh họa để bảo vệ

1. Nolan có Contribution với DirectorRole → định nghĩa hasValue phân loại DirectingContribution → Person có đóng góp đó được phân loại Filmmaker.
2. DiCaprio có Contribution với ActorRole → ActingContribution → Actor.
3. Inception liên kết tới genre được ánh xạ ActionGenre → ActionFilm. Nếu genre còn thuộc ScienceFictionGenre thì phim có thể thuộc hai nhóm.
4. Phim có hasAward tới Award → AwardWinningFilm; giải của người được xử lý riêng qua AwardWinner.
5. hasProductionCompany có inverse productionOf; ứng dụng đếm từ 3 IRI phim trở lên để gán FilmStudio. Tên lớp này là định nghĩa của bài, không kết luận công ty là studio lớn ngoài đời.

Các thể loại/giải được ánh xạ nhóm bằng từ khóa nhãn trong build.py; đây là bước quy tắc chuyển đổi dữ liệu, không phải suy luận tự khám phá nghĩa từ ngôn ngữ tự nhiên.

## 7. 24 câu hỏi SPARQL và kết quả kiểm tra

“Gốc” chỉ nạp movies.ttl. “Có phân loại” nạp movies.ttl + ontology/movie.ttl + inferred_classes.ttl. Với câu 14/15, 1 dòng là **một dòng thống kê**, không phải chỉ có một thực thể. Câu 24 dùng không --reasoned để xem kiểu gán gốc; chạy --reasoned trả thêm kiểu.

| File | Gốc | Có phân loại | Ý nghĩa |
|:--|:--|:--|:--|
| `01_films.rq` | 30 | 30 | Danh sách 30 phim |
| `02_inception.rq` | 1 | 1 | Inception: năm, thời lượng, đạo diễn |
| `03_nolan.rq` | 8 | 8 | 8 phim Nolan trong mẫu |
| `04_credits.rq` | 25 | 25 | Đóng góp Inception (25 bản ghi) |
| `05_external_links.rq` | 58 | 58 | Liên kết ngoài theo phim |
| `06_genres.rq` | 75 | 75 | Đếm phim theo thể loại |
| `07_source.rq` | 2 | 2 | Nguồn và hash Inception |
| `08_ask.rq` | true | true | Có liên kết Wikidata Inception? |
| `09_actors_of_inception.rq` | 21 | 21 | 21 diễn viên Inception |
| `10_production_companies_of_a_film.rq` | 4 | 4 | 4 công ty Inception |
| `11_awards_received_by_a_film.rq` | 7 | 7 | 7 giải The Godfather |
| `12_countries_and_languages_of_a_film.rq` | 1 | 1 | Quốc gia/ngôn ngữ Parasite |
| `13_fiction_genre_films_via_hierarchy.rq` | 0 | 29 | Phim qua hierarchy FictionGenre |
| `14_all_agents_people_and_organizations.rq` | 1 | 1 | Thống kê Person/Organization qua hierarchy |
| `15_feature_vs_animated_film_counts.rq` | 1 | 1 | Thống kê FeatureFilm/AnimatedFilm |
| `16_documentary_film_count_ask.rq` | false | false | Có DocumentaryFilm trong mẫu? |
| `17_inferred_actors.rq` | 0 | 20 | Actor được phân loại (LIMIT 20) |
| `18_inferred_filmmakers.rq` | 0 | 20 | Filmmaker được phân loại (LIMIT 20) |
| `19_inferred_action_films.rq` | 0 | 12 | 12 ActionFilm |
| `20_inferred_multi_genre_films.rq` | 0 | 30 | 30 MultiGenreFilm |
| `21_inferred_award_winning_films.rq` | 0 | 26 | 26 AwardWinningFilm |
| `22_inferred_film_studios.rq` | 0 | 6 | 6 FilmStudio theo quy tắc bài |
| `23_people_with_directing_and_writing_contribution.rq` | 0 | 10 | 10 người có đóng góp đạo diễn và biên kịch |
| `24_nolan_asserted_types_only.rq` | 1 | 3 | Kiểu Nolan gốc hoặc đã bổ sung tùy chế độ |

Nhóm trực tiếp: 01–12, 15–16; có schema: 13–14; cần file phân loại: 17–23; đối chiếu kiểu khai báo: 24. Giao diện có 14 mẫu trực tiếp. Terminal hỗ trợ --reasoned cho các nhóm còn lại.

## 8. Semantic Web đóng góp gì?

RDF cung cấp IRI dùng chung để mô tả và nối thực thể qua nhiều nguồn. OWL mô tả lớp/quan hệ dưới dạng máy xử lý được; bộ luật có thể bổ sung kiểu từ các quan hệ thay vì lưu sẵn nhãn nghề nghiệp. SPARQL hỏi cùng mô hình đồ thị, kể cả đường đi qua hierarchy khi schema được nạp.

CSDL quan hệ vẫn có thể trả các câu hỏi bằng JOIN, view, truy vấn đệ quy hoặc quy tắc ứng dụng. Không dùng “SQL không làm được” làm lập luận. Giá trị chính ở đây là chia sẻ định danh/từ vựng, liên kết dataset, nguồn truy lại được và định nghĩa ngữ nghĩa tường minh.

## 9. Giới hạn và tái lập

DocumentaryFilm/DocumentaryGenre có 0 cá thể; ASK false chỉ nói về dataset. MultiGenreFilm hiện bằng 30/30 do mẫu đều có nhiều thể loại. Việc phân loại FeatureFilm theo quy tắc P31 là giản lược; chưa chứng minh mọi phim phát hành rạp đều phù hợp định nghĩa học thuật. Không có ngân sách/doanh thu/streaming.

Đã bổ sung đủ 76 phản hồi gốc, kiểm tra toàn bộ hash và chạy lại collect/build/validate/reason. Có 14 test pass. Không phát hiện lỗi owlrl không đồng nghĩa ontology OWL DL đã được chứng minh nhất quán.

```bash
.venv/bin/python src/build.py
.venv/bin/python src/prepare_web.py
.venv/bin/python src/reason.py
.venv/bin/python src/query.py queries/18_inferred_filmmakers.rq --reasoned
.venv/bin/python -m pytest -q
```

Muốn lấy lại nguồn: dùng sao lưu đúng snapshot; nếu chạy collect.py/--refresh để tải mới, giữ mốc URL/hash/time mới và build, kiểm tra lại toàn bộ; không ghi đè lịch sử để giả vờ hash cũ đã khớp.

Nguồn: [OWL 2 Profiles](https://www.w3.org/TR/owl2-profiles/), [OWL 2 Primer](https://www.w3.org/TR/owl2-primer/), [SPARQL 1.1](https://www.w3.org/TR/sparql11-query/). Các số liệu và kết quả truy vấn lấy từ repository.

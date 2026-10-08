---
title: "MovieLOD: báo cáo học phần Semantic Web"
date: "MovieLOD 2.0 · Đối chiếu ngày 08/10/2026"
---

## 1. Mục tiêu và đối chiếu đề

MovieLOD là ứng dụng dữ liệu mở có liên kết về điện ảnh. Ví dụ xuyên suốt: phim **Inception**, đạo diễn **Christopher Nolan**, nguồn dữ liệu và các định danh bên ngoài. Giao diện ứng dụng dùng tiếng Anh; tài liệu giải thích bằng tiếng Việt. Bộ nộp gồm báo cáo này (không quá 15 trang), **24 slide** và kịch bản quay demo **4 phút 50 giây**. `Video_demo.mp4` được thay bằng video ghi thao tác trình duyệt và kết quả lệnh thật trên bản 2.0, lời đọc tiếng Việt tổng hợp.

| Yêu cầu đề gốc | Triển khai | Minh chứng |
|:--|:--|:--|
| YC1: Define an ontology | 42 lớp, quan hệ, ràng buộc và định nghĩa lớp | `ontology/movie.ttl`, hai file OWL, `src/build.py` |
| YC2: Collect relevant data | Wikidata/DBpedia, danh tính chính xác, URL và metadata nguồn | `src/collect.py`, `data/raw/`, `collection.json` |
| YC3: Transform to 4* | RDF, HTTP IRI, Turtle/JSON-LD, giấy phép, trang mô tả | `data/processed/`, `LICENSE-DATA.txt` |
| YC4: Establish links for 5* | 1.727 liên kết owl:sameAs | `link_audit.json`, truy vấn 05 |
| YC5: SPARQL endpoint/terminal | Web, Flask/RDFLib, terminal | `src/server.py`, `src/query.py`, 24 truy vấn |

**Trạng thái:** Bản 2.0 đã được xuất bản công khai và kiểm tra không đăng nhập: dữ liệu Turtle/JSON-LD, ontology và mô tả RDF của Inception đều đẳng cấu với graph cục bộ. Có 19.339 triple dữ liệu và 42 lớp ontology. Đã bổ sung 43 phản hồi còn thiếu và chạy lại quy trình: đủ 76/76 file nguồn, 76/76 SHA-256 khớp, không có file thiếu. Một phản hồi tải lại có nội dung thay đổi được ghi thời điểm/hash mới; danh mục lịch sử được giữ ở `evidence/source_manifest_before_recovery.json`.

## 2. Kiến trúc và quy trình

Chọn phim trong `config.json`, lấy phản hồi bằng `collect.py`, tạo mô hình và RDF bằng `build.py`, kiểm tra dữ liệu bằng Python, phân loại bằng `reason.py`, sau đó truy vấn và công bố. Phản hồi gốc lưu ở `data/raw/`; dữ liệu chuẩn hóa ở `data/processed/`; các số liệu và biên bản ở `evidence/`.

Dữ liệu khai báo nằm trong `movies.ttl`. Lược đồ nằm trong `ontology/movie.ttl`. Kiểu phân loại bổ sung nằm riêng trong `inferred_classes.ttl`. Endpoint mặc định chỉ truy vấn graph khai báo. Terminal với `--reasoned` nạp cả ba file; không tự chạy reasoner mỗi lần gọi.

\newpage

## 3. YC1 — Ontology và mô hình đóng góp

**42 lớp có tên:** dùng trực tiếp `dbo:Film`, `dbo:Person`, `dbo:Country`; 39 lớp khác thuộc namespace của bài. Có **23 object property**, **6 datatype property** và **14 lớp phân loại bổ sung**. Các lớp bên ngoài được tham chiếu qua equivalentClass không được cộng vào số lớp khai báo này.

| Nhánh | Ý nghĩa và ví dụ |
|:--|:--|
| CreativeWork / Film | Tác phẩm, phim, FeatureFilm, AnimatedFilm và các nhóm theo thể loại |
| Agent / Person / Organization | Người và tổ chức; ProductionCompany là công ty sản xuất |
| Contribution | Một người giữ một vai trò trong một phim |
| Genre / Award | Thể loại và giải thưởng, có các nhóm con |
| Country / Language / SourceSnapshot / Dataset | Quốc gia, ngôn ngữ, bản ghi nguồn và bộ dữ liệu |

**Contribution:** `contributionBy` trỏ một Person; `contributionTo` trỏ một Film; `hasRole` trỏ một ContributionRole. Bốn vai trò là Director, Actor, Writer và Producer. Nolan có thể có nhiều đóng góp riêng; không dùng lớp DirectorWriter của phiên bản cũ. `hasContribution` và `contributionOf` là các đường đi ngược.

Các quan hệ có domain/range và inverse; ba thuộc tính của Contribution là functional, có ràng buộc đúng một giá trị. Các lớp nền được khai báo rời nhau khi phù hợp. Actor và Filmmaker không rời nhau vì một người có thể vừa diễn xuất vừa đạo diễn.

**Domain/range và cardinality là ngữ nghĩa OWL:** domain/range có thể suy ra kiểu; cardinality đúng một không tự báo lỗi khi trường bị thiếu. Vì OWL dùng giả định thế giới mở và không mặc định mọi tên khác nhau đều là cá thể khác nhau, kiểm tra cấu trúc dữ liệu của ứng dụng được thực hiện riêng bằng Python.

**Ví dụ suy luận:** Contribution có DirectorRole được phân loại DirectingContribution; Person có đóng góp thuộc nhóm đạo diễn/biên kịch/sản xuất được phân loại Filmmaker. Nolan không được gán sẵn Filmmaker trong `movies.ttl`.

**Cách chạy:** 12 lớp dùng OWL RL; MultiGenreFilm và FilmStudio dùng SPARQL COUNT DISTINCT bổ sung. Việc đếm các IRI là quy tắc ứng dụng, chưa chứng minh ngữ nghĩa cardinality OWL DL nếu chưa có căn cứ cá thể khác nhau. Đã chạy HermiT/Pellet riêng trên OWL chính: nhất quán, không có lớp không khả thỏa; 12 lớp có số lượng khớp OWL RL, hai lớp cardinality có 0 cá thể suy luận DL. File OWL, Turtle và JSON-LD cùng dùng timestamp đến mili giây; manifest nguồn giữ thời điểm đầy đủ. Bảng đủ các lớp/thuộc tính ở `Ontology_Redesign.md`.

\newpage

## 4. YC2 — Thu thập và xuất xứ

| Chỉ số bản cục bộ | Giá trị |
|:--|--:|
| Phim / người / đóng góp | 30 / 851 / 1.010 |
| Công ty sản xuất / thực thể giải thưởng | 45 / 672 |
| Thể loại / quốc gia / ngôn ngữ | 75 / 11 / 15 |
| Phim có năm, thời lượng và đạo diễn | 30/30 cho từng trường |
| Phản hồi được liệt kê / file gốc còn có | 76 / 76 |

Wikidata được lấy qua API với sitelink Wikipedia tiếng Anh chính xác. P57/P161/P58/P162 cung cấp đạo diễn/diễn viên/biên kịch/nhà sản xuất; P136 thể loại, P495 quốc gia, P364 ngôn ngữ, P577 ngày phát hành, P2047 thời lượng, P166 giải, P272 công ty. Thu thập giải thưởng của người là bước bổ sung, khác giải của phim.

DBpedia chỉ được nối khi tài nguyên khớp tiêu đề và được khai báo `dbo:Film`. Chỉ có 28 liên kết DBpedia; không tự đoán hai phim còn lại. Metadata nguồn có URL, provider, retrieved_at, HTTP status, SHA-256 và đường dẫn. Hash kiểm tra toàn vẹn byte, không chứng minh độ đúng của phát biểu.

**Kiểm tra nguồn hiện tại:** Đã bổ sung 43 phản hồi còn thiếu và chạy lại quy trình: đủ 76/76 file nguồn, 76/76 SHA-256 khớp, không có file thiếu. Một phản hồi tải lại có nội dung thay đổi được ghi thời điểm/hash mới; danh mục lịch sử được giữ ở `evidence/source_manifest_before_recovery.json`. Đã chạy lại collect từ cache nguồn đầy đủ, build, reason, validate và test. Các phản hồi không đổi giữ hash/thời điểm lịch sử; phản hồi đổi có mốc nguồn mới được lưu trung thực.

## 5. YC3 — Chuyển đổi RDF và mức 4 sao

Dữ liệu gồm **19.339 triple**, lược đồ **518 triple**. Triple gồm chủ thể, quan hệ, đối tượng hoặc giá trị. Ví dụ `Inception dbo:director Nolan`; năm dùng số nguyên và thời lượng dùng số phút có datatype. Dùng QID để tạo IRI ổn định, chuẩn hóa thời lượng phút/giờ/giây, ghi các trường hợp nhiều giá trị trong `quality_issues.json`.

Turtle và JSON-LD biểu diễn cùng graph; file `Movie_Ontology.owl` chỉ có lược đồ, `Movie_Knowledge_Graph.owl` gồm lược đồ và dữ liệu. Có CSV cho tiện đọc nhưng CSV tự nó không phải RDF.

Dữ liệu có giấy phép **CC BY-SA 4.0**, ghi công các nguồn; mã ứng dụng MIT. Mức sao cộng dồn: công khai và giấy phép mở, dữ liệu có cấu trúc, định dạng mở, HTTP URI/RDF, rồi liên kết ngoài. **Bản 2.0 đã được xuất bản công khai và kiểm tra không đăng nhập: dữ liệu Turtle/JSON-LD, ontology và mô tả RDF của Inception đều đẳng cấu với graph cục bộ. Có 19.339 triple dữ liệu và 42 lớp ontology.** Kết luận công bố dựa trên kiểm tra URL không đăng nhập và so sánh graph, không chỉ dựa vào file cục bộ.

\newpage

## 6. YC4 — Liên kết cùng danh tính

Có **1.699 liên kết Wikidata + 28 DBpedia = 1.727 owl:sameAs**. Tổng gồm phim, người, thể loại, giải, công ty và các thực thể liên quan; truy vấn 05 chỉ theo phim trả **58 dòng**. `link_audit.json` lưu IRI nội bộ, IRI ngoài và phương pháp nối.

Ví dụ Inception nối với `http://www.wikidata.org/entity/Q25188` và tài nguyên DBpedia Inception. `owl:sameAs` khẳng định cùng một thực thể; `sourceSnapshot` ghi thông tin được lấy ở phản hồi nào. Tái dùng `dbo:Film` là dùng từ vựng ontology ở YC1, còn sameAs giữa cá thể là liên kết ở YC4.

Liên kết cùng danh tính cần kiểm tra kỹ vì OWL có thể lan truyền mọi phát biểu qua sameAs. Khi đếm sau suy luận, bài lọc namespace tài nguyên nội bộ để tránh tính các alias bên ngoài như nhiều cá thể. Điều kiện 4 sao và liên kết ngoài của bản 2.0 đã được đối chiếu trên bản công khai; tiêu chí 5 sao đạt theo phạm vi đề.

## 7. YC5 — Ba cách truy vấn

**Web:** mở `http://127.0.0.1:8000`, chọn Sample queries, bấm Run query. Có 14 câu trực tiếp trên giao diện, tìm phim, mở IRI và tải kết quả. SELECT trả bảng, ASK trả boolean, CONSTRUCT trả RDF. Chế độ local dùng endpoint; `/?browser` dùng Comunica. Website hosted dùng engine trình duyệt, không phải endpoint Flask công khai.

**Terminal:** `.venv/bin/python src/query.py queries/02_inception.rq` trả Inception, 2010, 148 phút, Christopher Nolan. Truy vấn Nolan trả 8 dòng; đóng góp Inception 25 dòng; diễn viên Inception 21 dòng. Các file 17/18 có LIMIT 20, nên 20 dòng hiển thị không phải tổng 769 Actor hoặc 89 Filmmaker.

**Endpoint:** GET/POST `/sparql`, hỗ trợ form hoặc `application/sparql-query`; SELECT/ASK trả SPARQL Results JSON, CONSTRUCT/DESCRIBE trả Turtle. Endpoint chặn Update và SERVICE/FROM tải ngoài. Tra cứu cục bộ với Accept text/turtle trả 303 đến mô tả RDF.

```bash
curl -X POST http://127.0.0.1:8000/sparql \
  -H 'Content-Type: application/sparql-query' \
  --data-binary @queries/02_inception.rq
.venv/bin/python src/query.py queries/18_inferred_filmmakers.rq --reasoned
```

Ảnh ứng dụng và ảnh trang Inception nằm ở `evidence/screenshots/`; ảnh trong slide là ảnh thao tác thật. Các truy vấn suy luận trả rỗng trên graph khai báo là kết quả đúng với chế độ nạp hiện tại.

\newpage

## 8. Kiểm tra, đánh giá và giới hạn

Lần kiểm tra 08/10/2026: **14 test pass**; kiểm tra các trường dữ liệu hiện tại không phát hiện lỗi; chạy đủ 24 file trên graph khai báo và trên graph có schema/phân loại đã lưu. `evidence/review_2026-10-08.json` chứa số liệu và xác nhận không còn file nguồn thiếu. `evidence/tests.txt` chứa kết quả test. Kiểm tra trình duyệt sau đồng bộ file local nằm trong `browser_checks.json`; trạng thái public đo mới ở `publication_checks.json`.

| Yêu cầu | Điểm tự đề xuất / 2 | Giới hạn |
|:--|--:|:--|
| YC1 | 2,0 | Ontology đã triển khai; HermiT/Pellet xác nhận nhất quán |
| YC2 | 2,0 | 76/76 phản hồi gốc có và khớp hash |
| YC3 | 2,0 | RDF công khai đẳng cấu với local |
| YC4 | 2,0 | Liên kết và bản công bố đã đồng bộ |
| YC5 | 2,0 | Web, endpoint và terminal hoạt động |
| Tổng | **10/10** | Thang chia đều do nhóm đề xuất; không phải điểm giảng viên |

Mẫu phim có chủ đích, không đại diện toàn bộ điện ảnh. DocumentaryFilm hiện không có cá thể; ASK false chỉ nói về dataset này. MultiGenreFilm bằng toàn bộ 30 phim vì mỗi phim trong mẫu có ít nhất hai thể loại. Các nhóm genre/award còn dùng từ khóa nhãn, cần kiểm tra thủ công khi mở rộng nguồn. FilmStudio là tên lớp theo quy tắc của bài (công ty có ít nhất ba phim trong mẫu), không phải xác nhận quy mô studio ngoài đời. Chưa mô hình hóa ngân sách, doanh thu, streaming hoặc từng bản dựng phim.

**Trước khi nộp:** điền thành viên trên bìa, xem lại video/slide và dùng ZIP mới. Phần nguồn, bản công khai và video đã được sửa; kiểm tra lại khi thay đổi dữ liệu hoặc mô hình. Lời thuyết trình riêng nằm ở `Script_thuyet_trinh.md` và notes của từng slide.

Nguồn ngữ nghĩa: [Linked Data và thang sao](https://www.w3.org/DesignIssues/LinkedData.html), [SPARQL 1.1](https://www.w3.org/TR/sparql11-query/), [OWL 2 Profiles](https://www.w3.org/TR/owl2-profiles/). Dẫn chiếu tiêu chuẩn dùng để giải thích RDF, SPARQL và giới hạn reasoning; số liệu ứng dụng lấy từ repository.

**Cập nhật timestamp/reasoner:** dùng duy nhất Movie_Knowledge_Graph.owl cho graph đầy đủ. HermiT/Pellet đã chạy; xem Ket_qua_reasoner.pdf. Video_demo.mp4 giữ nguyên theo yêu cầu nhóm; timestamp trong dữ liệu mới giảm đến mili giây, nội dung phim/quan hệ giữ nguyên, đã kiểm tra ở video_dataset_compatibility.json. Video chưa thể hiện kết quả reasoner mới và vẫn nhắc bộ slide ngắn 13 trang.

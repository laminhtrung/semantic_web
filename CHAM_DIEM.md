---
title: "MovieLOD: tự đánh giá sau khi sửa lỗi"
date: "Đối chiếu trực tiếp 08/10/2026 · giờ Việt Nam"
---

## Kết quả hiện tại: 10/10 theo thang tự đề xuất

**5/5 yêu cầu đạt trong phạm vi đề và các kiểm tra hiện tại.** Đề gốc không quy định trọng số; dùng thang chia đều **2 điểm/yêu cầu**, 4 tiêu chí con mỗi yêu cầu, mỗi mục 0,5 điểm. Đây là tự đánh giá có minh chứng, **không phải điểm chính thức của giảng viên**.

Ảnh đề: [đề gốc](<Screenshot 2026-10-05 at 14.39.32.png>). Đề yêu cầu ontology, thu thập, 4 sao, liên kết 5 sao, endpoint/terminal; sản phẩm gồm slide, báo cáo tối đa 15 trang, video 3–5 phút.

| YC | Yêu cầu | Điểm / 2 | Minh chứng chính |
|:--|:--|--:|:--|
| YC1 | Define an ontology for the selected domain | **2,0** | 42 lớp; 23 quan hệ; 6 datatype property; OWL và test |
| YC2 | Collect relevant data in this domain | **2,0** | 76/76 phản hồi gốc có, hash khớp; collect từ cache đã chạy lại |
| YC3 | Transform collected data into 4* standard | **2,0** | RDF, HTTP IRI, giấy phép; graph public đẳng cấu local |
| YC4 | Find and establish links to other datasets to obtain 5* standard | **2,0** | 1.727 owl:sameAs; bản công khai hiện tại có đầy đủ liên kết |
| YC5 | Provide an interface via SPARQL endpoint/terminal to query data | **2,0** | Web, GET/POST endpoint, terminal, 24 truy vấn và kiểm tra |
| Tổng | | **10,0/10** | **Cả 5 yêu cầu có minh chứng đạt** |

## Ba phần làm mất điểm đã được sửa

| Trước sửa | Sau sửa | Phần được khôi phục |
|:--|:--|:--|
| Thiếu 43/76 file nguồn | Đủ 76 file, 76 hash khớp. Các bản đổi nội dung có thời điểm/hash mới và giữ danh mục lịch sử | YC2 +0,5 |
| Hosted dùng 12.089 triple/9 lớp, khác local | Đã triển khai 2.0; hosted 19.339 triple/42 lớp; Turtle/JSON-LD/ontology/mô tả Inception đều đẳng cấu local | YC3 +0,5 |
| Liên kết mới chỉ có đầy đủ ở local | Graph công khai đã khớp bản chứa 1.727 liên kết | YC4 +0,5 |

Bản tự chấm trước sửa 8,5/10 được giữ ở `evidence/self_assessment_before_fix.md`. Biên bản thiếu nguồn trước sửa ở `review_before_fix.json`; kiểm tra HTTP cũ ở `review_publication_2026-10-08.json` là **lịch sử**, không dùng thay kết quả mới. Đã tạo video demo 2.0 để thay video tổng hợp cũ.

## Các kiểm tra thực tế

- `src/collect.py` chạy lại từ cache nguồn đầy đủ, xác định đủ 30 phim. API Wikidata được giãn lượt tải và tôn trọng Retry-After khi trả 429; cache hợp lệ không bị chờ.
- `src/build.py` tạo lại graph: **19.339 triple dữ liệu**, **518 triple lược đồ**, **42 lớp có tên**. Có **30 phim, 851 người, 1.010 Contribution, 45 công ty, 672 thực thể giải**, 75 thể loại, 11 quốc gia, 15 ngôn ngữ.
- `src/validate.py`: data_checks_passed=true, source_hashes_match=true, snapshots_checked=76, missing_source_files=[], query_files_executed=24. Truy vấn hierarchy/phân loại chạy ở chế độ có schema và kiểu bổ sung phù hợp.
- `src/reason.py` đã chạy lại; `ontology_reasoning.json` ghi kết quả và không có lỗi được phát hiện trong bộ luật dùng. File phân loại tách riêng khỏi dữ liệu khai báo.
- **14 test pass** (thời gian thực tế ở evidence/tests.txt); **9/9 kiểm tra trình duyệt pass**. Endpoint SELECT/ASK/CONSTRUCT, nguồn/IRI, dữ liệu Inception và luật phân loại đã được kiểm tra.
- `src/check_publication.py` dùng HTTP không cookie/đăng nhập: **8 URL trả 200**, cả **4 graph RDF kiểm tra đẳng cấu local**, có giấy phép mở và mô tả RDF tra cứu qua IRI.
- Video mới ghi tương tác trình duyệt và kết quả lệnh thực thi thật, **290,05 giây**, 1280×720, có giọng tổng hợp tiếng Việt Linh và đủ YC1–YC5.

Các biên bản: `source_recovery.json`, `validation.json`, `ontology_reasoning.json`, `tests.txt`, `browser_checks.json`, `publication_checks.json`, `video.json`, `review_2026-10-08.json`, `deliverables.json`.

## YC1 — Ontology: 2,0/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Lớp phù hợp lĩnh vực và cây phân cấp | 0,5 | 42 owl:Class IRI; CreativeWork/Agent/Contribution/Genre/Award; dùng Film/Person/Country trực tiếp từ DBpedia |
| Quan hệ và datatype property có ý nghĩa | 0,5 | 23 object property, 6 datatype property; domain/range và mô hình người–phim–vai trò |
| Có ngữ nghĩa OWL và ràng buộc | 0,5 | equivalentClass, giao/hợp, restriction tồn tại/hasValue, inverse, functional, cardinality, disjoint khi phù hợp |
| Ontology đọc được và test minh họa | 0,5 | Hai file OWL, Turtle, kiểm tra bản xuất và các luật OWL RL trong tests |

**Giới hạn giữ nguyên:** 12 lớp dùng OWL RL; MultiGenreFilm/FilmStudio dùng COUNT DISTINCT bổ sung. Đếm IRI là quy tắc ứng dụng, không tự chứng minh cardinality OWL DL do OWL không mặc định mọi IRI khác nhau đều chỉ các cá thể khác nhau. Đã chạy HermiT/Pellet và xác nhận nhất quán; hai lớp cardinality có 0 cá thể được suy luận DL. Đề không bắt buộc reasoner DL hay công cụ cụ thể; không tự cộng/trừ điểm vì công cụ ngoài 5 yêu cầu.

## YC2 — Thu thập: 2,0/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Dữ liệu thật liên quan đến điện ảnh | 0,5 | 30 phim và các thực thể liên quan lấy từ Wikidata/DBpedia |
| Có mã thu thập và xác định danh tính | 0,5 | collect.py; sitelink chính xác; DBpedia root phải có dbo:Film |
| Có metadata và quy tắc nguồn | 0,5 | URL/provider/time/status/hash/path; sourceSnapshot; ghi mốc mới khi phản hồi đổi |
| Giữ đủ phản hồi gốc và kiểm tra tái lập | 0,5 | 76/76 file và hash khớp; collect/build/validate/reason chạy lại |

43 phản hồi thiếu đã được bổ sung. Không gán hash cũ cho phản hồi đổi nội dung; một phản hồi được lưu hash/thời điểm mới và dựng lại dữ liệu. Danh mục trước sửa ở `source_manifest_before_recovery.json`. Quy tắc gitignore loại phản hồi nguồn đã được bỏ; ZIP nộp chứa đầy đủ phản hồi gốc. Hash kiểm tra toàn vẹn byte, không chứng minh tất cả phát biểu ngoài đời đúng. Không trừ vì chỉ 30 phim: đề không đưa số lượng tối thiểu.

## YC3 — Chuyển đổi 4 sao: 2,0/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Chuyển nguồn thành RDF có lớp/quan hệ/giá trị | 0,5 | build.py; 19.339 triple, datatype năm/thời lượng; test Inception |
| Định dạng mở và HTTP IRI có thể tra cứu | 0,5 | Turtle/JSON-LD/OWL; trang resource có JSON-LD và liên kết Turtle |
| Giấy phép mở, ghi công và metadata dataset | 0,5 | CC BY-SA 4.0; LICENSE-DATA.txt; Dublin Core/VoID |
| Công bố bản hiện tại, kiểm tra không đăng nhập | 0,5 | URL public 200; Turtle và JSON-LD đẳng cấu local; trạng thái succeeded thật |

Mức sao cộng dồn theo [Linked Data và thang sao](https://www.w3.org/DesignIssues/LinkedData.html). Kết luận dựa trên giấy phép, HTTP IRI, khả năng tra cứu và graph công khai đúng phiên bản, không chỉ file RDF cục bộ hoặc giá trị audience trong JSON. Content negotiation/303 được kiểm tra ở Flask local; hosted tĩnh cung cấp HTML/JSON-LD và link RDF, không tự khẳng định nó có cùng hành vi 303.

## YC4 — Liên kết 5 sao: 2,0/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Có liên kết tới dataset ngoài | 0,5 | 1.699 Wikidata + 28 DBpedia = 1.727 owl:sameAs |
| Có quy tắc cùng danh tính | 0,5 | QID/sitelink chính xác; chủ thể DBpedia khớp và có kiểu Film |
| Lưu, kiểm kê và truy vấn liên kết | 0,5 | link_audit.json; query 05 trả 58 dòng theo phim; query 08 True |
| Hoàn tất điều kiện 4 sao + liên kết trên bản public | 0,5 | Graph public đẳng cấu bản chứa toàn bộ liên kết; IRI RDF tra cứu được |

Tái dùng lớp DBpedia ở YC1 khác sameAs nối cá thể ở YC4. sourceSnapshot ghi xuất xứ, không thay sameAs. Tổng liên kết trên mọi nhóm thực thể khác số dòng truy vấn chỉ theo phim. Không tự cho điểm thêm vì tăng số lượng liên kết.

## YC5 — Truy vấn: 2,0/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Web cho người dùng | 0,5 | Query editor, 14 mẫu trực tiếp, results/export, tìm phim và mở IRI |
| Endpoint hỗ trợ giao thức truy vấn | 0,5 | GET/POST; JSON SELECT/ASK; Turtle CONSTRUCT/DESCRIBE; test protocol |
| Terminal đọc file SPARQL | 0,5 | query.py; 24 file; --reasoned cho schema/phân loại |
| Câu hỏi và kết quả được kiểm tra | 0,5 | Inception 2010/148/Nolan; 8 phim Nolan; 25 đóng góp; ASK True; tests/browser |

Endpoint mặc định đọc graph khai báo. Hosted có Comunica trong trình duyệt, không phải endpoint Flask public. Query 17/18 LIMIT 20, không lấy 20 dòng làm tổng Actor/Filmmaker. Không có requirement về Update/federated SERVICE nên không tự trừ vì endpoint chặn chúng.

## Sản phẩm nộp ngoài thang 10

| Sản phẩm | Kết quả |
|:--|:--|
| Báo cáo ≤15 trang | Bản 2.0 đã cập nhật; số trang thực ở document_pages.json |
| Slide | 24 trang PPTX/PDF, font Be Vietnam Pro, ảnh app thật, sơ đồ; có Speaker Notes và 11 khung Protégé để nhóm bổ sung |
| Video 3–5 phút | Video_demo.mp4 mới: 290,05 giây; ghi thao tác app và kết quả lệnh; giọng tổng hợp Linh |
| Script thuyết trình riêng | Script_thuyet_trinh.md/pdf, khớp 24 slide và có câu hỏi bảo vệ |
| Tài liệu đọc hiểu | A–Z, hướng dẫn chi tiết, mô tả ontology và bảng đầy đủ tiếng Việt |
| Mã/dữ liệu/giấy phép/evidence | ZIP mới chứa nguồn, RDF/OWL, truy vấn, biên bản và sản phẩm nộp |

Giảng viên có thể dùng trọng số khác hoặc đánh giá chất lượng bảo vệ. Nhóm cần điền tên thành viên/lớp trên bìa, xem lại video và tập trình bày; không được gọi giọng tổng hợp là lời ghi của sinh viên. Các giới hạn về mẫu phim, ánh xạ theo nhãn và cardinality bằng COUNT DISTINCT vẫn được giữ. HermiT/Pellet đã xác nhận nhất quán; bảng DL nằm trong Ket_qua_reasoner.pdf.

## Kiểm tra lại khi sửa bài

```bash
.venv/bin/python src/collect.py
.venv/bin/python src/build.py
.venv/bin/python src/prepare_web.py
.venv/bin/python src/reason.py
.venv/bin/python src/validate.py
.venv/bin/python -m pytest -q
```

Sau thay đổi dữ liệu, khởi động lại server, kiểm tra browser, cập nhật tài liệu và đánh giá lại tính tương thích của video, xuất bản và chạy check_publication.py. Chỉ giữ đề xuất 10/10 khi các minh chứng tiếp tục đạt. Không đổi điểm hoặc JSON trạng thái để thay cho sửa và kiểm tra thật.

**Ảnh Protégé trong bộ 24 trang:** hiện là khung chờ có hướng dẫn, chưa phải ảnh đã chụp. Checklist_anh_Protege.md/pdf và các Speaker Notes ghi đúng file/view cần dùng. Đây là phần nhóm chủ động bổ sung theo yêu cầu, không thay bằng ảnh dựng.

## Đồng bộ timestamp và reasoner

File chính Movie_Knowledge_Graph.owl, Turtle/JSON-LD và Web dùng timestamp đến mili giây. HermiT/Pellet đã xác nhận nhất quán và không có lớp không khả thỏa; 12 lớp khớp OWL RL. MultiGenreFilm/FilmStudio có 0 cá thể suy luận DL; 30/6 là số đếm ứng dụng. Video giữ nguyên theo yêu cầu nhóm; không coi hash dữ liệu trong video là hash bản mới. video_dataset_compatibility.json xác minh mọi triple khác retrievedAt và byte MP4 giữ nguyên.

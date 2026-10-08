---
title: "MovieLOD: tự đánh giá theo 5 yêu cầu đề bài"
date: "Đối chiếu trực tiếp 08/10/2026 · giờ Việt Nam"
---

## Kết quả hiện tại

**8,5/10 theo thang tự đề xuất: 2/5 yêu cầu đạt đầy đủ, 3/5 đạt phần lớn.** Đây không phải điểm chính thức của giảng viên. Ảnh đề gốc không quy định trọng số; tài liệu dùng **2 điểm/yêu cầu**, mỗi yêu cầu có 4 tiêu chí con, mỗi tiêu chí 0,5 điểm. Điểm này đánh giá bộ bài hiện tại, gồm dữ liệu cục bộ và phiên bản công bố tương ứng; không lấy thành công của website cũ để xác nhận bản 2.0.

Ảnh đề: [đề gốc](<Screenshot 2026-10-05 at 14.39.32.png>). Đề yêu cầu ontology, thu thập, 4 sao, liên kết 5 sao, endpoint/terminal; sản phẩm gồm slide, báo cáo tối đa 15 trang, video 3–5 phút.

| YC | Yêu cầu | Điểm / 2 | Mức đạt | Thiếu sót ảnh hưởng điểm |
|:--|:--|--:|:--|:--|
| YC1 | Define an ontology for the selected domain | 2,0 | Đầy đủ trong phạm vi kiểm tra | Chưa có chứng minh OWL DL toàn bộ; đề không bắt buộc nên không tự trừ thêm |
| YC2 | Collect relevant data in this domain | 1,5 | Phần lớn | Thiếu 43/76 file phản hồi gốc, chưa tái lập đủ nguồn |
| YC3 | Transform collected data into 4* standard | 1,5 | Phần lớn | Dữ liệu public chưa khớp bản 2.0 cục bộ |
| YC4 | Find and establish links to other datasets to obtain 5* standard | 1,5 | Phần lớn | Liên kết local có, chưa công bố đồng bộ toàn bộ bản mới |
| YC5 | Provide an interface via SPARQL endpoint/terminal to query data | 2,0 | Đầy đủ | Web/endpoint/terminal hoạt động; suy luận dùng terminal riêng |
| Tổng | | **8,5/10** | **2 đầy đủ, 3 phần lớn** | |

## Minh chứng được kiểm tra lại

- Parse RDF/OWL và kiểm tra kiểu/thuộc tính trong dữ liệu cục bộ; graph dữ liệu **19.339 triple**, lược đồ **518 triple**, **42 lớp có tên**. Không phát hiện lỗi trong kiểm tra trường ứng dụng `check_data()`.
- Dữ liệu: **30 phim, 851 người, 1.010 Contribution, 45 công ty, 672 thực thể giải**, 75 thể loại, 11 quốc gia, 15 ngôn ngữ. Ba lớp DBpedia dùng trực tiếp là Film, Person, Country.
- Có **1.727 owl:sameAs**: 1.699 Wikidata và 28 DBpedia. Query 05 chỉ xét phim nên trả 58 dòng.
- Kiểm tra 76 đường dẫn nguồn: **33 file có và khớp hash, 43 file thiếu, 0 hash sai trong file có**. Không xác nhận hash cho file thiếu. Lệnh validate.py thực tế dừng FileNotFoundError; evidence/validation.json là biên bản lịch sử.
- Chạy đủ **24 file truy vấn** trên graph gốc và trên graph có schema + file phân loại đã lưu. Kết quả ở [review mới](evidence/review_2026-10-08.json). Truy vấn có phân loại không phải lần chạy reasoner mới của review script; các test độc lập có thực thi suy luận.
- **13 test pass** trong 89,22 giây; [biên bản](evidence/tests.txt). Các test xác nhận những hành vi cụ thể, không chứng minh toàn bộ dữ liệu nguồn đúng hoặc OWL DL nhất quán.
- Kiểm tra HTTP public không có phiên đăng nhập: trang chủ, RDF, ontology, IRI Inception, giấy phép đều HTTP 200. Graph hosted **12.089 triple**, không đẳng cấu graph local; ontology hosted có **9 lớp**. [Biên bản HTTP mới](evidence/review_publication_2026-10-08.json).
- Giao diện, ảnh và file tĩnh local đã được build đồng bộ; kiểm tra trình duyệt mới và ảnh ở `evidence/browser_checks.json`, `evidence/screenshots/`. Không dùng việc đồng bộ local làm bằng chứng đã triển khai public.

## YC1 — Ontology: 2,0/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Lớp phù hợp lĩnh vực và cây phân cấp | 0,5 | 42 owl:Class IRI; CreativeWork/Agent/Contribution/Genre/Award; Film/Person/Country tái dùng DBpedia |
| Quan hệ và datatype property có ý nghĩa | 0,5 | 23 object property, 6 datatype property; domain/range; quan hệ trực tiếp và Contribution |
| Có ngữ nghĩa OWL/ràng buộc | 0,5 | equivalentClass, giao/hợp, restriction tồn tại/hasValue, inverse, functional, cardinality, rời nhau khi phù hợp |
| Xuất ontology đọc được, có test minh họa | 0,5 | Movie_Ontology.owl và Movie_Knowledge_Graph.owl; kiểm tra bản xuất và luật OWL RL trong tests |

**Giới hạn:** 12 lớp phân loại dùng OWL RL; 2 lớp MultiGenreFilm/FilmStudio được thêm qua SPARQL COUNT DISTINCT. Đếm IRI là quy tắc ứng dụng, không tự chứng minh cardinality OWL DL do không có giả định mọi IRI khác nhau đều là cá thể khác nhau. Không nói đã có kết quả HermiT/Pellet nếu chưa chạy. Đề không yêu cầu công cụ DL cụ thể; không tự cộng/trừ điểm vì chọn công cụ khác.

## YC2 — Thu thập: 1,5/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Có dữ liệu thực liên quan đến điện ảnh | 0,5 | 30 phim và các thực thể liên quan, dữ liệu chuẩn hóa có phát biểu Wikidata |
| Có mã thu thập từ nguồn thật | 0,5 | collect.py, API Wikidata, JSON DBpedia, khớp sitelink và kiểm tra dbo:Film |
| Có metadata xuất xứ và quy tắc xử lý nguồn | 0,5 | snapshots.json có URL/time/provider/status/hash/path; normalized staging và sourceSnapshot |
| Giữ đủ phản hồi gốc và kiểm tra tái lập trọn bộ | **0,0** | Thiếu 43 file trong 76 được liệt kê; validate.py không hoàn tất |

Việc có metadata không khắc phục mất file gốc; không cho điểm đầy đủ phần tái lập. Dữ liệu còn đủ để chạy ứng dụng và build từ bản chuẩn hóa nên không chấm mất toàn bộ YC2. Không trừ vì chỉ 30 phim: đề không quy định số lượng tối thiểu.

## YC3 — Chuyển đổi 4 sao: 1,5/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Chuyển dữ liệu thành RDF có lớp/quan hệ/giá trị | 0,5 | build.py; 19.339 triple; kiểm tra fields và test Inception |
| Có định dạng mở và HTTP IRI để mô tả/tải | 0,5 | Turtle, JSON-LD, OWL; resource pages; local RDF dereferencing |
| Có giấy phép dữ liệu mở, ghi công và metadata dataset | 0,5 | CC BY-SA 4.0, LICENSE-DATA.txt; Dublin Core/VoID |
| Công bố đầy đủ bản hiện tại và đối chiếu truy cập thực tế | **0,0** | Public vẫn là bản 12.089 triple/9 lớp; local 19.339/42 |

Website **đã public**, không mô tả nó là private hay HTTP 401 theo biên bản cũ. Tuy nhiên chưa công bố đồng bộ bản 2.0. HTTP 200 file dữ liệu chưa chứng minh toàn bộ phiên bản nộp hiện tại đạt 4 sao. Theo [Linked Data và thang sao](https://www.w3.org/DesignIssues/LinkedData.html), các mức cộng dồn và cần công bố với giấy phép mở. Hành vi 303 local không được giả định cho hosted tĩnh.

## YC4 — Liên kết 5 sao: 1,5/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Có liên kết tới dataset ngoài | 0,5 | 1.699 Wikidata + 28 DBpedia |
| Có quy tắc xác định cùng danh tính | 0,5 | QID/sitelink chính xác; DBpedia root phải là Film |
| Liên kết được lưu và truy vấn/kiểm kê | 0,5 | owl:sameAs, link_audit.json, query 05/08; phim có liên kết ngoài |
| Hoàn tất mức 5 sao trên bản công khai khớp local | **0,0** | Cần điều kiện 4 sao và xuất bản toàn bộ bản mới |

Điểm công bố được xét ở cả YC3 và YC4 vì 5 sao phụ thuộc 4 sao; đây là cách chia tiêu chí của thang tự đề xuất, không phải quy định chấm của đề. Tái dùng dbo:Film ở YC1 khác sameAs nối cá thể ở YC4; không dùng cùng một việc để tự cộng hai lần.

## YC5 — Truy vấn: 2,0/2,0

| Tiêu chí con | Điểm | Minh chứng |
|:--|--:|:--|
| Có giao diện Web cho người dùng | 0,5 | Query editor, 14 mẫu trực tiếp, results, export, tìm phim/IRI |
| Endpoint hỗ trợ giao thức truy vấn | 0,5 | Flask GET/POST, JSON SELECT/ASK, Turtle CONSTRUCT/DESCRIBE; test protocol |
| Terminal chạy file SPARQL | 0,5 | query.py; 24 file; --reasoned cho nhóm schema/phân loại |
| Có truy vấn thực và kiểm tra kết quả | 0,5 | Inception 2010/148/Nolan; 8 phim Nolan; 25 đóng góp; ASK True; 13 test pass |

Endpoint mặc định không tự nạp suy luận. Bản hosted có engine Comunica trong trình duyệt; không gọi đó là endpoint Python công khai. Truy vấn mẫu 17/18 LIMIT 20; số dòng không phải tổng cá thể. Không có requirement về federated SERVICE hay Update nên không tự trừ vì endpoint chặn chúng.

## Sản phẩm nộp: kiểm tra riêng ngoài thang 10

| Sản phẩm | Trạng thái |
|:--|:--|
| Báo cáo ≤15 trang | Đã cập nhật bản 2.0; số trang xuất thực tế ở evidence/document_pages.json |
| Slide | PPTX chỉnh sửa được, 13 slide; PDF 13 trang; font Be Vietnam Pro; sơ đồ và ảnh thật |
| Video 3–5 phút | **Chưa quay bản mới**. Có kịch bản 4:50; Video_demo.mp4 cũ không được dùng làm minh chứng 2.0 |
| Script thuyết trình riêng | Script_thuyet_trinh.md/pdf, khớp 13 slide; lời nằm cả trong Speaker Notes |
| Tài liệu đọc hiểu | A–Z, hướng dẫn chi tiết, mô tả ontology và bảng đầy đủ đã sửa bằng tiếng Việt |

Việc có kịch bản không có nghĩa video mới đã đạt. Điểm 8,5 đánh giá 5 yêu cầu kỹ thuật theo thang đề xuất; giảng viên có thể xét thêm sản phẩm nộp hoặc dùng trọng số khác.

## Cách hoàn tất và chấm lại

1. Khôi phục 43 phản hồi gốc đúng snapshot từ sao lưu hoặc thu thập lại với mốc nguồn mới; kiểm tra đầy đủ hash và chạy validate.py hoàn tất. Không giả vờ dữ liệu tải mới là phản hồi lịch sử khớp hash cũ.
2. Xuất bản lại bản 2.0, kiểm tra từ phiên không đăng nhập, tải RDF/ontology và so sánh graph với local. Ghi bằng chứng thật; sửa JSON audience không thay thế triển khai.
3. Quay demo thật theo Kich_ban_video.md, đo 180–300 giây, xem lại nội dung và chữ/âm thanh; điền nhóm/thành viên trên bìa.
4. Chạy lại kiểm tra và chấm theo cùng thang. Nếu nguồn đủ (+0,5), công bố 4 sao khớp (+0,5), liên kết 5 sao bản mới đủ (+0,5) và các kiểm tra khác vẫn đạt thì có thể đề xuất **10/10**. Không nâng điểm trước khi có minh chứng.

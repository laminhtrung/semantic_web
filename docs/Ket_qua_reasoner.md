# Kết quả reasoner và đồng bộ dữ liệu

Cập nhật ngày 08/10/2026. Dùng **một file knowledge graph chính: ontology/Movie_Knowledge_Graph.owl**. Movie_Ontology.owl vẫn là file schema riêng, không phải bản knowledge graph thứ hai. Bản OWL tương thích riêng đã được bỏ.

## Kết luận

**HermiT 1.3.8.1099 và Pellet 2.3.1 đều chạy thành công trên file chính:** ontology nhất quán, không có lớp có tên không khả thỏa; đã hoàn tất phân cấp lớp và suy luận cá thể. Chạy qua CLI với Java Temurin 17.0.20.1; không phải ảnh giao diện Protégé. Pellet cũng kiểm tra file schema và xác nhận nhất quán.

Lỗi trước đây phát sinh khi HermiT đọc giây có sáu chữ số thập phân. Pipeline hiện xuất timestamp đến mili giây: .736805+00:00 thành .736+00:00. Cách xuất này áp dụng thống nhất cho OWL, Turtle, JSON-LD và Web. Manifest nguồn thô giữ độ chính xác gốc; không sửa phản hồi hoặc hash nguồn. Không bỏ thuộc tính ngày giờ, không thêm AllDifferent để thay đổi suy luận.

## Số cá thể suy luận

Hai reasoner có số lượng khớp nhau. Chỉ đếm IRI tài nguyên nội bộ, loại alias Wikidata/DBpedia.

| Lớp | HermiT | Pellet |
|---|---:|---:|
| ActingContribution | 855 | 855 |
| DirectingContribution | 31 | 31 |
| WritingContribution | 51 | 51 |
| ProducingContribution | 73 | 73 |
| Actor | 769 | 769 |
| Filmmaker | 89 | 89 |
| AwardWinner | 290 | 290 |
| ActionFilm | 12 | 12 |
| ComedyFilm | 4 | 4 |
| DramaFilm | 25 | 25 |
| ScienceFictionFilm | 6 | 6 |
| AwardWinningFilm | 26 | 26 |
| MultiGenreFilm | 0 | 0 |
| FilmStudio | 0 | 0 |

Nolan (person-Q25191) thuộc **Filmmaker** và **AwardWinner** theo cả hai reasoner. Mười hai lớp đầu khớp OWL RL. Pellet hoàn tất bước suy luận cá thể trong khoảng 120,49 giây.

**MultiGenreFilm và FilmStudio:** HermiT/Pellet có 0 cá thể được suy luận vào hai lớp này; số 30/6 trong pipeline ứng dụng là quy tắc SPARQL COUNT DISTINCT. OWL không mặc định hai IRI khác nhau là hai cá thể khác nhau. Không có cá thể suy luận không đồng nghĩa lớp không khả thỏa. Phải ghi rõ phương pháp khi dùng hai bảng kết quả.

## Dùng trong Protégé

1. Stop reasoner và đóng bản đang mở để tránh dùng dữ liệu cũ.
2. Mở ontology/Movie_Knowledge_Graph.owl đã cập nhật trong thư mục dự án này.
3. Chọn HermiT → Start reasoner; xem inferred hierarchy hoặc inferred Types.
4. Với Nolan, kiểm tra Filmmaker/AwardWinner; ảnh asserted chỉ thể hiện kiểu khai báo.

Nếu từng lưu một bản sao ở thư mục khác, cần mở lại file mới trong dự án. Slide và checklist dùng tên file chính trên.

## Minh chứng và chạy lại

- evidence/hermit_run.json: file đầu vào, SHA-256 và số lượng HermiT.
- evidence/hermit_primary_run.txt: log thực thi và các dòng Type từ HermiT.
- evidence/hermit_inferred_types.ttl: các type trích từ HermiT.
- evidence/pellet_run.json: từng bước kiểm tra, SHA-256, thời gian và số lượng Pellet.
- evidence/pellet_Movie_*_*.txt: log consistency, unsat, classify và realize.
- evidence/pellet_inferred_types.ttl: các type trích từ Pellet.
- evidence/timestamp_normalization.json: thời điểm gốc, thời điểm xuất và hash mới.

```bash
.venv/bin/python -m pip install -r requirements_reasoner.txt
.venv/bin/python src/check_owl_reasoner.py --java /duong/dan/toi/java --realize
```

Lệnh trên chạy Pellet trực tiếp với OWLAPI. Nếu Java nằm trong PATH có thể bỏ --java. HermiT có thể chạy trong Protégé theo hướng dẫn trên. src/build.py luôn xuất timestamp đến mili giây, nên build lại không tạo lỗi sáu chữ số như trước.

## Đồng bộ và video giữ nguyên

Đã kiểm tra Turtle và JSON-LD đẳng cấu; OWL chính đẳng cấu với dữ liệu cộng schema. Các kiểm tra nguồn, truy vấn và test đã chạy lại. Bản Web dùng cùng dữ liệu và được kiểm tra sau xuất bản.

**Video_demo.mp4 giữ nguyên byte theo yêu cầu nhóm.** Hash dữ liệu khi ghi video được giữ đúng là hash lịch sử, không thay bằng hash mới. video_dataset_compatibility.json xác minh chỉ 76 triple retrievedAt thay đổi độ chính xác; mọi triple khác và MP4 không đổi. Nội dung phim, vai trò, liên kết và số đếm trong video vẫn áp dụng. Video chưa thể hiện kết quả HermiT/Pellet mới và vẫn nhắc bộ slide ngắn 13 trang; dùng báo cáo này cùng slide chính 24 trang để trình bày kết quả hiện tại.

Tài liệu: [Owlready2 Reasoning](https://owlready2.readthedocs.io/en/v0.49/reasoning.html).

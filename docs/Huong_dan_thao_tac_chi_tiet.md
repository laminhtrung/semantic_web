---
title: "MovieLOD: hướng dẫn thao tác chi tiết bản 2.0"
date: "MovieLOD 2.0 · Đối chiếu 08/10/2026"
---

## 1. Phiên bản, thứ tự đọc và kết quả cần biết

Tài liệu cho **ontology 2.0**, cập nhật 08/10/2026. Giao diện tiếng Anh, hướng dẫn tiếng Việt. Đọc Huong_dan_A_Z trước; tra bảng lớp ở Ontology_Redesign; tập nói theo Script_thuyet_trinh; quay theo Kich_ban_video.

**Mốc local:** 42 lớp, 30 phim, 851 người, 1.010 đóng góp, 45 công ty, 672 thực thể giải, 19.339 triple dữ liệu, 518 triple lược đồ, 1.727 sameAs. Có 24 file SPARQL và 14 mẫu trực tiếp trên Web. Số lượng có thể thay đổi nếu tải lại nguồn; phải đo lại thay vì dùng mốc này cho phiên bản mới.

**Các lỗi đã sửa:** bổ sung 43 file còn thiếu, hiện đủ 76/76 và hash khớp; công bố bản 2.0 với 19.339 triple và 42 lớp, graph public đẳng cấu local. 14 test pass vẫn cần đi kèm kiểm tra nguồn. Biên bản mới ở evidence/review_2026-10-08.json và publication_checks.json. Video_demo.mp4 đã được thay bằng demo tương tác bản 2.0 với lời tiếng Việt tổng hợp.

## 2. Chuẩn bị môi trường và chạy ngay

Mở terminal tại thư mục chứa README.md và config.json:

```bash
pwd
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/server.py
```

Mở **http://127.0.0.1:8000**. Dừng bằng Ctrl+C. Có thể dùng start.command trên macOS. Nếu cổng bị chiếm, dùng `--port 8001`; thay cổng trong mọi URL/curl. Không tự dừng server của người khác. Server nạp dữ liệu lúc khởi động; **sau build phải khởi động lại** để endpoint không giữ graph cũ trong RAM.

Dữ liệu chuẩn hóa đã có; không cần chạy collect hay validate để mở ứng dụng. Khi ghi video hãy dùng một server vừa khởi động trên cổng trống.

## 3. Kiểm tra giao diện lần đầu

1. Chọn **Inception: year, runtime and director**; bấm **Run query** nếu cần. Thấy Inception, 2010, 148, Christopher Nolan.
2. Chọn **Films directed by Christopher Nolan**: 8 dòng trong dataset.
3. Chọn **Who contributed to Inception, and in which role?**: 25 dòng, các vai trò Actor/Director/Writer/Producer. Hai vai trò cùng người có các Contribution riêng.
4. Chọn **Production companies of Inception**: 4 dòng. **Awards received by The Godfather**: 7 dòng.
5. Chọn **Is Inception linked to its Wikidata entity?**: True.
6. Bấm **Download results** để tải kết quả. Dùng Find a film để tìm Inception, mở trang thực thể, nguồn và link Download RDF (Turtle).

Các số option không cố định khi thêm câu hỏi; dùng **nhãn**. Query editor có thể sửa SPARQL. Gõ `not SPARQL`, bấm Run query để xem báo lỗi; chọn lại câu hỏi mẫu để phục hồi.

## 4. Đọc dữ liệu nguồn và hiểu YC2

Mở src/collect.py: phim được tìm bằng sitelink Wikipedia chính xác. Wikidata cung cấp dữ liệu về đạo diễn, diễn viên, biên kịch, nhà sản xuất, thể loại, quốc gia, ngôn ngữ, năm, thời lượng, giải và công ty. DBpedia chỉ nối khi đúng chủ thể Film.

Mở data/raw/snapshots.json để xem URL/provider/retrieved_at/http_status/sha256/path. Chọn một row có path đang tồn tại để mở phản hồi gốc. Hash là dấu vân tay byte; cùng hash chứng minh nội dung khớp với mốc lưu, không chứng minh độ đúng ngoài đời.

**Nguồn đã hoàn tất:** danh mục có 76 row, 76 file có và 76 hash khớp. validate.py hoàn tất và có biên bản mới. Một phản hồi đổi nội dung được ghi hash/thời điểm mới; danh mục trước khôi phục được giữ để truy lịch sử.

Khôi phục từ bản sao lưu đúng snapshot nếu có. Nếu phải tải lại, giữ mốc thời điểm/hash mới, build và kiểm tra lại; dữ liệu Internet có thể thay đổi. collect.py dùng cache đủ và khớp hash; khi thiếu sẽ tải, `--refresh` buộc tải lại. **Chạy thu thập có thể thay đổi bộ dữ liệu**, hãy giữ bản sao của data trước khi chủ động cập nhật.

```bash
.venv/bin/python src/collect.py
# Refresh all source responses:
.venv/bin/python src/collect.py --refresh
```

## 5. Sinh mô hình/RDF và đồng bộ Web local

```bash
.venv/bin/python src/build.py
.venv/bin/python src/prepare_web.py
```

Build dùng dữ liệu chuẩn hóa hiện có và sinh RDF, OWL, số liệu, trang thực thể và dữ liệu cho Web. Prepare_web cập nhật truy vấn mẫu/giấy phép/PDF trong web/dist. Không cần tải lại nguồn để build bản đã chuẩn hóa. Sau khi build, khởi động lại server.

| File | Dùng để làm gì |
|:--|:--|
| ontology/Movie_Ontology.owl | Chỉ mô hình; mở trong Protégé để xem lớp/ràng buộc |
| ontology/Movie_Knowledge_Graph.owl | Mô hình + dữ liệu; xem cá thể |
| ontology/movie.ttl | Lược đồ Turtle; nguồn đối chiếu 42 lớp |
| data/processed/movies.ttl | Graph khai báo; endpoint truy vấn file này |
| data/processed/movies.jsonld | Cùng dữ liệu dưới dạng JSON-LD |
| data/processed/inferred_classes.ttl | Các kiểu phân loại bổ sung, tách khỏi graph gốc |
| web/dist/data/ | Dữ liệu cấp cho engine trình duyệt |
| evidence/statistics.json | Số liệu mới sau build |

Build không khắc phục các snapshot gốc đã mất. “Dựng được từ dữ liệu chuẩn hóa” khác “tái lập được từ mọi phản hồi gốc”.

## 6. Xem ontology trong Protégé

1. File → Open → ontology/Movie_Ontology.owl. Trong Entities → Classes, chọn Film, Person, Country và kiểm tra IRI DBpedia.
2. Mở CreativeWork/Agent/Contribution/Genre/Award để xem nhánh. Số lớp 42 đếm owl:Class IRI tự khai báo; Protégé có thể hiển thị thêm lớp tham chiếu ngoài và biểu thức vô danh.
3. Object properties → contributionBy/contributionTo/hasRole: kiểm tra domain, range, functional; lớp Contribution có restriction đúng một người/phim/vai trò.
4. Chọn hasContribution/contributionOf để xem inverse; director có inverse directed.
5. Mở Movie_Knowledge_Graph.owl, Individuals chọn film-Q25188 (Inception), person-Q25191 (Nolan), một Contribution của Nolan. Xem vai trò, phim và nguồn.
6. Chọn Filmmaker/Actor để xem equivalentClass. Các kiểu không gán sẵn cần reasoning mới xuất hiện.

**Giới hạn:** HermiT/Pellet đã chạy trên Movie_Knowledge_Graph.owl và xác nhận nhất quán. Timestamp trong bản RDF chuẩn hóa dùng mili giây; bản nguồn thô giữ thời điểm đầy đủ. OWL không mặc định hai IRI là cá thể khác nhau; không khẳng định ngưỡng cardinality bằng số IRI là chứng minh DL. Domain/range/cardinality không tự thay kiểm tra biểu mẫu bằng Python.

## 7. Kiểm tra và tạo phân loại

```bash
.venv/bin/python src/validate.py
.venv/bin/python src/reason.py
.venv/bin/python -m pytest -q
```

Validate kiểm tra các trường cơ bản, hash phản hồi nguồn và chạy file SPARQL. Lệnh hiện chạy hoàn tất: data_checks_passed=true, source_hashes_match=true, snapshots_checked=76 và không có file thiếu. Khi tải lại phải đo mới số lượng/hash thay vì mặc định mốc cũ.

Reason thực hiện OWL RL cho 12 lớp, COUNT DISTINCT cho 2 lớp MultiGenreFilm/FilmStudio. Kết quả ở ontology_reasoning.json và inferred_classes.ttl. Không chạy trong thời gian demo nếu mất nhiều thời gian; chạy trước để tạo file. Không có lỗi được phát hiện bởi owlrl không đồng nghĩa chứng minh OWL DL nhất quán.

Test hiện **14 passed** (xem thời gian thực tế trong evidence/tests.txt). Có kiểm tra endpoint, kiểu DBpedia, chuẩn hóa Inception, role, kiểm tra dữ liệu thiếu, OWL RL và các định nghĩa lớp. Chạy test là một phần xác minh; kiểm tra 76 nguồn được thực hiện riêng và đã đạt.

## 8. Terminal và endpoint

**Terminal đọc graph gốc:**

```bash
.venv/bin/python src/query.py queries/02_inception.rq
.venv/bin/python src/query.py queries/04_credits.rq
.venv/bin/python src/query.py queries/08_ask.rq
```

**Truy vấn có schema/phân loại:**

```bash
.venv/bin/python src/query.py queries/13_fiction_genre_films_via_hierarchy.rq --reasoned
.venv/bin/python src/query.py queries/18_inferred_filmmakers.rq --reasoned
.venv/bin/python src/query.py queries/24_nolan_asserted_types_only.rq
.venv/bin/python src/query.py queries/24_nolan_asserted_types_only.rq --reasoned
```

Câu 13 trả 29 phim khi có schema. Câu 18 hiển thị 20 dòng do LIMIT dù tổng có 89 Filmmaker. Câu 24 gốc có 1 kiểu; có phân loại có 3 kiểu. --reasoned nạp file phân loại đã có, không chạy suy luận ngay.

**Endpoint — server đang chạy ở terminal A:**

```bash
curl -G http://127.0.0.1:8000/sparql \
  --data-urlencode query@queries/02_inception.rq
curl -X POST http://127.0.0.1:8000/sparql \
  -H 'Content-Type: application/sparql-query' \
  --data-binary @queries/02_inception.rq
curl -L -H 'Accept: text/turtle' \
  http://127.0.0.1:8000/resource/film-Q25188
```

GET/POST SELECT/ASK trả JSON. CONSTRUCT/DESCRIBE trả Turtle. Accept Turtle tại resource cục bộ trả 303; -L theo chuyển hướng. Hosted dùng Comunica trong trình duyệt và file RDF, không phải endpoint Flask public. SERVICE/FROM tải ngoài và SPARQL Update bị chặn.

## 9. Ảnh minh chứng và kiểm tra trình duyệt

Script bổ sung cần Playwright và Google Chrome đã cài, hoặc Chromium của Playwright. Script không bắt buộc để mở ứng dụng.

```bash
.venv/bin/python -m pip install playwright
# If a suitable Chrome is not installed:
.venv/bin/python -m playwright install chromium
.venv/bin/python src/browser_check.py --port 8000
```

Server phải chạy đúng cổng. Có thể dùng --port 8001/8002 khi kiểm tra. Script ghi 4 ảnh (app/Nolan/resource/mobile) và browser_checks.json. Minh chứng: SELECT endpoint, Comunica SELECT/GROUP BY/ASK/CONSTRUCT, thông báo lỗi, trang IRI, không tràn màn hình mobile, không có exception trình duyệt.

Ảnh trong slide phải lấy **sau khi build và khởi động lại server**. Nếu chỉ dữ liệu endpoint mới nhưng file web cũ, KPI và trang thực thể sẽ lệch; build + prepare_web đồng bộ file local rồi chụp lại. Việc này chưa xuất bản lên Internet.

## 10. Sửa tài liệu, tạo slide và PDF

Nguồn nội dung tài liệu là các file Markdown trong docs. Lời slide nằm trong src/presentation_content.py; sơ đồ và bố cục trong src/make_slides_video.py. Font chung **Be Vietnam Pro**. Các công cụ PDF cần Pandoc, Tectonic và font; máy hiện tại đã có.

```bash
.venv/bin/python src/make_slides_video.py --slides-only
.venv/bin/python src/make_docs.py
.venv/bin/python src/prepare_web.py
```

make_docs chỉ render Markdown hiện có, không tự ghi đè nội dung đã sửa. Có thể render riêng: `.venv/bin/python src/make_docs.py docs/Bao_cao.md`. Huong_dan_thao_tac_chi_tiet cũng có thể render bằng make_manual.py. PDF slide hiện có 24 trang; PowerPoint có editable text/diagram và Speaker Notes. PDF slide hiện là bản vector xuất từ PPTX qua LibreOffice; thiếu LibreOffice thì trình tạo dùng bản raster dự phòng.

Nếu máy người đọc không có Be Vietnam Pro, cài font để PPTX giữ đúng bố cục hoặc dùng PDF. Điền nhóm/thành viên/lớp trên bìa. Không cần thêm ảnh stock; slide có sơ đồ mô hình và ảnh ứng dụng thật. Có thể thêm ảnh Protégé thật theo cảnh YC1 trong kịch bản nếu muốn.

## 11. Quay video 3–5 phút

Dùng Kich_ban_video.md/pdf: timeline 0:00–4:50, lời đọc từng cảnh, lệnh thật và kết quả mong đợi. Script_thuyet_trinh.md/pdf là lời nói 24 slide (~18–22 phút), không dùng nguyên để quay video 3–5 phút.

Quay thao tác Protégé/editor/Web/terminal. Giữ cảnh nguồn/RDF/giấy phép/sameAs; demo không chỉ bấm hai câu hỏi. Video_demo.mp4 hiện là bản demo 2.0 dài khoảng 4:50, ghi thao tác trình duyệt và kết quả lệnh thật, có lời tiếng Việt tổng hợp. Xem lại trước khi nộp; có thể thay bằng giọng của thành viên.

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 docs/Video_demo_2_0.mp4
```

## 12. Công bố và đối chiếu bản public

Lần kiểm tra mới 08/10: trang chủ, dataset, Turtle/JSON-LD, ontology, IRI Inception, mô tả RDF và giấy phép đều trả 200 không đăng nhập. RDF public có 19.339 triple, ontology 42 lớp; cả 4 graph RDF kiểm tra đều đẳng cấu với local. Kết luận dùng kết quả HTTP và graph, không chỉ trường audience/status trong JSON.

Sau khi nhóm xuất bản bản mới, kiểm tra từ phiên không đăng nhập: trang dataset, Turtle/JSON-LD, ontology, IRI và giấy phép. Tải RDF public về và so sánh **graph đẳng cấu**, không so byte vì thứ tự Turtle có thể khác. Lưu thời điểm, status, URL và kết quả thật trong evidence. Hosted có file tĩnh nên không mặc định có hành vi 303/content negotiation như Flask local.

Đổi tên miền cần dùng src/rebase.py rồi build/prepare_web; IRI trong dữ liệu/truy vấn/giao diện phải thống nhất. Site đã được triển khai lại qua quy trình hosting; trạng thái và ID phiên bản thật nằm trong publication.json. Khi sửa sau này, xuất bản và đối chiếu lại.

## 13. Chấm và kiểm tra sản phẩm nộp

Theo thang tự đề xuất chia đều 2 điểm mỗi YC: cả 5 YC đều đạt 2 điểm; tổng **10/10**. Đề gốc không có trọng số; đọc CHAM_DIEM.md để xem tiêu chí con và minh chứng. Đây không phải điểm chính thức của giảng viên.

Báo cáo tối đa 15 trang; slide 24 trang theo yêu cầu nhóm; video mới 180–300 giây. Có mã nguồn, RDF, OWL, dữ liệu gốc đủ, giấy phép, scripts và evidence. Không đóng gói .venv/Git/cache; kiểm tra file nguồn có thực sự trong ZIP vì mọi phản hồi gốc phải nằm trong bộ nộp; quy tắc gitignore làm mất nguồn đã được bỏ. `src/package.py` là tiện ích đóng gói, không thay các thiếu sót thành đạt.

## 14. Lỗi thường gặp

| Hiện tượng | Cách kiểm tra và xử lý |
|:--|:--|
| Port already in use | Dùng --port cổng trống và sửa URL/curl; không dừng tiến trình khác |
| Contribution trả 0 | Server giữ graph cũ; build/prepare_web và khởi động server mới |
| KPI/ảnh còn 15 lớp hoặc 964 links | File web cũ; build lại để đồng bộ statistics.json và RDF |
| validate FileNotFoundError | Thiếu snapshot; bổ sung bản gốc hoặc thu thập lại có mốc mới |
| Filmmaker/Actor trả 0 trên endpoint | Chạy terminal --reasoned; endpoint mặc định chỉ graph gốc |
| Câu hỏi chỉ 20 người | LIMIT 20; tổng Actor/Filmmaker nằm ở ontology_reasoning.json |
| Documentary ASK false | Mẫu chưa có phim tài liệu; không phải kết luận ngoài dataset |
| PDF lỗi công cụ/font | Kiểm tra Pandoc/Tectonic/Be Vietnam Pro, đọc build_*.log |
| PPTX chữ lệch máy khác | Cài Be Vietnam Pro hoặc trình chiếu PDF |
| Hosted có 200 nhưng số liệu cũ | Xuất bản đúng bản mới rồi đối chiếu graph |

## 15. Bổ sung ảnh Protégé vào bộ 24 slide

Có 11 khung P00–P10, có hướng dẫn ngay trên slide và Speaker Notes. Đọc Checklist_anh_Protege.md/pdf để chọn đúng file OWL, lớp/thuộc tính/cá thể và nội dung cần thấy. Khung chờ chưa phải ảnh thật. Có thể chèn trực tiếp vào PPTX hoặc lưu ảnh đúng stem ở evidence/protege (PNG/JPG/JPEG), chạy lại make_slides_video.py --slides-only. Ảnh tự thay khung chờ khi tạo lại. Bản ngắn 13 trang vẫn ở Slide_ngan_13.pptx/pdf.

**Cập nhật timestamp/reasoner:** dùng duy nhất Movie_Knowledge_Graph.owl cho graph đầy đủ. HermiT/Pellet đã chạy; xem Ket_qua_reasoner.pdf. Video_demo.mp4 giữ nguyên theo yêu cầu nhóm; timestamp trong dữ liệu mới giảm đến mili giây, nội dung phim/quan hệ giữ nguyên, đã kiểm tra ở video_dataset_compatibility.json. Video chưa thể hiện kết quả reasoner mới và vẫn nhắc bộ slide ngắn 13 trang.

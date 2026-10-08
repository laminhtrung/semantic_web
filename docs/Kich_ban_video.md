---
title: "MovieLOD: kịch bản quay demo 4 phút 50 giây"
date: "MovieLOD 2.0 · Đối chiếu ngày 08/10/2026"
---

## Mục tiêu và thời lượng

**Một video thao tác thật 4 phút 50 giây**, có lời đọc tiếng Việt; cho thấy đủ YC1–YC5. Video có 10 cảnh tương tác và minh chứng; không dùng bộ slide thay cho demo. Có thể dựng cắt cảnh giữa Protégé, trình soạn thảo, Web và terminal. Các lệnh được chạy thật; giữ lại đầu vào và kết quả trong khung hình. Video_demo.mp4 hiện đã được tạo từ ghi thao tác app thật và kết quả lệnh thực thi, có giọng tiếng Việt tổng hợp Linh; không phải ghi desktop Protégé hay lời của sinh viên.

## Chuẩn bị trước khi bấm quay

- Mở `ontology/Movie_Ontology.owl` bằng Protégé; tab Classes có Film/Person/Contribution, tab Object properties có contributionBy/contributionTo/hasRole.
- Mở `data/raw/snapshots.json`, `src/collect.py`, `data/processed/movies.ttl`, `LICENSE-DATA.txt` trong editor; tăng font khoảng 18–22.
- Chạy server ở terminal A, mở `http://127.0.0.1:8000`; nếu dùng cổng khác thay toàn bộ lệnh curl. Chạy lại server sau build để không giữ graph cũ trong RAM.
- Terminal B ở thư mục gốc, chuẩn bị lệnh bên dưới. `inferred_classes.ttl` đã có; chạy lại reason.py trước buổi quay nếu cần cập nhật. Không chờ reasoner chạy trong khung 3–5 phút.
- Đặt trình duyệt 125–150% tùy màn hình, quay 1920×1080 hoặc 1280×720, 30 fps; bật micro và tắt thông báo. Thử ghi 10 giây để kiểm tra tiếng.
- Chọn câu hỏi bằng **nhãn**, không dựa số thứ tự option. Có 14 mẫu trực tiếp trên Web, 24 file truy vấn tổng cộng.
- Nếu không lấy được hình Protégé, chèn sơ đồ slide 4–5 kèm ghi rõ “sơ đồ mô hình”; vẫn quay màn hình file OWL và các ràng buộc thật.

\newpage

## Timeline cố định

| Thời gian | Cảnh và thao tác | Kết quả phải thấy | Yêu cầu |
|:--|:--|:--|:--|
| 0:00–0:15 | Trang chủ, rê vào SPARQL và danh sách phim | Tên MovieLOD, ô truy vấn, dữ liệu phim | Giới thiệu |
| 0:15–0:50 | Trang ontology / trình xem minh chứng OWL: Film, Person, Contribution và ràng buộc | IRI DBpedia, đúng 1 người/phim/vai trò, 4 vai trò | YC1 |
| 0:50–1:15 | Trình xem collect.py/snapshots.json và một phản hồi gốc | Sitelink, URL, retrieved_at, SHA-256 | YC2 |
| 1:15–1:45 | Mở movies.ttl, giấy phép; mở IRI Inception và link tải RDF | Triple, datatype, HTTP IRI và giấy phép | YC3 |
| 1:45–2:10 | Web: External links for each film và ASK Wikidata | Wikidata + DBpedia của Inception, ASK True | YC4 |
| 2:10–2:50 | Web: Inception; phim Nolan; đóng góp Inception | 2010/148/Nolan; 8 dòng; 25 đóng góp/4 vai trò | YC5 |
| 2:50–3:15 | Web: công ty Inception; giải Godfather; Download results | 4 công ty; 7 giải; file kết quả được tải | YC2/YC5 |
| 3:15–3:45 | Terminal: curl POST và query.py; Accept Turtle | JSON có Nolan; 303 theo bằng -L rồi Turtle | YC3/YC5 |
| 3:45–4:25 | Terminal: kiểu Nolan gốc; cùng câu với --reasoned; ActionFilm | 1 kiểu gốc → 3 kiểu khi nạp phân loại; 12 ActionFilm | YC1/YC5 |
| 4:25–4:50 | Hiện validation, test, kiểm tra public và kết luận | 76 hash khớp, 13 test pass, public khớp; 10/10 tự đánh giá | Tổng kết |

## Lời đọc từng cảnh

### 0:00–0:15 — MovieLOD · dữ liệu điện ảnh liên kết

Đây là Movie L O D, ứng dụng dữ liệu phim liên kết. Nhóm sẽ minh họa năm yêu cầu bằng ontology, dữ liệu thật, R D F, liên kết bên ngoài và các truy vấn chạy trực tiếp.

### 0:15–0:50 — YC1 · Ontology và mô hình Contribution

Ontology có bốn mươi hai lớp và dùng trực tiếp Film, Person, Country của DBpedia. Mô hình Contribution ghi một người giữ một vai trò trong một phim. Ba quan hệ contribution By, contribution To và has Role có ràng buộc đúng một giá trị. Bốn vai trò là đạo diễn, diễn viên, biên kịch và nhà sản xuất. Một người có thể giữ nhiều vai trò bằng các bản ghi riêng. Các lớp Actor và Filmmaker được phân loại từ định nghĩa thay vì nhập sẵn.

### 0:50–1:15 — YC2 · Phản hồi nguồn thật và SHA-256

Mã thu thập lấy Wikidata và DBpedia, xác định phim qua sitelink Wikipedia chính xác. Trên màn hình là metadata và một phản hồi nguồn thật, có địa chỉ, thời điểm và mã băm. Các phản hồi được giữ để kiểm tra và chạy lại. SHA hai trăm năm mươi sáu kiểm tra toàn vẹn nội dung, không tự chứng minh mọi phát biểu ngoài đời đều đúng.

### 1:15–1:45 — YC3 · RDF, HTTP IRI và giấy phép mở

Dữ liệu được chuyển thành các bộ ba: chủ thể, quan hệ và đối tượng hoặc giá trị. Inception có đạo diễn Christopher Nolan, năm hai nghìn mười và thời lượng một trăm bốn mươi tám phút. Định danh H T T P mở được trang mô tả và bản R D F để tải. Dữ liệu có Turtle, JSON L D và giấy phép C C BY S A bốn chấm không. Phần công bố được đối chiếu với bản cục bộ trong biên bản kiểm tra.

### 1:45–2:10 — YC4 · sameAs đến Wikidata và DBpedia

Inception nối tới Wikidata và DBpedia bằng owl same As. Hai định danh này cùng chỉ một thực thể. Tổng dataset có một nghìn bảy trăm hai mươi bảy liên kết; bảng theo phim có năm mươi tám dòng. Câu ASK trả True cho liên kết Wikidata. Quan hệ nguồn dữ liệu được ghi riêng và không thay thế same As.

### 2:10–2:50 — YC5 · Inception, phim Nolan và các vai trò

Truy vấn Inception trả năm phát hành, thời lượng và tên đạo diễn. Đổi câu hỏi sang phim do Nolan đạo diễn, chúng ta có tám dòng trong bộ dữ liệu. Truy vấn đóng góp Inception trả hai mươi lăm bản ghi, có các vai trò Actor, Director, Writer và Producer. Nolan xuất hiện ở những công việc khác nhau trong cùng phim. Các kết quả được S P A R Q L tính từ đồ thị. Người dùng có thể sửa câu hỏi rồi bấm Run query để chạy lại.

### 2:50–3:15 — YC5 · Công ty, giải thưởng và tải kết quả

Ứng dụng còn có câu hỏi về công ty sản xuất, giải thưởng và nguồn. Inception có bốn công ty trong dữ liệu. The Godfather có bảy giải được ghi nhận. Nút Download results tải kết quả đang hiển thị. Có thể dùng dữ liệu này để kiểm tra lại bằng một công cụ khác.

### 3:15–3:45 — YC5 · Kết quả thật từ endpoint và terminal

Đây là kết quả các lệnh đã chạy thật. P O S T tới endpoint trả J S O N có Inception và Christopher Nolan. Cùng câu hỏi chạy được bằng file S P A R Q L ở terminal. Khi gửi Accept text turtle tới định danh phim cục bộ, server trả chuyển hướng ba trăm linh ba; curl trừ L theo chuyển hướng và nhận mô tả R D F. Giao diện, endpoint và terminal dùng cùng dữ liệu khai báo.

### 3:45–4:25 — YC1 + YC5 · Kiểu gốc và kiểu được phân loại

Trên dữ liệu gốc, Nolan chỉ được khai báo là Person. Chạy cùng câu với reasoned, kết quả bổ sung Filmmaker và AwardWinner từ file phân loại. Contribution có DirectorRole được phân loại DirectingContribution; người có đóng góp đó được phân loại Filmmaker. Có mười hai ActionFilm trong mẫu. Mười hai lớp dùng luật O W L R L. Hai lớp có ngưỡng số lượng dùng truy vấn đếm I R I bổ sung; phần này chưa phải bằng chứng phân loại O W L D L đầy đủ.

### 4:25–4:50 — Đối chiếu minh chứng và bộ bài nộp

Bài có ontology, dữ liệu thật, R D F, liên kết và ba cách truy vấn. Các kiểm tra nguồn, truy vấn, test và bản công khai được lưu trong evidence để đối chiếu. Báo cáo, mười ba slide và video này cùng dùng mô hình hai chấm không. Bảng tự chấm ghi điểm theo minh chứng, không phải điểm chính thức của giảng viên.

## Lệnh chạy thật trong cảnh terminal

**Server ở terminal A:**

```bash
.venv/bin/python src/server.py
```

**Terminal B — endpoint và terminal (3:15–3:45):**

```bash
curl -s -X POST http://127.0.0.1:8000/sparql \
  -H 'Content-Type: application/sparql-query' \
  --data-binary @queries/02_inception.rq | .venv/bin/python -m json.tool
.venv/bin/python src/query.py queries/02_inception.rq
curl -s -L -H 'Accept: text/turtle' \
  http://127.0.0.1:8000/resource/film-Q25188
```

Muốn hiện rõ 303 trước khi theo redirect: dùng `curl -s -D - -o /dev/null -H 'Accept: text/turtle' http://127.0.0.1:8000/resource/film-Q25188`.

**Kiểu Nolan và phân loại (3:45–4:25):**

```bash
.venv/bin/python src/query.py queries/24_nolan_asserted_types_only.rq
.venv/bin/python src/query.py queries/24_nolan_asserted_types_only.rq --reasoned
.venv/bin/python src/query.py queries/19_inferred_action_films.rq --reasoned
```

Câu 24 chỉ là “kiểu khai báo” khi chạy không --reasoned: **1 kiểu Person**. Với --reasoned, cùng truy vấn hiển thị **3 kiểu** từ dữ liệu đã lưu: Person, Filmmaker, AwardWinner. `query.py` nạp kết quả phân loại đã có, không tính suy luận trong thời gian quay.

## Đối chiếu để không bỏ sót yêu cầu

| YC | Phải có hình bằng chứng trong video |
|:--|:--|
| YC1 | OWL có lớp/ràng buộc và đối chiếu kiểu gốc–phân loại |
| YC2 | Mã thu thập, danh mục nguồn và một phản hồi gốc còn có |
| YC3 | Triple RDF, HTTP IRI, giấy phép, tải RDF; minh chứng public khớp local |
| YC4 | sameAs tới Wikidata/DBpedia và ASK True |
| YC5 | Web SELECT, endpoint POST, terminal, file kết quả tải |

## Xử lý khi quay và kiểm tra bản xuất

Nếu câu hỏi Contribution trả 0, kiểm tra server có còn chạy graph cũ trong RAM không; chạy lại server trên cổng trống. Nếu truy vấn Actor/Filmmaker trên Web trả 0, chuyển sang terminal với --reasoned. Nếu trình duyệt đợi engine, dựng cắt phần đợi, giữ nguyên thao tác và kết quả. Không dựng kết quả giả. Nếu quá 5 phút, giảm thời gian rê chuột và cắt khoảng im lặng, giữ các cảnh YC1–YC5. Nếu thiếu hình, ghi chú nơi cần bổ sung và dùng ảnh thật trong `evidence/screenshots/`.

Xuất MP4 H.264 + AAC; thời lượng 180–300 giây; xem lại một lượt để bảo đảm chữ đọc được, lời và thao tác khớp, có đủ 5 YC. Bản hiện có là `Video_demo.mp4`; đã kiểm tra thời lượng và khung hình của bản mới.

## Tạo lại video tự động từ thao tác thật

Bản đã tạo dùng Chromium ghi thao tác Web và trang xem nguồn/kết quả lệnh thực thi thật; không ghi desktop Protégé. Giọng Linh tổng hợp, không phải lời sinh viên. Cần macOS, Playwright (kèm FFmpeg của Playwright), FFmpeg hệ thống và dữ liệu/evidence đã kiểm tra.

Terminal A:

```bash
.venv/bin/python src/demo_server.py --port 8002
```

Terminal B:

```bash
.venv/bin/python -m pip install playwright
.venv/bin/python -m playwright install ffmpeg
.venv/bin/python src/record_demo.py --port 8002
```

Script chỉ ghi cảnh kết luận khi kiểm tra public đã khớp. Chưa thay giọng của thành viên; có thể dùng lời bên trên để ghi giọng riêng.

**Bộ slide cập nhật:** bản đầy đủ 24 trang có script riêng; video hiện có vẫn minh họa app và nhắc bộ ngắn 13 trang được giữ ở Slide_ngan_13.pptx/pdf. Không thay đổi dữ liệu hoặc nội dung demo khi mở rộng slide.

**Cập nhật timestamp/reasoner:** dùng duy nhất Movie_Knowledge_Graph.owl cho graph đầy đủ. HermiT/Pellet đã chạy; xem Ket_qua_reasoner.pdf. Video_demo.mp4 giữ nguyên theo yêu cầu nhóm; timestamp trong dữ liệu mới giảm đến mili giây, nội dung phim/quan hệ giữ nguyên, đã kiểm tra ở video_dataset_compatibility.json. Video chưa thể hiện kết quả reasoner mới và vẫn nhắc bộ slide ngắn 13 trang.

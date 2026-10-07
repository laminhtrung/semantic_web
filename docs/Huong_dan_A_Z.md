---
title: "MovieLOD: làm và đọc bài từ A đến Z"
date: "Hướng dẫn ngắn • 06/10/2026"
---

## A. Bạn có gì trong thư mục này?

Đây là **bản độc lập**, không cần mở file OWL mở rộng cũ để chạy. Bài có **30 phim, 15 lớp**, nguồn thật và một ứng dụng truy vấn.

| Thư mục / file | Để làm gì? |
|:--|:--|
| `README.md` | Điểm bắt đầu, các lệnh chạy và trạng thái xuất bản. |
| `ontology/` | Mô hình OWL và dữ liệu RDF. |
| `data/raw/` | Phản hồi gốc; metadata ghi URL, ngày lấy và SHA-256. |
| `data/processed/` | Dữ liệu đã chuẩn hóa: Turtle, JSON-LD, CSV. |
| `src/` | Mã thu thập, chuyển đổi, kiểm tra, server và terminal. |
| `queries/` | 8 câu hỏi SPARQL mẫu, có thể chỉnh sửa. |
| `web/dist/` | Giao diện và dữ liệu phục vụ trên Web. |
| `evidence/` | Số liệu, kết quả kiểm tra, ảnh và biên bản thực thi. |
| `docs/` | Báo cáo, hướng dẫn, slide và video. |

**Bốn từ để nhớ:** ontology = mô hình; RDF = câu dữ liệu; IRI = định danh; SPARQL = ngôn ngữ hỏi dữ liệu. Đọc ví dụ Inception trước, rồi mới xem mã nguồn.

## B. Chạy ứng dụng ngay

Mở terminal trong thư mục này. Dùng Python 3.9 trở lên.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/server.py
```

Mở **http://127.0.0.1:8000**. Có sẵn dữ liệu nên không cần tải lại. Trên macOS, `start.command` làm các bước khởi động này. Dừng server bằng Ctrl+C.

Trong giao diện: chọn câu hỏi Inception → bấm **Run query** → đọc bảng → mở một phim để thấy thông tin và nguồn → tải Turtle nếu muốn xem RDF. Bản hosted: [MovieLOD](https://movie-lod-semantic-web.laminhtrung2001.chatgpt.site/).

**Xuất bản:** Đã xuất bản công khai; người có URL truy cập được dữ liệu và giao diện. Bản hosted chưa có ontology 1.1.0 với sáu defined class; cần xuất bản lại để đồng bộ.

\newpage

## C. Đọc ontology — YC1

Mở `ontology/Movie_Ontology.owl` bằng Protégé để xem **mô hình**. Mở `ontology/Movie_Knowledge_Graph.owl` để xem **cả mô hình và dữ liệu**.

| Tên / từ tiếng Anh | Dịch | Hiểu bằng ví dụ |
|:--|:--|:--|
| dbo:Film / dbo:Person | Phim / người | Lớp DBpedia, dùng cho Inception / Christopher Nolan. |
| ex:Genre / dbo:Country / ex:Language | Thể loại / quốc gia / ngôn ngữ | Country dùng lớp DBpedia; Genre và Language thuộc mô hình của bài. |
| Credit / ContributionRole | Đóng góp / vai trò | Nolan làm đạo diễn trong Inception. |
| SourceSnapshot / Dataset | Bản ghi nguồn / bộ dữ liệu | Thông tin truy lại được; dữ liệu được mô tả và tải về. |
| Object property / Data property | Quan hệ / thuộc tính giá trị | Phim → đạo diễn; phim → năm. |
| Exactly 1 / Inverse | Đúng một / quan hệ ngược | Một credit có đúng một người; director ↔ directed. |

**Đi từ một ví dụ:** Film Inception → `hasCredit` → credit → `participant` Nolan + `role` DirectorRole + `sourceSnapshot` nguồn. Đây là cách lưu một người làm nhiều vai trò mà không lẫn các đóng góp.

## D. Thu thập nguồn thật — YC2

```bash
.venv/bin/python src/collect.py
```

Mã chọn phim theo `config.json`; tải Wikidata theo tiêu đề Wikipedia tiếng Anh; tải dữ liệu các người/thể loại/quốc gia/ngôn ngữ liên quan; kiểm tra chủ thể Film của DBpedia; lưu phản hồi gốc.

**Mỗi nguồn có:** URL = địa chỉ; `retrieved_at` = thời điểm lấy; SHA-256 = dấu vân tay nội dung. Mở `data/raw/snapshots.json` để tra từng phản hồi. Mã dùng cache khi hash vẫn đúng; thêm `--refresh` để tải lại từ Internet.

**Danh tính được kiểm tra:** QID Wikidata được giải quyết từ sitelink đúng tiêu đề; DBpedia dùng cùng tiêu đề và type Film. Không nối bằng cách đoán từ tên gần giống. Xem lỗi hoặc phản hồi bị bỏ ở `evidence/collection.json`.

\newpage

## E. Chuyển thành RDF — YC3

```bash
.venv/bin/python src/build.py
```

Mã dùng 15 lớp (3 lớp DBpedia và 12 lớp của bài), trong đó 6 defined class dùng giao/hợp và restriction tồn tại; xem `Mo_ta_ontology.md` và chạy `src/reason.py` để kiểm tra phân loại; biến thông tin đã thu thập thành đồ thị RDF; tạo định danh từ QID; đổi thời lượng về phút; thêm nguồn; xuất Turtle, JSON-LD, CSV và OWL.

| Câu viết gọn | Dịch |
|:--|:--|
| `film-Q25188 a dbo:Film` | Đối tượng này là phim, dùng trực tiếp lớp của DBpedia. |
| `film-Q25188 ex:title "Inception"` | Phim có tên Inception. |
| `film-Q25188 dbo:director person-Q25191` | Nolan là đạo diễn của phim. |
| `credit ex:role ex:DirectorRole` | Bản ghi đóng góp này có vai trò đạo diễn. |

`a` viết tắt `rdf:type`; `ex:` viết tắt từ vựng của bài; `dbo:` viết tắt DBpedia ontology. `dbo:Film`, `dbo:Person`, `dbo:Country` là các lớp tái sử dụng trực tiếp. Các tên `film-...` là phần cuối IRI đầy đủ.

**Phần công bố:** Web có trang IRI cho từng thực thể, RDF của thực thể, JSON-LD và các file tải. Giấy phép được ghi cả trong RDF và `LICENSE-DATA.txt`. Muốn đủ Open Data, audience phải công khai; chạy trên localhost chỉ là minh chứng chạy ứng dụng tại máy.

## F. Liên kết ngoài — YC4

`owl:sameAs` nghĩa là hai IRI chỉ cùng thực thể. Inception có QID **Q25188**; Nolan có QID **Q25191**. Mỗi thực thể được tái dùng giữa các phim, không tạo một Nolan khác cho từng phim.

Mở `evidence/link_audit.json` để xem IRI nội bộ, IRI ngoài và phương pháp nối. Có **964 liên kết** trong lần tạo dữ liệu này. `sameAs` dùng cho danh tính; `wasDerivedFrom` dùng cho nguồn.

## G. Kiểm tra trước khi demo

```bash
.venv/bin/python src/validate.py
.venv/bin/python -m pytest -q
```

Python kiểm tra phim có tên, nguồn, liên kết; credit có đúng phim–người–vai trò; bản ghi nguồn có URL, thời điểm, hash. Mã kiểm tra nằm ở `src/validate.py`. Test còn thử truy vấn, chuyển hướng RDF, câu truy vấn sai và suy luận quan hệ ngược. Kết quả nằm trong `evidence/`.

\newpage

## H. Truy vấn theo ba cách — YC5

**1. Giao diện:** mở Web, chọn câu hỏi mẫu, chỉnh SPARQL nếu cần, bấm chạy, đọc bảng và tải kết quả. Bản hosted dùng Comunica để hỏi file RDF trong trình duyệt. Bản cục bộ dùng endpoint.

**2. Terminal:**

```bash
.venv/bin/python src/query.py queries/02_inception.rq
```

**3. Endpoint:** chạy server, rồi mở terminal khác:

```bash
curl -X POST http://127.0.0.1:8000/sparql \
  -H 'Content-Type: application/sparql-query' \
  --data-binary @queries/02_inception.rq
```

| Truy vấn | Câu hỏi dễ hiểu |
|:--|:--|
| `01_films.rq` | Bộ dữ liệu có những phim nào? |
| `02_inception.rq` | Inception ra năm nào, dài bao lâu, ai đạo diễn? |
| `03_nolan.rq` | Có những phim nào do Nolan đạo diễn? |
| `04_credits.rq` | Ai đóng góp vai trò gì trong Inception? |
| `05_external_links.rq` | Phim nối tới định danh ngoài nào? |
| `06_genres.rq` | Mỗi thể loại có bao nhiêu phim trong mẫu? |
| `07_source.rq` | Thông tin Inception được lấy từ đâu, khi nào? |
| `08_ask.rq` | Inception có đúng liên kết Wikidata không? |

`SELECT` = lấy bảng; `WHERE` = mẫu dữ liệu; `OPTIONAL` = thông tin có thì lấy; `FILTER` = điều kiện; `COUNT` = đếm; `ASK` = đúng/sai. Truy vấn mặc định đọc dữ liệu gốc, không tự bật suy luận.

## I. Gói nộp và những điều cần nhớ

**Nộp:** mã và dữ liệu trong thư mục này; `docs/Bao_cao.pdf` (không quá 15 trang); `docs/Slide.pptx`; `docs/Video_demo.mp4` (3–5 phút). Video có lời đọc tiếng Việt tổng hợp, minh họa bằng dữ liệu và ảnh ứng dụng thật; có kịch bản để tự thuyết trình lại.

**Trình bày theo 5 ý:** mô hình 15 lớp (9 nền + 6 suy luận; xem Mo_ta_ontology.md) → nguồn thật có hash → RDF và IRI → liên kết Wikidata/DBpedia → truy vấn ra kết quả. Không cần giải thích các mô-đun giải thưởng hoặc streaming vì bản này không đưa chúng vào phạm vi.

**Nếu lỗi:** kiểm tra đã cài requirements; cổng 8000 chưa bị dùng; dữ liệu đã build. Dùng `--port 8001` nếu cần đổi cổng. API nguồn cần Internet khi thu thập mới; phản hồi cũ được giữ để chạy lại. Trạng thái công khai được ghi đúng trong `evidence/publication.json`.

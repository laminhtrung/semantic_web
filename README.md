# MovieLOD — bản bài làm độc lập từ A đến Z

**Bắt đầu:** đọc [hướng dẫn A–Z](docs/Huong_dan_A_Z.pdf), rồi chạy ứng dụng. Bản này dùng mô hình **15 lớp**, dữ liệu thật của **30 phim**, có nguồn, chuyển đổi RDF, **964 liên kết ngoài**, giao diện SPARQL, endpoint và terminal.

**Ngôn ngữ ứng dụng:** giao diện, truy vấn mẫu, tên biến SPARQL, nhãn ontology/vai trò và thông báo endpoint dùng tiếng Anh. Tài liệu hướng dẫn học phần được viết bằng tiếng Việt.

## Chạy ngay

Mở terminal trong thư mục này:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/server.py
```

Mở **http://127.0.0.1:8000**. Dữ liệu đã có sẵn. Trên macOS có thể chạy [start.command](start.command). Dừng server bằng Ctrl+C. Nếu cổng đã được dùng: `src/server.py --port 8001`.

**Bản hosted:** [MovieLOD](https://movie-lod-semantic-web.laminhtrung2001.chatgpt.site). Trạng thái và audience thực tế nằm ở [publication.json](evidence/publication.json). Site đã được cập nhật công khai với giao diện và truy vấn tiếng Anh, cùng dữ liệu dùng trực tiếp các lớp DBpedia. Trạng thái triển khai mới nằm trong `publication.json`; `publication_checks.json` ghi lại lần đối chiếu HTTP trước đó.

## Sản phẩm nộp

- [Báo cáo](docs/Bao_cao.pdf): đối chiếu đúng 5 tiêu chí; không quá 15 trang.
- [Slide PowerPoint](docs/Slide.pptx) và [PDF slide](docs/Slide.pdf).
- [Video demo](docs/Video_demo.mp4): 3–5 phút, có lời đọc tiếng Việt tổng hợp và hình ứng dụng thật.
- [Hướng dẫn A–Z](docs/Huong_dan_A_Z.pdf); [kịch bản thuyết trình](docs/Kich_ban_video.md).
- [Hướng dẫn thao tác chi tiết từ đầu đến cuối](docs/Huong_dan_thao_tac_chi_tiet.pdf): thao tác, lệnh chạy, kết quả cần thấy và xử lý lỗi; có [bản Markdown](docs/Huong_dan_thao_tac_chi_tiet.md).
- Mã nguồn, dữ liệu gốc, dữ liệu RDF và biên bản kiểm tra trong thư mục này.

## 5 yêu cầu tương ứng với phần nào?

| Yêu cầu trong đề | Phần đã triển khai | Minh chứng |
|:--|:--|:--|
| YC1 — Define an ontology: định nghĩa mô hình | 15 lớp; tái sử dụng trực tiếp 3 lớp DBpedia; quan hệ, cardinality, inverse, disjointness và 6 defined class dùng giao/hợp. | `ontology/Movie_Ontology.owl`; `src/build.py`; test truy vấn DBpedia và suy luận. |
| YC2 — Collect data: thu thập dữ liệu | Tải Wikidata/DBpedia, xác định danh tính chính xác, lưu phản hồi gốc và hash. | `src/collect.py`; `data/raw/snapshots.json`; `evidence/collection.json`. |
| YC3 — Transform to 4*: RDF và công bố mở | Turtle, JSON-LD, HTTP IRI, giấy phép; trang mô tả từng thực thể và tải RDF. | `data/processed/`; `LICENSE-DATA.txt`; Web; `publication.json`. |
| YC4 — Link to 5*: liên kết ngoài | 936 liên kết Wikidata và 28 DBpedia, ghi phương pháp nối. | `evidence/link_audit.json`; truy vấn 05. |
| YC5 — SPARQL interface: truy vấn | Web, endpoint GET/POST cục bộ, terminal; SELECT/ASK/CONSTRUCT. | `src/server.py`; `src/query.py`; `queries/`; ảnh và video demo. |

**Điều kiện xuất bản:** chạy cục bộ hay có bản hosted riêng tư chưa đủ “Open Data trên Web”. Cần xác nhận audience `public`, status `succeeded` và bản công khai khớp phiên bản dữ liệu nộp. `local_changes_pending_publication` ghi nhận khi bản hosted còn dùng dữ liệu trước lần sửa mới.

### Tái sử dụng các lớp DBpedia

| Lớp dùng trực tiếp | Dữ liệu trong bài | Định nghĩa nguồn |
|:--|:--|:--|
| `dbo:Film` | 30 phim | [DBpedia Film](https://dbpedia.org/ontology/Film) |
| `dbo:Person` | 851 người tham gia | [DBpedia Person](https://dbpedia.org/ontology/Person) |
| `dbo:Country` | 11 quốc gia | [DBpedia Country](https://dbpedia.org/ontology/Country) |

Các IRI lớp này được dùng trực tiếp trong `rdf:type`, domain/range, ràng buộc OWL và truy vấn mẫu. Ví dụ Inception có kiểu `dbo:Film`; Nolan có kiểu `dbo:Person`. Truy vấn `?film a dbo:Film` chạy được trên dữ liệu đã lưu mà không cần bật suy luận.

Mô hình có **42 lớp có tên** (ontology 2.0.0): 3 lớp DBpedia tái dùng, phần còn lại thuộc namespace của bài — theo cây `CreativeWork`/`Agent`/`Contribution`/`Genre`/`Award`/`Organization`, trong đó **14 lớp là suy luận** (`Actor`, `Filmmaker`, `AwardWinner`, `ActionFilm`, `MultiGenreFilm`, `FilmStudio`...). Chi tiết đầy đủ ở [Ontology_Redesign.md](docs/Ontology_Redesign.md).

### Phân loại suy luận và ý nghĩa lớp

14 lớp suy luận (`Actor`, `Filmmaker`, `AwardWinner`, `ActingContribution`/`DirectingContribution`/`WritingContribution`/`ProducingContribution`, `ActionFilm`/`ComedyFilm`/`DramaFilm`/`ScienceFictionFilm`/`MultiGenreFilm`/`AwardWinningFilm`, `FilmStudio`) được định nghĩa bằng `equivalentClass`, `intersectionOf`, `unionOf`, `someValuesFrom`, `hasValue` và `minQualifiedCardinality`. Xem [mô tả ontology và câu hỏi bảo vệ](docs/Mo_ta_ontology.md) và [bảng chi tiết đầy đủ](docs/Ontology_Redesign.md). Kết quả chạy suy luận ở [ontology_reasoning.json](evidence/ontology_reasoning.json); các kiểu suy ra được lưu riêng trong `data/processed/inferred_classes.ttl`. Endpoint mặc định vẫn truy vấn dữ liệu khai báo — chạy `python src/query.py <file> --reasoned` để truy vấn trên các lớp suy luận.

Bản hosted cần xuất bản lại để đồng bộ ontology 2.0.0 (bản local hiện có 42 lớp, nhiều hơn bản hosted). PDF báo cáo, slide và video hiện vẫn mô tả ontology 1.1.0 trước khi mở rộng Contribution/Award/Organization.

## Làm lại toàn bộ quy trình

```bash
.venv/bin/python src/collect.py
.venv/bin/python src/build.py
.venv/bin/python src/prepare_web.py
.venv/bin/python src/validate.py
.venv/bin/python src/reason.py
.venv/bin/python -m pytest -q
```

Hoặc `make all` sau khi tạo `.venv`. Thu thập mặc định dùng cache đã kiểm tra SHA-256; `collect.py --refresh` tải lại qua Internet. Không tự điền thông tin thiếu. `quality_issues.json` ghi các giá trị nguồn cần chú ý.

**Truy vấn bằng terminal:**

```bash
.venv/bin/python src/query.py queries/02_inception.rq
```

**Gọi endpoint:** khởi động server, rồi:

```bash
curl -X POST http://127.0.0.1:8000/sparql \
  -H 'Content-Type: application/sparql-query' \
  --data-binary @queries/02_inception.rq
```

**Tra cứu một IRI bằng RDF:**

```bash
curl -L -H 'Accept: text/turtle' \
  http://127.0.0.1:8000/resource/film-Q25188
```

## Cách đọc các file

| Nơi lưu | Ý nghĩa |
|:--|:--|
| `config.json` | URL định danh và danh sách phim đã chọn. |
| `ontology/Movie_Ontology.owl` | Chỉ mô hình: mở bằng Protégé để xem lớp/quy tắc. |
| `ontology/Movie_Knowledge_Graph.owl` | Cả mô hình và dữ liệu: mở bằng Protégé để xem cá thể. |
| `data/raw/` | Phản hồi thật, URL nguồn, thời điểm lấy và SHA-256. |
| `data/processed/` | Dữ liệu chuẩn hóa, tách riêng khỏi nguồn gốc. |
| `queries/` | 24 câu hỏi SPARQL mẫu (3 nhóm: trực tiếp, theo hierarchy, cần suy luận) theo thứ tự học/demo. |
| `src/` | Mã nguồn toàn quy trình, có thể chạy từng bước. |
| `web/dist/` | Web, thư viện truy vấn tự chứa, trang RDF và mô tả tài nguyên. |
| `evidence/` | Số liệu, kiểm tra dữ liệu bằng Python, kiểm tra nguồn, kết quả truy vấn, ảnh. |
| `docs/` | Các tài liệu để đọc, thuyết trình và nộp. |

**Giấy phép:** dữ liệu CC BY-SA 4.0, ghi công Wikidata/DBpedia/Wikipedia; mã ứng dụng MIT. Thư viện Comunica giữ giấy phép riêng.

## Kiểm tra giao diện và tạo lại tài liệu

Ứng dụng chạy được chỉ với Python và các dependencies. PDF/slide/video đã được tạo sẵn. Để tạo lại PDF: cần Pandoc, Tectonic và font Be Vietnam Pro; chạy `.venv/bin/python src/make_docs.py`.

Kiểm tra trình duyệt là bước bổ sung: cài Playwright và Chromium, chạy server, rồi `python src/browser_check.py`. Script dùng Chrome đã cài trên macOS hoặc Chromium của Playwright. Không cần bước này để dùng ứng dụng.

Tạo lại hướng dẫn thao tác chi tiết: chỉnh `docs/Huong_dan_thao_tac_chi_tiet.md`, rồi chạy `.venv/bin/python src/make_manual.py`; dùng cùng Pandoc, Tectonic và font như báo cáo.

Video được tạo từ slide và ảnh ứng dụng thật; giọng tiếng Việt Linh của macOS. Mã tạo lại nằm ở `src/make_slides_video.py`, cần FFmpeg và lệnh `say` trên macOS.

**Đổi địa chỉ xuất bản:** chạy `src/rebase.py https://ten-mien-moi`, sau đó build, prepare_web, validate và tạo lại tài liệu. Mã đồng bộ namespace trong dữ liệu, truy vấn và giao diện. Không sửa từng IRI bằng tay.

**Gói lại để nộp:** `.venv/bin/python src/package.py` kiểm tra RDF, số trang báo cáo, slide, thời lượng video và tạo ZIP bên cạnh thư mục này; loại `.venv`, Git và file tạm.

Nguồn đối chiếu: [W3C Linked Data](https://www.w3.org/DesignIssues/LinkedData.html), [W3C SPARQL 1.1](https://www.w3.org/TR/sparql11-query/), [Wikidata licensing](https://www.wikidata.org/wiki/Wikidata:Licensing), [Comunica](https://comunica.dev/docs/query/getting_started/query_browser_app/).

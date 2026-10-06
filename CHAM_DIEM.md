# Chấm điểm MovieLOD theo yêu cầu đề bài

Ngày kiểm tra: **06/10/2026** (giờ Việt Nam).

**Cập nhật sau lần chấm ban đầu:** repo đã chuyển sang tái sử dụng trực tiếp 3 lớp DBpedia; xem mục 10. Site hiện đã public và dữ liệu trả HTTP 200, nhưng bản hosted còn dùng kiểu lớp trước lần sửa. Bảng điểm và số liệu ở mục 1–9 bên dưới là kết quả của lần chấm ban đầu, khi Site còn riêng tư; không dùng trạng thái HTTP 401 lịch sử để mô tả Site hiện tại. Cần xuất bản bản sửa và đối chiếu dữ liệu hosted trước khi chấm lại phiên bản mới.

**Điểm đề xuất: 9,0/10.** YC1, YC2 và YC5 đạt đầy đủ trong phạm vi đề; YC3 và YC4 đạt phần triển khai kỹ thuật nhưng chưa hoàn tất điều kiện công bố dữ liệu mở. Slide, báo cáo và thời lượng video đáp ứng các điều kiện sản phẩm nộp.

Đây là điểm tự đánh giá có dẫn chứng, **không phải điểm chính thức của giảng viên**. [Ảnh đề gốc](<Screenshot 2026-10-05 at 14.39.32.png>) ghi 5 yêu cầu nhưng không quy định trọng số. File này đề xuất chia đều **2 điểm/yêu cầu**, mỗi yêu cầu gồm 4 mục kiểm tra, mỗi mục 0,5 điểm. Sản phẩm nộp được kiểm tra riêng, không cộng thêm ngoài thang 10.

## 1. Bảng điểm và nơi tìm minh chứng

| Mã | Yêu cầu nguyên văn trong đề | Điểm tối đa | Điểm đề xuất | Kết luận | Phần trình bày trong báo cáo | Phần triển khai chính |
|:--|:--|--:|--:|:--|:--|:--|
| YC1 | Define an ontology for the selected domain | 2,0 | **2,0** | Đạt | [Báo cáo, mục 3](docs/Bao_cao.md#3-yc1--ontology-vừa-đủ-cho-lĩnh-vực-phim), PDF trang 2 | [Ontology OWL](ontology/Movie_Ontology.owl), [lược đồ Turtle](ontology/movie.ttl), `src/build.py::schema()` |
| YC2 | Collect relevant data in this domain | 2,0 | **2,0** | Đạt | [Báo cáo, mục 4](docs/Bao_cao.md#4-yc2--thu-thập-dữ-liệu-thật-có-thể-kiểm-tra-lại), PDF trang 2 | [Mã thu thập](src/collect.py), [danh mục nguồn](data/raw/snapshots.json), [kết quả thu thập](evidence/collection.json) |
| YC3 | Transform collected data into 4* standard | 2,0 | **1,5** | Đạt một phần; thiếu truy cập công khai | [Báo cáo, mục 5](docs/Bao_cao.md#5-yc3--chuyển-đổi-rdf-và-điều-kiện-4-sao), PDF trang 3 | [Mã chuyển đổi](src/build.py), [RDF](data/processed/movies.ttl), [giấy phép](LICENSE-DATA.txt), [trạng thái xuất bản](evidence/publication.json) |
| YC4 | Find and establish links to other datasets to obtain 5* standard | 2,0 | **1,5** | Liên kết đã có; chưa hoàn tất LOD 5 sao công khai | [Báo cáo, mục 6](docs/Bao_cao.md#6-yc4--liên-kết-ngoài-để-tạo-ngữ-cảnh), PDF trang 3 | `src/build.py::add_link()`, [kiểm kê liên kết](evidence/link_audit.json), [truy vấn liên kết](queries/05_external_links.rq) |
| YC5 | Provide an interface via SPARQL endpoint/terminal to query data | 2,0 | **2,0** | Đạt | [Báo cáo, mục 7](docs/Bao_cao.md#7-yc5--giao-diện-endpoint-và-terminal-chạy-thực-tế), PDF trang 4 | [Endpoint](src/server.py), [terminal](src/query.py), [giao diện](web/dist/index.html), [8 truy vấn mẫu](queries/) |
| **Tổng** | | **10,0** | **9,0** | **3 yêu cầu đạt đầy đủ, 2 yêu cầu đạt một phần** | [Báo cáo PDF](docs/Bao_cao.pdf) | |

## 2. YC1 — Ontology: 2,0/2,0

| Mục chấm | Tối đa | Đạt | Minh chứng cụ thể |
|:--|--:|--:|:--|
| Có các lớp phù hợp với lĩnh vực phim | 0,5 | 0,5 | `src/build.py`, hàm `schema()`, dòng 19: tạo 9 lớp `Film`, `Person`, `Genre`, `Country`, `Language`, `Credit`, `ContributionRole`, `SourceSnapshot`, `Dataset`. Đếm trực tiếp `owl:Class` trong [movie.ttl](ontology/movie.ttl) được 9 lớp. |
| Có quan hệ và thuộc tính giá trị, domain/range | 0,5 | 0,5 | [movie.ttl](ontology/movie.ttl): `dbo:director` ở dòng 10; `ex:hasGenre` dòng 35; `ex:releaseYear` dòng 45; `ex:runtimeMinutes` dòng 53. Quan hệ phim–người và các giá trị năm/thời lượng được khai báo rõ. |
| Có ngữ nghĩa OWL và ràng buộc mô hình | 0,5 | 0,5 | [movie.ttl](ontology/movie.ttl): `Credit` dòng 140 có cardinality đúng 1 người, 1 phim, 1 vai trò; quan hệ inverse ở dòng 10 và 121; `AllDisjointClasses` dòng 181. [validate.py](src/validate.py) bổ sung kiểm tra cơ bản bằng Python. |
| Có ontology đọc được và minh chứng suy luận | 0,5 | 0,5 | [Movie_Ontology.owl](ontology/Movie_Ontology.owl) parse được và tương đương lược đồ Turtle. [test_application.py](tests/test_application.py), `test_owl_inverse_rule_and_domain_alignment()`, dòng 65: OWL RL suy ra Nolan `ex:directed` Inception và Inception thuộc `dbo:Film`; test chạy lại pass. |

**Giới hạn của kết luận:** đã kiểm tra parse, tính nhất quán giữa các bản xuất và một quy tắc suy luận thực tế. Chưa chạy phân loại toàn bộ ontology bằng reasoner OWL DL trong Protégé. Đề gốc không bắt buộc bước này nên không tự đặt thêm khoản trừ điểm.

## 3. YC2 — Thu thập dữ liệu: 2,0/2,0

| Mục chấm | Tối đa | Đạt | Minh chứng cụ thể |
|:--|--:|--:|:--|
| Có dữ liệu liên quan đến lĩnh vực đã chọn | 0,5 | 0,5 | [config.json](config.json) chọn 30 phim; đếm graph được 30 phim, 805 người, 936 credit, 75 thể loại, 11 quốc gia, 15 ngôn ngữ. Cả 30 phim có năm, thời lượng và đạo diễn. |
| Có mã thu thập từ nguồn thật | 0,5 | 0,5 | [collect.py](src/collect.py), `fetch()` dòng 15 và `collect()` dòng 56: gọi API Wikidata và JSON DBpedia; lấy phim theo sitelink Wikipedia tiếng Anh chính xác. |
| Giữ dữ liệu gốc và thông tin nguồn | 0,5 | 0,5 | [snapshots.json](data/raw/snapshots.json) liệt kê 56 phản hồi gốc với `url`, `provider`, `retrieved_at`, `http_status`, `sha256`, `path`. Các file phản hồi và metadata được lưu trong [data/raw/](data/raw/). |
| Có thể kiểm tra và chạy lại từ nguồn đã lưu | 0,5 | 0,5 | `fetch()` kiểm tra SHA-256 trước khi dùng cache; `--refresh` dùng để tải lại. Tính lại hash trong lần chấm này: **56/56 khớp**. [collection.json](evidence/collection.json) ghi nhận đủ 30/30 phim. |

**Các trường hợp chưa đầy đủ đã được ghi nhận:** Tenet và The Prestige không được nối DBpedia vì chủ thể phản hồi không khai báo rõ `dbo:Film`; cả hai vẫn có dữ liệu và liên kết Wikidata. [quality_issues.json](evidence/quality_issues.json) có 19 ghi nhận: 13 thiếu nhãn tiếng Anh bị bỏ qua, 4 phim có nhiều thời lượng, 2 thực thể không khai báo rõ là người bị loại khỏi `Person`.

Các giới hạn này cần trình bày khi bảo vệ. Đề không yêu cầu số phim tối thiểu, mọi thuộc tính đều đầy đủ hoặc mỗi phim phải có liên kết đến cả hai nguồn, nên không trừ điểm chỉ vì mẫu có 30 phim hay chỉ có 28 liên kết DBpedia. Kiểm tra lần này dùng nguồn đã lưu, không tải mới toàn bộ dữ liệu từ Internet.

## 4. YC3 — Chuyển đổi theo mức 4 sao: 1,5/2,0

| Mục chấm | Tối đa | Đạt | Minh chứng cụ thể |
|:--|--:|--:|:--|
| Chuyển dữ liệu thu thập thành RDF có kiểu và quan hệ | 0,5 | 0,5 | [build.py](src/build.py), `build()` dòng 79: tạo 12.089 triple; chuẩn hóa năm/thời lượng; tạo credit và provenance. [movies.ttl](data/processed/movies.ttl) và [movies.jsonld](data/processed/movies.jsonld) tương đương graph; kiểm tra Python đạt `data_checks_passed = true`. |
| Dùng HTTP(S) IRI và có phần tra cứu thực thể | 0,5 | 0,5 | [common.py](src/common.py) định nghĩa namespace từ `base_url`; ví dụ IRI phim kết thúc bằng `/resource/film-Q25188`. [server.py](src/server.py), `resource()` dòng 56 và `describe()` dòng 66: HTML, HTTP 303, Turtle/JSON-LD. Test tra cứu thực thể cục bộ pass; [trang Inception](web/dist/resource/film-Q25188/index.html) có JSON-LD nhúng và liên kết RDF. |
| Có định dạng mở, giấy phép và metadata bộ dữ liệu | 0,5 | 0,5 | Có Turtle, JSON-LD, CSV; [LICENSE-DATA.txt](LICENSE-DATA.txt) ghi CC BY-SA 4.0 và nguồn. `build.py` dòng 160 tạo `dct:license`, `dct:source`, `void:dataDump`; dữ liệu trong `web/dist/data/movies.ttl` khớp bản xử lý. |
| Dữ liệu và IRI được truy cập công khai trên Web | 0,5 | **0,0** | [publication.json](evidence/publication.json) ghi `status = succeeded` nhưng `audience = private`. Kiểm tra HTTP không đăng nhập đến URL dữ liệu nhận **401**, không nhận RDF. Chưa chứng minh được điều kiện công khai. |

**Lý do thiếu 0,5 điểm:** chuyển đổi RDF và chuẩn bị Web đã hoàn thành, nhưng dữ liệu chưa được công bố cho người ngoài truy cập. IRI chứa tên miền HTTPS và có file RDF trong repo chưa đủ chứng minh mức Open Data 4 sao.

Thang sao là cộng dồn: có dữ liệu trên Web với giấy phép mở trước, rồi thêm định dạng có cấu trúc, định dạng mở, RDF/định danh và liên kết ngoài. Căn cứ: [W3C — Linked Data, mục “Is your Linked Open Data 5 Star?”](https://www.w3.org/DesignIssues/LinkedData.html#fivestar).

## 5. YC4 — Liên kết để đạt mức 5 sao: 1,5/2,0

| Mục chấm | Tối đa | Đạt | Minh chứng cụ thể |
|:--|--:|--:|:--|
| Có liên kết RDF đến các dataset bên ngoài | 0,5 | 0,5 | Đếm trực tiếp `owl:sameAs` được **964 liên kết**: 936 Wikidata, 28 DBpedia. [movies.ttl](data/processed/movies.ttl), [link_audit.json](evidence/link_audit.json). |
| Có phương pháp nối danh tính rõ ràng | 0,5 | 0,5 | `collect.py::collect()` lấy QID qua sitelink chính xác và kiểm tra chủ thể DBpedia có kiểu `dbo:Film`. `build.py::add_link()` dòng 93 ghi hai IRI và phương pháp nối, dùng QID nguồn hoặc cùng tiêu đề Wikipedia kèm kiểm tra kiểu. |
| Có kiểm kê, độ bao phủ và truy vấn chứng minh liên kết | 0,5 | 0,5 | Tập cặp IRI trong audit **khớp hoàn toàn** với `owl:sameAs` trong graph; mọi dòng có phương pháp nối. 30/30 phim có liên kết ngoài. [05_external_links.rq](queries/05_external_links.rq) chạy lại trả 58 dòng liên kết của phim; [08_ask.rq](queries/08_ask.rq) trả `true` cho Inception–Wikidata. |
| Hoàn tất mức 5 sao trên nền dữ liệu mở mức 4 sao | 0,5 | **0,0** | Điều kiện xuất bản công khai của YC3 chưa hoàn tất, nên chưa thể xác nhận LOD 5 sao công khai. [publication.json](evidence/publication.json) vẫn là `private`. |

**Lý do thiếu 0,5 điểm:** yêu cầu đề nói “to obtain 5* standard”, bao gồm kết quả đạt mức sao, ngoài việc tạo liên kết. Theo cách chấm đề xuất, điều kiện công khai có một mục 0,5 điểm ở YC3 và một mục 0,5 điểm về hoàn tất mức 5 sao ở YC4; cùng một việc xuất bản còn thiếu ảnh hưởng hai đầu ra phụ thuộc nhau. Cách phân bổ này được công khai để người chấm có thể điều chỉnh trọng số.

**Cách hiểu số liệu:** 936 liên kết Wikidata là tổng liên kết của 30 phim + 805 người + 75 thể loại + 11 quốc gia + 15 ngôn ngữ. Con số này tình cờ bằng số credit; không có nghĩa mỗi credit được nối Wikidata.

**Giới hạn kiểm tra liên kết:** đã đối chiếu cấu trúc, phương pháp tạo và độ khớp giữa audit với graph. Chưa truy cập lại toàn bộ 964 IRI ngoài hoặc xác minh thủ công mọi danh tính; số lượng liên kết và kiểm tra cấu trúc không tự chứng minh mọi liên kết đều đúng ngoài đời.

## 6. YC5 — Giao diện SPARQL: 2,0/2,0

| Mục chấm | Tối đa | Đạt | Minh chứng cụ thể |
|:--|--:|--:|:--|
| Có endpoint hoặc terminal truy vấn graph thực tế | 0,5 | 0,5 | [server.py](src/server.py), `sparql()` dòng 32: endpoint `/sparql` dùng RDFLib. [query.py](src/query.py): nhận file `.rq`, đọc graph và thực thi truy vấn. |
| Có giao diện nhập truy vấn và xem kết quả | 0,5 | 0,5 | [index.html](web/dist/index.html) có ô SPARQL, câu hỏi mẫu, vùng kết quả, tải kết quả. [app.js](web/dist/app.js), `execute()` dòng 23: gọi endpoint cục bộ hoặc Comunica trong trình duyệt. |
| Có truy vấn mẫu thể hiện khai thác dữ liệu | 0,5 | 0,5 | 8 file trong [queries/](queries/) đều chạy lại thành công; có phim, đạo diễn, vai trò, liên kết, thống kê, nguồn và ASK. Inception trả Christopher Nolan; truy vấn Nolan trả 8 phim. |
| Có kiểm chứng giao thức và xử lý kết quả/lỗi | 0,5 | 0,5 | [test_application.py](tests/test_application.py): `test_get_and_post_sparql_protocol()` dòng 32; `test_ask_and_construct()` dòng 42; `test_invalid_and_remote_queries_are_rejected()` dòng 49. Test GET/POST, SELECT/ASK/CONSTRUCT và truy vấn sai đều pass. |

Endpoint Python hiện chạy **cục bộ**; bản hosted tĩnh dùng Comunica để truy vấn trong trình duyệt, không phải minh chứng endpoint Python đã được deploy. YC5 vẫn đạt vì đề cho phép endpoint/terminal và repo có cả hai cách chạy cục bộ. Đề không bắt buộc endpoint công khai hay truy vấn liên hợp `SERVICE`.

## 7. Sản phẩm nộp theo “Expected Outcome”

| Sản phẩm đề yêu cầu | File kiểm tra | Kết quả | Phạm vi kết luận |
|:--|:--|:--|:--|
| Slide | [Slide.pptx](docs/Slide.pptx), [Slide.pdf](docs/Slide.pdf) | **Đạt về sản phẩm:** PPTX 8 slide, PDF 8 trang | Đã mở cấu trúc PPTX/PDF và đếm trực tiếp; không chấm riêng chất lượng thuyết trình. |
| Report, không quá 15 trang | [Bao_cao.pdf](docs/Bao_cao.pdf) | **Đạt:** 5 trang | Đã đọc phần văn bản PDF; có phần đối chiếu 5 yêu cầu, kiến trúc, kiểm tra và giới hạn. |
| Video, 3–5 phút | [Video_demo.mp4](docs/Video_demo.mp4) | **Đạt về thời lượng:** 256,04644 giây ≈ 4 phút 16 giây | Đo trực tiếp bằng `ffprobe`; chưa xem/nghe toàn bộ video để chấm chất lượng lời đọc hay demo. |

Các file hướng dẫn và kịch bản là tài liệu hỗ trợ, không được tự cộng điểm thưởng. Không dùng số dòng code, dung lượng ontology hay lượng tài liệu để thay thế việc đáp ứng yêu cầu.

## 8. Kết quả kiểm tra lại trong lần chấm này

Những kết quả dưới đây được đo lại từ file hiện tại, không chỉ sao chép số liệu trong `evidence/`:

| Kiểm tra | Kết quả |
|:--|:--|
| `.venv/bin/python -m pytest -q` | **8 passed in 9.70s** |
| Kiểm tra cơ bản bằng Python trên RDF hiện tại | `data_checks_passed = true` |
| Hash các phản hồi gốc | 56/56 khớp SHA-256 |
| Số triple | 12.089 dữ liệu; 169 lược đồ |
| Turtle và JSON-LD dữ liệu | Tương đương graph |
| OWL ontology và lược đồ Turtle | Tương đương graph |
| OWL knowledge graph và dữ liệu + lược đồ | Tương đương graph |
| RDF trong bản Web và bản xử lý | Tương đương graph |
| Kiểm kê liên kết và graph | Khớp toàn bộ 964 cặp IRI |
| Độ bao phủ phim | 30/30 có năm, thời lượng, đạo diễn, nguồn và liên kết ngoài |
| Kiểm tra sản phẩm nộp | Báo cáo 5 trang; PPTX/PDF slide 8 trang/slide; video 256,04644 giây |
| Truy cập URL Turtle không đăng nhập | HTTP **401**, `Content-Type: text/html; charset=utf-8`; chưa truy cập được RDF công khai |

URL kiểm tra truy cập: `https://movie-lod-semantic-web.laminhtrung2001.chatgpt.site/data/movies.ttl`.

Kết quả 8 truy vấn mẫu:

| File | Kiểu | Kết quả |
|:--|:--|:--|
| [01_films.rq](queries/01_films.rq) | SELECT | 30 dòng |
| [02_inception.rq](queries/02_inception.rq) | SELECT | 1 dòng |
| [03_nolan.rq](queries/03_nolan.rq) | SELECT | 8 dòng |
| [04_credits.rq](queries/04_credits.rq) | SELECT | 23 dòng |
| [05_external_links.rq](queries/05_external_links.rq) | SELECT | 58 dòng |
| [06_genres.rq](queries/06_genres.rq) | SELECT | 75 dòng |
| [07_source.rq](queries/07_source.rq) | SELECT | 2 dòng |
| [08_ask.rq](queries/08_ask.rq) | ASK | `true` |

[browser_checks.json](evidence/browser_checks.json) lưu 9 kiểm tra trình duyệt đã pass, kèm [ảnh giao diện](evidence/screenshots/). Đây là minh chứng có sẵn; **không chạy lại trình duyệt trong lần chấm này**. Các biên bản `evidence/validation.json`, `evidence/statistics.json`, `evidence/deliverables.json` được đối chiếu với số liệu đo lại; không sửa nội dung của chúng để nâng điểm.

## 9. Phần cần hoàn tất để xét đủ 10/10 theo thang đề xuất

1. Công bố dữ liệu với quyền truy cập công khai thực tế; giấy phép mở hiện đã có.
2. Kiểm tra từ phiên không đăng nhập: trang dataset, URL Turtle/JSON-LD và IRI Inception phải truy cập được; IRI phải cung cấp mô tả và đường dẫn đến RDF. Kiểm tra thêm IRI lớp như `/ontology#Film`. HTTP 303 ở máy chủ cục bộ hiện có chưa chứng minh hành vi của bản hosted.
3. Ghi lại trạng thái xuất bản thực tế và kiểm tra HTTP trong minh chứng; đồng bộ phần trạng thái trong README/báo cáo rồi tạo lại PDF nếu dùng để nộp. **Chỉ đổi `audience` trong JSON không đủ.**
4. Khi truy cập công khai và tra cứu IRI được xác nhận, chấm lại mục công khai ở YC3 (+0,5) và mục hoàn tất LOD 5 sao ở YC4 (+0,5). Nếu các kiểm tra khác vẫn đạt, tổng theo thang này là **10,0/10**.

Phần đánh giá này chỉ tạo file chấm điểm; không thay đổi quyền xuất bản của website.

## 10. Cập nhật: tái sử dụng trực tiếp lớp DBpedia

| Lớp tái sử dụng | Dữ liệu cục bộ hiện tại | Minh chứng triển khai |
|:--|:--|:--|
| `dbo:Film` | 30 phim | `src/build.py::schema()` và `build()`; `queries/02_inception.rq`; `src/validate.py` |
| `dbo:Person` | 805 người | Kiểu thực thể, domain/range và cardinality của `ex:participant`; kiểm tra credit bằng Python |
| `dbo:Country` | 11 quốc gia | Kiểu thực thể và range của `ex:country` |

Mô hình hiện có 3 lớp DBpedia và 6 lớp `ex:`. Ba lớp tái sử dụng xuất hiện trực tiếp trong `rdf:type`, domain/range, ràng buộc OWL và kiểm tra Python; các truy vấn phim dùng `dbo:Film`. Đây là việc tái sử dụng từ vựng ở YC1; các liên kết cá thể `owl:sameAs` ở YC4 vẫn có 964 liên kết.

Kết quả kiểm tra bản sửa: 12.089 triple dữ liệu, **166 triple lược đồ**, 8 test pass; kiểm tra Python đạt data_checks_passed = true; 8 truy vấn mẫu và 9 kiểm tra trình duyệt đều pass. `tests/test_application.py::test_dbpedia_class_queries_and_owl_inverse_rule()` xác nhận truy vấn trực tiếp các lớp DBpedia không cần suy luận, cùng quy tắc inverse và range.

Đã tạo lại báo cáo, hướng dẫn, slide, video và ảnh giao diện theo namespace mới. [statistics.json](evidence/statistics.json), [validation.json](evidence/validation.json), [tests.txt](evidence/tests.txt) và [browser_checks.json](evidence/browser_checks.json) chứa minh chứng cập nhật.

**Trạng thái hosted hiện tại:** [publication_checks.json](evidence/publication_checks.json) ghi các URL dữ liệu, thực thể, ontology và giấy phép trả HTTP 200. Graph hosted chưa có thực thể được khai báo trực tiếp `dbo:Film`, còn graph cục bộ có 30 phim kiểu này. [publication.json](evidence/publication.json) ghi audience `public` và `local_changes_pending_publication = true`; cần xuất bản lại bản sửa để đồng bộ trước khi đánh giá lại trọn bộ.

## 11. Cập nhật: giản lược kiểm tra dữ liệu

Bản hiện tại dùng `src/validate.py::check_data()` để kiểm tra các trường cơ bản: phim có một tên, nguồn và liên kết ngoài; credit có một phim, một người và một vai trò; nguồn có URL, thời điểm và SHA-256. Vẫn kiểm tra hash phản hồi gốc, chạy 8 truy vấn và test ứng dụng. Ràng buộc cardinality, domain/range và inverse tiếp tục nằm trong ontology OWL.

Đề gốc chỉ yêu cầu ontology, thu thập, mức 4–5 sao và giao diện truy vấn; công cụ kiểm tra ngoài 5 yêu cầu không được tự cộng điểm. Thay đổi này không làm mất một tiêu chí của đề.

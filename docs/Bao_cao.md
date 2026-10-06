---
title: "MovieLOD: ứng dụng dữ liệu phim liên kết"
date: "Báo cáo học phần Semantic Web • 06/10/2026"
---

## 1. Mục tiêu và yêu cầu đề bài

**Mục tiêu:** xây dựng một ứng dụng Linked Open Data (LOD — dữ liệu mở có liên kết) về điện ảnh. Người dùng xem phim, truy lại nguồn và đặt câu hỏi bằng SPARQL. Mô hình được giới hạn ở phần cần cho bài, gồm **9 lớp**.

| Đề gốc | Dịch và sản phẩm tương ứng |
|:--|:--|
| Define an ontology for the selected domain | **YC1:** định nghĩa mô hình điện ảnh → ontology OWL, sơ đồ và quy tắc. |
| Collect relevant data in this domain | **YC2:** thu thập dữ liệu → mã thu thập, phản hồi gốc, URL, thời điểm và mã băm. |
| Transform collected data into 4* standard | **YC3:** biểu diễn theo chuẩn 4 sao → RDF, IRI, giấy phép mở và công bố dữ liệu. |
| Find and establish links to other datasets to obtain 5* standard | **YC4:** nối dữ liệu với bộ dữ liệu khác → liên kết đúng danh tính tới Wikidata/DBpedia. |
| Provide an interface via SPARQL endpoint/terminal to query data | **YC5:** có nơi chạy truy vấn → giao diện Web, endpoint và terminal. |

**Sản phẩm kèm theo:** báo cáo này; `Slide.pptx` và `Slide.pdf`; `Video_demo.mp4` dài 3–5 phút; hướng dẫn chạy từ A đến Z.

## 2. Kiến trúc và quy trình

**Chọn phim → tải dữ liệu → kiểm tra danh tính → chuẩn hóa → tạo RDF → kiểm tra → truy vấn → xuất bản.**

| Thành phần | Việc thực hiện | File chính |
|:--|:--|:--|
| Thu thập | Tải API Wikidata và JSON DBpedia; lưu nguyên phản hồi. | `src/collect.py`; `data/raw/` |
| Chuyển đổi | Tạo định danh, lớp, quan hệ, credit và thông tin nguồn. | `src/build.py` |
| Chất lượng | Kiểm tra dữ liệu bằng Python, mã băm, truy vấn và quy tắc suy luận. | `src/validate.py`; `tests/` |
| Ứng dụng | Giao diện Web; endpoint cục bộ dùng RDFLib; bản hosted dùng Comunica. | `src/server.py`; `web/dist/` |
| Minh chứng | Kết quả đo thực tế, ảnh giao diện, báo cáo và video. | `evidence/`; `docs/` |

**Trạng thái xuất bản:** Đã xuất bản công khai; người có URL truy cập được dữ liệu và giao diện. Bản hosted còn dùng kiểu lớp trước lần sửa; bản trong repo đã dùng trực tiếp dbo:Film, dbo:Person, dbo:Country và cần xuất bản lại để đồng bộ.

\newpage

## 3. YC1 — Ontology vừa đủ cho lĩnh vực phim

| Lớp / thuật ngữ | Dịch | Ý nghĩa |
|:--|:--|:--|
| dbo:Film; dbo:Person | Phim; người | Tái sử dụng trực tiếp lớp DBpedia cho đối tượng trung tâm. |
| ex:Genre; dbo:Country; ex:Language | Thể loại; quốc gia; ngôn ngữ | Country tái sử dụng DBpedia; Genre và Language thuộc mô hình của bài. |
| Credit; ContributionRole | Bản ghi đóng góp; vai trò | Ai làm việc gì trong phim nào? |
| SourceSnapshot; Dataset | Bản ghi nguồn; bộ dữ liệu | Thông tin lấy từ đâu, được công bố thế nào? |

Một **credit** nối đúng **1 phim, 1 người, 1 vai trò**. Ba vai trò được dùng là đạo diễn, diễn viên, biên kịch. Ví dụ: Inception → credit đạo diễn → Christopher Nolan, với role `DirectorRole`.

Quan hệ đối tượng (*object property*) nối hai thực thể: `dbo:director`, `ex:hasGenre`, `ex:participant`. Thuộc tính giá trị (*data property*) nối thực thể với giá trị: `ex:title`, `ex:releaseYear`, `ex:runtimeMinutes`.

**Quy tắc OWL:** các lớp chính loại trừ nhau; một credit có số lượng giá trị cố định và loại giá trị được quy định. `director` là quan hệ ngược của `directed`: nếu phim có đạo diễn Nolan, có thể suy ra Nolan đã đạo diễn phim đó. Test xác nhận truy vấn trực tiếp các lớp DBpedia, rồi chạy OWL RL để kiểm tra quan hệ ngược và suy luận range `dbo:Person`; đây không phải tuyên bố đã chạy phân loại toàn bộ bằng reasoner OWL DL.

**Tái sử dụng từ vựng:** dùng trực tiếp `dbo:Film`, `dbo:Person`, `dbo:Country` trong kiểu thực thể, domain/range, cardinality và SPARQL. Mô hình gồm 3 lớp DBpedia và 6 lớp `ex:`. Dùng `owl:sameAs` để nối cá thể cùng danh tính, PROV cho nguồn, Dublin Core cho giấy phép và VoID cho bộ dữ liệu. Tái sử dụng lớp và liên kết cá thể là hai việc riêng. Các file OWL đều mở được bằng Protégé.

## 4. YC2 — Thu thập dữ liệu thật, có thể kiểm tra lại

Danh sách chọn có **30 phim**. Đây là mẫu có chủ đích để minh họa ứng dụng, không phải toàn bộ phim trên thế giới. API Wikidata được truy theo **sitelink Wikipedia tiếng Anh chính xác**, không đoán danh tính từ tên gần giống.

| Chỉ số từ lần chạy | Kết quả |
|:--|--:|
| Phim / người | 30 / 805 |
| Credit | 936 |
| Thể loại / quốc gia / ngôn ngữ | 75 / 11 / 15 |
| Phản hồi nguồn đã lưu | 56 |
| Phim có năm / thời lượng / đạo diễn | 30 / 30 / 30 |

Mỗi phản hồi có URL, thời điểm lấy, HTTP status và SHA-256. **Mã băm** là dấu vân tay của nội dung; dùng để kiểm tra phản hồi có bị đổi không. 56 phản hồi đã được kiểm tra khớp mã băm.

**Chọn nguồn:** dùng nhãn và các phát biểu của Wikidata cho thông tin chính; không nhập nguyên các nhãn/`sameAs` bị trộn của DBpedia. Chỉ nối DBpedia khi chủ thể đúng tiêu đề Wikipedia và được khai báo `dbo:Film`.

\newpage

## 5. YC3 — Chuyển đổi RDF và điều kiện 4 sao

Một **triple** gồm chủ thể → quan hệ → đối tượng/giá trị. Dữ liệu có **12089 triple**, ontology có **166 triple**. Có bản Turtle, JSON-LD, CSV; có OWL chỉ chứa lược đồ và OWL chứa cả đồ thị.

| Việc chuẩn hóa | Cách thực hiện |
|:--|:--|
| Định danh ổn định | Dùng QID nguồn để tạo IRI, ví dụ `film-Q25188`; cùng thực thể được tái sử dụng. |
| Năm phát hành | Năm sớm nhất trong các ngày nguồn có lịch Gregory và độ chính xác ít nhất đến năm. |
| Thời lượng | Chuyển đơn vị phút/giây/giờ về phút; không tự điền giá trị thiếu. |
| Nhiều giá trị nguồn | Ưu tiên phát biểu có rank preferred; ghi các thời lượng khác vào nhật ký chất lượng. |
| Đóng góp | Tạo credit riêng theo bộ phim–người–vai trò, giữ nguồn của phát biểu. |
| Nguồn dữ liệu | `sourceSnapshot` nối bản ghi với URL, thời điểm và SHA-256. |

**Giấy phép dữ liệu:** CC BY-SA 4.0, có ghi công Wikidata, DBpedia và Wikipedia contributors. Dữ liệu có ghi giấy phép trong RDF và trong `LICENSE-DATA.txt`. Mã ứng dụng có giấy phép MIT; thư viện giữ giấy phép của tác giả.

**Định danh phim mẫu:** [Inception](https://movie-lod-semantic-web.laminhtrung2001.chatgpt.site/resource/film-Q25188). Mở IRI sẽ thấy mô tả HTML, liên kết RDF và JSON-LD nhúng. Máy chủ cục bộ còn nhận `Accept: text/turtle`, chuyển hướng HTTP 303 và trả RDF riêng của thực thể.

**Địa chỉ bộ dữ liệu:** [dataset](https://movie-lod-semantic-web.laminhtrung2001.chatgpt.site/dataset), [RDF Turtle](https://movie-lod-semantic-web.laminhtrung2001.chatgpt.site/data/movies.ttl), [ontology](https://movie-lod-semantic-web.laminhtrung2001.chatgpt.site/ontology).

Theo [thang sao Linked Data](https://www.w3.org/DesignIssues/LinkedData.html), các mức sao cộng dồn; có RDF và IRI là phần kỹ thuật, còn Open Data cần công bố trên Web với giấy phép mở. **Trạng thái hiện tại:** Đã xuất bản công khai; người có URL truy cập được dữ liệu và giao diện. Bản hosted còn dùng kiểu lớp trước lần sửa; bản trong repo đã dùng trực tiếp dbo:Film, dbo:Person, dbo:Country và cần xuất bản lại để đồng bộ.

## 6. YC4 — Liên kết ngoài để tạo ngữ cảnh

Có **964 liên kết `owl:sameAs`**: **936** tới Wikidata, **28** tới DBpedia. Liên kết bao phủ phim, người và các thuật ngữ được sử dụng. Mỗi phim có ít nhất một liên kết ngoài.

`sameAs` dịch là **“hai định danh chỉ cùng một thực thể”**. Ví dụ: Inception cục bộ ↔ Wikidata Q25188 ↔ DBpedia Inception. `wasDerivedFrom` dịch là **“được lấy từ”**; quan hệ này nói về nguồn thông tin, không thay thế `sameAs`.

`evidence/link_audit.json` ghi cả hai IRI và phương pháp nối. 5 sao thêm liên kết ngoài trên nền điều kiện 4 sao; không đánh đồng số lượng liên kết với điểm đánh giá.

\newpage

## 7. YC5 — Giao diện, endpoint và terminal chạy thực tế

**Giao diện Web:** có ô nhập SPARQL, câu hỏi mẫu, bảng kết quả, báo lỗi và tải kết quả. Có thể tìm phim và mở IRI để xem nguồn. Bản hosted chạy truy vấn RDF ngay trong trình duyệt bằng Comunica; bản cục bộ gửi truy vấn tới endpoint Python.

**Endpoint cục bộ:** `http://127.0.0.1:8000/sparql`. Hỗ trợ GET, POST form và `application/sparql-query`; trả SPARQL Results JSON cho SELECT/ASK và Turtle cho CONSTRUCT/DESCRIBE. Chỉ truy vấn dataset của bài; không nhận SPARQL Update và không dùng SERVICE/FROM để tải dữ liệu ngoài.

**Terminal:** `.venv/bin/python src/query.py queries/02_inception.rq`. Tám file truy vấn bao gồm danh sách phim, Inception, phim của Nolan, credit, liên kết ngoài, thống kê thể loại, nguồn và ASK.

```sparql
PREFIX ex: <https://movie-lod-semantic-web.laminhtrung2001.chatgpt.site/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?ten ?daoDien WHERE {
  ?phim a dbo:Film ; ex:title "Inception" ;
        ex:title ?ten ; dbo:director ?nguoi .
  ?nguoi rdfs:label ?daoDien .
}
```

**Dịch:** tìm phim tên Inception, đi theo quan hệ đạo diễn, rồi lấy tên người đó. **Kết quả đã kiểm tra:** Inception — Christopher Nolan. `SELECT` chọn cột; `WHERE` đưa mẫu dữ liệu; `?` đánh dấu biến cần tìm. Cú pháp đối chiếu [W3C SPARQL 1.1](https://www.w3.org/TR/sparql11-query/).

![Giao diện thật với truy vấn Inception](../evidence/screenshots/01_app.png){width=95%}

\newpage

## 8. Kiểm tra, giới hạn và cách chạy lại

| Kiểm tra | Minh chứng |
|:--|:--|
| Kiểm tra cơ bản bằng Python | `evidence/validation.json`; data_checks_passed = true. |
| Toàn vẹn phản hồi gốc | `evidence/validation.json`; 56 mã băm khớp. |
| Chạy các truy vấn mẫu | `evidence/query_results.json`; 8 truy vấn đã chạy. |
| Endpoint, nội dung RDF, lỗi đầu vào | `tests/test_application.py`; biên bản `evidence/tests.txt`. |
| Suy luận quan hệ ngược | Test thực thi OWL RL; không lưu kết quả suy luận lẫn vào graph gốc. |
| Giao diện và trình duyệt | `evidence/browser_checks.json`; ảnh desktop/mobile. |
| Xuất bản | `evidence/publication.json` ghi URL, trạng thái và audience thực tế. |

**Giới hạn:** mẫu phim được chọn có chủ đích; không thu thập giải thưởng, streaming hoặc ngân sách. Thông tin có thể thay đổi sau ngày lấy. Dữ liệu thiếu giữ trạng thái chưa biết, không tự gán 0. Năm và thời lượng là giá trị tóm tắt, không mô tả từng quốc gia hoặc từng bản dựng. Kiểm tra Python xác nhận một số trường cơ bản; không chứng minh mọi phát biểu đúng ngoài đời hay mọi ràng buộc OWL đều thỏa mãn.

**Chạy trên macOS/Linux:** vào thư mục `movie_lod_complete`, tạo virtual environment, cài `requirements.txt`, chạy `make all` để thu thập lại từ cache và kiểm tra, rồi `make serve`. Mở `http://127.0.0.1:8000`. Trên macOS có thể chạy `start.command`.

**Chạy lại không cần tải nguồn mới:** dùng phản hồi đã lưu; `collect.py` kiểm tra hash trước khi dùng cache. Dùng `--refresh` nếu muốn tải phiên bản mới từ Internet. Thư viện Python vẫn cần được cài trước khi chạy.

**Đối chiếu cuối:** YC1 có ontology và quy tắc; YC2 có mã thu thập, dữ liệu gốc, nguồn; YC3 có RDF, IRI, giấy phép và bản xuất bản; YC4 có liên kết được kiểm tra; YC5 có giao diện, endpoint và terminal. **Điều kiện công khai của YC3–YC4 phụ thuộc audience của bản hosted nêu ở trên.** Báo cáo không tự gán điểm chính thức.

Nguồn kỹ thuật: [W3C Linked Data](https://www.w3.org/DesignIssues/LinkedData.html), [W3C SPARQL](https://www.w3.org/TR/sparql11-query/), [Wikidata licensing](https://www.wikidata.org/wiki/Wikidata:Licensing), [Comunica](https://comunica.dev/docs/query/getting_started/query_browser_app/).

"""Generate readable Vietnamese hand-in documents from measured project evidence."""
import json
import subprocess
from pathlib import Path
from common import ROOT,BASE,write_json

HEADER=r'''
\usepackage{newunicodechar}
\newunicodechar{→}{\ensuremath{\rightarrow}}
\newunicodechar{↔}{\ensuremath{\leftrightarrow}}
\usepackage{fvextra}
\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaklines=true,breakanywhere=true,fontsize=\small}
\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\small MovieLOD · Bài làm hoàn chỉnh}
\fancyfoot[C]{\small\thepage}\setlength{\headheight}{15pt}
\renewcommand{\arraystretch}{1.14}\setlength{\extrarowheight}{1pt}
\AtBeginEnvironment{longtable}{\small}
\setlength{\emergencystretch}{3em}\setlength{\parskip}{4pt}
\usepackage{titling}\setlength{\droptitle}{-1.5cm}
\pretitle{\begin{center}\Large\bfseries\color{teal}}
\posttitle{\par\end{center}\vspace{-0.5em}}
\predate{\begin{center}\small}\postdate{\par\end{center}\vspace{-1em}}
'''

def main():
    s=json.loads((ROOT/'evidence/statistics.json').read_text())
    v=json.loads((ROOT/'evidence/validation.json').read_text())
    publication_path=ROOT/'evidence/publication.json'
    publication=json.loads(publication_path.read_text()) if publication_path.exists() else {'audience':'private','status':'prepared'}
    public=publication.get('audience')=='public' and publication.get('status')=='succeeded'
    pub_text='Đã xuất bản công khai; người có URL truy cập được dữ liệu và giao diện.' if public else 'Bản chạy và dữ liệu đã chuẩn bị. Bản hosted hiện riêng tư; cần chủ sở hữu cho phép công khai để hoàn tất điều kiện Open Data trên Web.'
    if public and publication.get('local_changes_pending_publication'):
        pub_text+=' Bản hosted còn dùng kiểu lớp trước lần sửa; bản trong repo đã dùng trực tiếp dbo:Film, dbo:Person, dbo:Country và cần xuất bản lại để đồng bộ.'
    report=f'''---
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

**Trạng thái xuất bản:** {pub_text}

\\newpage

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

Danh sách chọn có **{s['films']} phim**. Đây là mẫu có chủ đích để minh họa ứng dụng, không phải toàn bộ phim trên thế giới. API Wikidata được truy theo **sitelink Wikipedia tiếng Anh chính xác**, không đoán danh tính từ tên gần giống.

| Chỉ số từ lần chạy | Kết quả |
|:--|--:|
| Phim / người | {s['films']} / {s['persons']} |
| Credit | {s['credits']} |
| Thể loại / quốc gia / ngôn ngữ | {s['genres']} / {s['countries']} / {s['languages']} |
| Phản hồi nguồn đã lưu | {s['snapshots']} |
| Phim có năm / thời lượng / đạo diễn | {s['with_year']} / {s['with_runtime']} / {s['with_director']} |

Mỗi phản hồi có URL, thời điểm lấy, HTTP status và SHA-256. **Mã băm** là dấu vân tay của nội dung; dùng để kiểm tra phản hồi có bị đổi không. {v['snapshots_checked']} phản hồi đã được kiểm tra khớp mã băm.

**Chọn nguồn:** dùng nhãn và các phát biểu của Wikidata cho thông tin chính; không nhập nguyên các nhãn/`sameAs` bị trộn của DBpedia. Chỉ nối DBpedia khi chủ thể đúng tiêu đề Wikipedia và được khai báo `dbo:Film`.

\\newpage

## 5. YC3 — Chuyển đổi RDF và điều kiện 4 sao

Một **triple** gồm chủ thể → quan hệ → đối tượng/giá trị. Dữ liệu có **{s['data_triples']} triple**, ontology có **{s['schema_triples']} triple**. Có bản Turtle, JSON-LD, CSV; có OWL chỉ chứa lược đồ và OWL chứa cả đồ thị.

| Việc chuẩn hóa | Cách thực hiện |
|:--|:--|
| Định danh ổn định | Dùng QID nguồn để tạo IRI, ví dụ `film-Q25188`; cùng thực thể được tái sử dụng. |
| Năm phát hành | Năm sớm nhất trong các ngày nguồn có lịch Gregory và độ chính xác ít nhất đến năm. |
| Thời lượng | Chuyển đơn vị phút/giây/giờ về phút; không tự điền giá trị thiếu. |
| Nhiều giá trị nguồn | Ưu tiên phát biểu có rank preferred; ghi các thời lượng khác vào nhật ký chất lượng. |
| Đóng góp | Tạo credit riêng theo bộ phim–người–vai trò, giữ nguồn của phát biểu. |
| Nguồn dữ liệu | `sourceSnapshot` nối bản ghi với URL, thời điểm và SHA-256. |

**Giấy phép dữ liệu:** CC BY-SA 4.0, có ghi công Wikidata, DBpedia và Wikipedia contributors. Dữ liệu có ghi giấy phép trong RDF và trong `LICENSE-DATA.txt`. Mã ứng dụng có giấy phép MIT; thư viện giữ giấy phép của tác giả.

**Định danh phim mẫu:** [Inception]({BASE}/resource/film-Q25188). Mở IRI sẽ thấy mô tả HTML, liên kết RDF và JSON-LD nhúng. Máy chủ cục bộ còn nhận `Accept: text/turtle`, chuyển hướng HTTP 303 và trả RDF riêng của thực thể.

**Địa chỉ bộ dữ liệu:** [dataset]({BASE}/dataset), [RDF Turtle]({BASE}/data/movies.ttl), [ontology]({BASE}/ontology).

Theo [thang sao Linked Data](https://www.w3.org/DesignIssues/LinkedData.html), các mức sao cộng dồn; có RDF và IRI là phần kỹ thuật, còn Open Data cần công bố trên Web với giấy phép mở. **Trạng thái hiện tại:** {pub_text}

## 6. YC4 — Liên kết ngoài để tạo ngữ cảnh

Có **{s['same_as']} liên kết `owl:sameAs`**: **{s['wikidata_links']}** tới Wikidata, **{s['dbpedia_links']}** tới DBpedia. Liên kết bao phủ phim, người và các thuật ngữ được sử dụng. Mỗi phim có ít nhất một liên kết ngoài.

`sameAs` dịch là **“hai định danh chỉ cùng một thực thể”**. Ví dụ: Inception cục bộ ↔ Wikidata Q25188 ↔ DBpedia Inception. `wasDerivedFrom` dịch là **“được lấy từ”**; quan hệ này nói về nguồn thông tin, không thay thế `sameAs`.

`evidence/link_audit.json` ghi cả hai IRI và phương pháp nối. 5 sao thêm liên kết ngoài trên nền điều kiện 4 sao; không đánh đồng số lượng liên kết với điểm đánh giá.

\\newpage

## 7. YC5 — Giao diện, endpoint và terminal chạy thực tế

**Giao diện Web:** có ô nhập SPARQL, câu hỏi mẫu, bảng kết quả, báo lỗi và tải kết quả. Có thể tìm phim và mở IRI để xem nguồn. Bản hosted chạy truy vấn RDF ngay trong trình duyệt bằng Comunica; bản cục bộ gửi truy vấn tới endpoint Python.

**Endpoint cục bộ:** `http://127.0.0.1:8000/sparql`. Hỗ trợ GET, POST form và `application/sparql-query`; trả SPARQL Results JSON cho SELECT/ASK và Turtle cho CONSTRUCT/DESCRIBE. Chỉ truy vấn dataset của bài; không nhận SPARQL Update và không dùng SERVICE/FROM để tải dữ liệu ngoài.

**Terminal:** `.venv/bin/python src/query.py queries/02_inception.rq`. Tám file truy vấn bao gồm danh sách phim, Inception, phim của Nolan, credit, liên kết ngoài, thống kê thể loại, nguồn và ASK.

```sparql
PREFIX ex: <{BASE}/ontology#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?ten ?daoDien WHERE {{
  ?phim a dbo:Film ; ex:title "Inception" ;
        ex:title ?ten ; dbo:director ?nguoi .
  ?nguoi rdfs:label ?daoDien .
}}
```

**Dịch:** tìm phim tên Inception, đi theo quan hệ đạo diễn, rồi lấy tên người đó. **Kết quả đã kiểm tra:** Inception — Christopher Nolan. `SELECT` chọn cột; `WHERE` đưa mẫu dữ liệu; `?` đánh dấu biến cần tìm. Cú pháp đối chiếu [W3C SPARQL 1.1](https://www.w3.org/TR/sparql11-query/).

![Giao diện thật với truy vấn Inception](../evidence/screenshots/01_app.png){{width=95%}}

\\newpage

## 8. Kiểm tra, giới hạn và cách chạy lại

| Kiểm tra | Minh chứng |
|:--|:--|
| Kiểm tra cơ bản bằng Python | `evidence/validation.json`; data_checks_passed = {str(v['data_checks_passed']).lower()}. |
| Toàn vẹn phản hồi gốc | `evidence/validation.json`; {v['snapshots_checked']} mã băm khớp. |
| Chạy các truy vấn mẫu | `evidence/query_results.json`; {v['query_files_executed']} truy vấn đã chạy. |
| Endpoint, nội dung RDF, lỗi đầu vào | `tests/test_application.py`; biên bản `evidence/tests.txt`. |
| Suy luận quan hệ ngược | Test thực thi OWL RL; không lưu kết quả suy luận lẫn vào graph gốc. |
| Giao diện và trình duyệt | `evidence/browser_checks.json`; ảnh desktop/mobile. |
| Xuất bản | `evidence/publication.json` ghi URL, trạng thái và audience thực tế. |

**Giới hạn:** mẫu phim được chọn có chủ đích; không thu thập giải thưởng, streaming hoặc ngân sách. Thông tin có thể thay đổi sau ngày lấy. Dữ liệu thiếu giữ trạng thái chưa biết, không tự gán 0. Năm và thời lượng là giá trị tóm tắt, không mô tả từng quốc gia hoặc từng bản dựng. Kiểm tra Python xác nhận một số trường cơ bản; không chứng minh mọi phát biểu đúng ngoài đời hay mọi ràng buộc OWL đều thỏa mãn.

**Chạy trên macOS/Linux:** vào thư mục `movie_lod_complete`, tạo virtual environment, cài `requirements.txt`, chạy `make all` để thu thập lại từ cache và kiểm tra, rồi `make serve`. Mở `http://127.0.0.1:8000`. Trên macOS có thể chạy `start.command`.

**Chạy lại không cần tải nguồn mới:** dùng phản hồi đã lưu; `collect.py` kiểm tra hash trước khi dùng cache. Dùng `--refresh` nếu muốn tải phiên bản mới từ Internet. Thư viện Python vẫn cần được cài trước khi chạy.

**Đối chiếu cuối:** YC1 có ontology và quy tắc; YC2 có mã thu thập, dữ liệu gốc, nguồn; YC3 có RDF, IRI, giấy phép và bản xuất bản; YC4 có liên kết được kiểm tra; YC5 có giao diện, endpoint và terminal. **Điều kiện công khai của YC3–YC4 phụ thuộc audience của bản hosted nêu ở trên.** Báo cáo không tự gán điểm chính thức.

Nguồn kỹ thuật: [W3C Linked Data](https://www.w3.org/DesignIssues/LinkedData.html), [W3C SPARQL](https://www.w3.org/TR/sparql11-query/), [Wikidata licensing](https://www.wikidata.org/wiki/Wikidata:Licensing), [Comunica](https://comunica.dev/docs/query/getting_started/query_browser_app/).
'''
    guide=f'''---
title: "MovieLOD: làm và đọc bài từ A đến Z"
date: "Hướng dẫn ngắn • 06/10/2026"
---

## A. Bạn có gì trong thư mục này?

Đây là **bản độc lập**, không cần mở file OWL mở rộng cũ để chạy. Bài có **{s['films']} phim, 9 lớp**, nguồn thật và một ứng dụng truy vấn.

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

Trong giao diện: chọn câu hỏi Inception → bấm **Chạy truy vấn** → đọc bảng → mở một phim để thấy thông tin và nguồn → tải Turtle nếu muốn xem RDF. Bản hosted: [MovieLOD]({BASE}/).

**Xuất bản:** {pub_text}

\\newpage

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

\\newpage

## E. Chuyển thành RDF — YC3

```bash
.venv/bin/python src/build.py
```

Mã dùng 9 lớp (3 lớp DBpedia và 6 lớp của bài) cùng các quy tắc; biến thông tin đã thu thập thành đồ thị RDF; tạo định danh từ QID; đổi thời lượng về phút; thêm nguồn; xuất Turtle, JSON-LD, CSV và OWL.

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

Mở `evidence/link_audit.json` để xem IRI nội bộ, IRI ngoài và phương pháp nối. Có **{s['same_as']} liên kết** trong lần tạo dữ liệu này. `sameAs` dùng cho danh tính; `wasDerivedFrom` dùng cho nguồn.

## G. Kiểm tra trước khi demo

```bash
.venv/bin/python src/validate.py
.venv/bin/python -m pytest -q
```

Python kiểm tra phim có tên, nguồn, liên kết; credit có đúng phim–người–vai trò; bản ghi nguồn có URL, thời điểm, hash. Mã kiểm tra nằm ở `src/validate.py`. Test còn thử truy vấn, chuyển hướng RDF, câu truy vấn sai và suy luận quan hệ ngược. Kết quả nằm trong `evidence/`.

\\newpage

## H. Truy vấn theo ba cách — YC5

**1. Giao diện:** mở Web, chọn câu hỏi mẫu, chỉnh SPARQL nếu cần, bấm chạy, đọc bảng và tải kết quả. Bản hosted dùng Comunica để hỏi file RDF trong trình duyệt. Bản cục bộ dùng endpoint.

**2. Terminal:**

```bash
.venv/bin/python src/query.py queries/02_inception.rq
```

**3. Endpoint:** chạy server, rồi mở terminal khác:

```bash
curl -X POST http://127.0.0.1:8000/sparql \\
  -H 'Content-Type: application/sparql-query' \\
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

**Trình bày theo 5 ý:** mô hình 9 lớp → nguồn thật có hash → RDF và IRI → liên kết Wikidata/DBpedia → truy vấn ra kết quả. Không cần giải thích các mô-đun giải thưởng hoặc streaming vì bản này không đưa chúng vào phạm vi.

**Nếu lỗi:** kiểm tra đã cài requirements; cổng 8000 chưa bị dùng; dữ liệu đã build. Dùng `--port 8001` nếu cần đổi cổng. API nguồn cần Internet khi thu thập mới; phản hồi cũ được giữ để chạy lại. Trạng thái công khai được ghi đúng trong `evidence/publication.json`.
'''
    docs=ROOT/'docs';docs.mkdir(exist_ok=True)
    (docs/'latex_header.tex').write_text(HEADER,encoding='utf-8')
    for name,content in [('Bao_cao',report),('Huong_dan_A_Z',guide)]:
        md=docs/(name+'.md');md.write_text(content,encoding='utf-8')
        subprocess.run(['pandoc',str(md),'--standalone','--from','markdown','--to','latex','--lua-filter='+str(docs/'code-wrap.lua'),'--include-in-header='+str(docs/'latex_header.tex'),'-V','documentclass=article','-V','fontsize=11pt','-V','geometry:a4paper,margin=19mm','-V','mainfont=Be Vietnam Pro','-V','monofont=Menlo','-V','colorlinks=true','-V','linkcolor=teal','-V','urlcolor=teal','--syntax-highlighting=none','-o',str(docs/(name+'.tex'))],check=True,cwd=docs)
        with (ROOT/'evidence'/('build_'+name+'.log')).open('w') as log:
            subprocess.run(['tectonic',str(docs/(name+'.tex'))],check=True,cwd=docs,stdout=log,stderr=log)
    print('Reports created')

if __name__=='__main__':main()
